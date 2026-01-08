import csv
from collections import defaultdict

# Load keystrokes
events = []
with open("keystrokes.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        events.append({
            "event": row["event"],
            "key": row["key"],
            "time": float(row["timestamp"])
        })

# Separate press and release times
press_times = defaultdict(list)
release_times = defaultdict(list)

for e in events:
    if e["event"] == "press":
        press_times[e["key"]].append(e["time"])
    elif e["event"] == "release":
        release_times[e["key"]].append(e["time"])

# Compute key hold times
hold_times = []

for key in press_times:
    for p, r in zip(press_times[key], release_times.get(key, [])):
        hold_times.append(r - p)

# Compute inter-key delays
inter_key_delays = []
press_events = [e for e in events if e["event"] == "press"]

for i in range(1, len(press_events)):
    delay = press_events[i]["time"] - press_events[i - 1]["time"]
    inter_key_delays.append(delay)

# Typing speed
total_time = press_events[-1]["time"] - press_events[0]["time"]
typing_speed = len(press_events) / total_time if total_time > 0 else 0

# Feature summary
features = {
    "avg_hold_time": sum(hold_times) / len(hold_times) if hold_times else 0,
    "avg_inter_key_delay": sum(inter_key_delays) / len(inter_key_delays) if inter_key_delays else 0,
    "typing_speed_keys_per_sec": typing_speed
}

print("🧠 Extracted Behavioral Features:\n")
for k, v in features.items():
    print(f"{k}: {v:.4f}")
