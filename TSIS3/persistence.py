import json
import os

SETTINGS_FILE = 'settings.json'
LEADERBOARD_FILE = 'leaderboard.json'

DEFAULT_SETTINGS = {
    "sound": True,
    "car_color": "Blue",
    "difficulty": "Normal"
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return DEFAULT_SETTINGS.copy()
    return DEFAULT_SETTINGS.copy()

def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_score(name, score, distance):
    lb = load_leaderboard()
    lb.append({"name": name, "score": int(score), "distance": int(distance)})
    lb = sorted(lb, key=lambda x: x['score'], reverse=True)[:10]
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(lb, f, indent=4)