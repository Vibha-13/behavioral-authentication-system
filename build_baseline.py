import csv
import glob
from collections import defaultdict

def extract_features(file_path):
    events = []
    with open(file_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            events.append({
                "event": row["event"],
                "key": row["key"],
                "time": float(row["timestamp"])
            })

    press_times = defaultdict(list)
    release_times = defaultdict(list)

    for e in events:
        if e["event"] == "press":
            press_times[e["key"]].append(e["time"])
        elif e["event"] == "release":
            release_times[e["key"]].append(e["time"])

    hold_times = []
    for key in press_times:
        for p, r in zip(press_times[key], release_times.get(key, [])):
            hold_times.append(r - p)

    press_events = [e for e in events if e["event"] == "press"]
    inter_delays = [
        press_events[i]["time"] - press_events[i-1]["time"]
        for i in range(1, len(press_events))
    ]

    total_time = press_events[-1]["time"] - press_events[0]["time"]
    speed = len(press_events) / total_time if total_time > 0 else 0

    return {
        "hold": sum(hold_times)/len(hold_times),
        "delay": sum(inter_delays)/len(inter_delays),
        "speed": speed
    }

# Build baseline from all samples
features = defaultdict(list)

for file in glob.glob("samples/*.csv"):
    f = extract_features(file)
    for k in f:
        features[k].append(f[k])

baseline = {k: sum(v)/len(v) for k, v in features.items()}

print("🧠 Baseline Behavior (YOU):\n")
for k, v in baseline.items():
    print(f"{k}: {v:.4f}")
