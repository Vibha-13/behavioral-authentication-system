import csv
from collections import defaultdict
from statistics import variance
from session_monitor import SessionMonitor

# ---------------- Feature Extraction ----------------
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
        press_events[i]["time"] - press_events[i - 1]["time"]
        for i in range(1, len(press_events))
    ]

    total_time = press_events[-1]["time"] - press_events[0]["time"]
    speed = len(press_events) / total_time if total_time > 0 else 0

    return {
        "hold_mean": sum(hold_times) / len(hold_times),
        "delay_mean": sum(inter_delays) / len(inter_delays),
        "speed": speed,
        "hold_var": variance(hold_times) if len(hold_times) > 1 else 0,
        "delay_var": variance(inter_delays) if len(inter_delays) > 1 else 0
    }

# ---------------- Baseline ----------------
baseline = {
    "hold_mean": 0.1595,
    "delay_mean": 0.2010,
    "speed": 5.0744,
    "hold_var": 0.002,
    "delay_var": 0.003
}

# ---------------- Parameters ----------------
LEARNING_THRESHOLD = 0.20
LEARNING_RATE = 0.10

FREEZE_THRESHOLD = 0.60
DECAY_THRESHOLD = 0.50
DECAY_PENALTY = 0.10

W_MEAN = 0.40
W_STABILITY = 0.35
W_SESSION = 0.25

monitor = SessionMonitor(window_size=5)

# ---------------- Compare ----------------
current = extract_features("test_sample.csv")

def norm_diff(a, b):
    return abs(a - b) / b if b > 0 else 0

mean_risk = min((
    norm_diff(current["hold_mean"], baseline["hold_mean"]) +
    norm_diff(current["delay_mean"], baseline["delay_mean"]) +
    norm_diff(current["speed"], baseline["speed"])
) / 3, 1.0)

stability_risk = min((
    norm_diff(current["hold_var"], baseline["hold_var"]) +
    norm_diff(current["delay_var"], baseline["delay_var"])
) / 2, 0.6)


monitor.update(mean_risk)
_, session_risk = monitor.assess()

final_risk = (
    W_MEAN * mean_risk +
    W_STABILITY * stability_risk +
    W_SESSION * session_risk
)

# ---------------- Trust Decay ----------------
if session_risk >= DECAY_THRESHOLD:
    final_risk = min(final_risk + DECAY_PENALTY, 1.0)

# ---------------- Decision ----------------
print(f"\n🔥 Final Risk Score: {final_risk:.2f}")

if final_risk < 0.30:
    verdict = "NORMAL"
elif final_risk < 0.55:
    verdict = "UNCERTAIN"
else:
    verdict = "SUSPICIOUS"

print(f"🔐 AUTH RESULT: {verdict}")

# ---------------- Learning Freeze ----------------
if (
    verdict == "NORMAL"
    and final_risk <= LEARNING_THRESHOLD
    and session_risk < FREEZE_THRESHOLD
):
    print("\n🧠 Adaptive Learning Triggered")
    for k in baseline:
        baseline[k] = (
            (1 - LEARNING_RATE) * baseline[k]
            + LEARNING_RATE * current[k]
        )
else:
    print("\n🛑 Learning Frozen (risk too high or session unstable)")
