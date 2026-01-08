import time
import csv
from pynput import keyboard

keystrokes = []

def on_press(key):
    keystrokes.append(("press", str(key), time.time()))

def on_release(key):
    keystrokes.append(("release", str(key), time.time()))
    if key == keyboard.Key.esc:
        return False  # Stop listener

print("⌨️ Start typing normally. Press ESC to stop.\n")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# Save to CSV
with open("keystrokes.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["event", "key", "timestamp"])
    writer.writerows(keystrokes)

print("✅ Keystrokes saved to keystrokes.csv")
