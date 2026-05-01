import json
import os

SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "snake_color": [0, 255, 0], # Green
    "grid": True,
    "sound": True
}

def load_settings():
    settings = DEFAULT_SETTINGS.copy()
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            try:
                loaded = json.load(f)
                # Добавляем загруженные настройки поверх стандартных
                # Если в файле нет ключа 'grid', он останется из DEFAULT_SETTINGS
                for key in loaded:
                    if key in settings:
                        settings[key] = loaded[key]
            except json.JSONDecodeError:
                pass
    return settings
def save_settings(settings):
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(settings, f, indent=4)