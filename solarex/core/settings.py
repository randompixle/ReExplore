import json
from pathlib import Path

class Settings:
    def __init__(self, app_name="SolarEx"):
        cfg = Path.home() / ".config" / app_name
        cfg.mkdir(parents=True, exist_ok=True)
        self.path = cfg / "settings.json"
        self._data = {}
        self.load()

    def load(self):
        try:
            self._data = json.loads(self.path.read_text(encoding="utf-8"))
        except Exception:
            self._data = {}

    def save(self):
        try:
            self.path.write_text(json.dumps(self._data, indent=2), encoding="utf-8")
        except Exception as e:
            print("[SolarEx][settings] save failed:", e)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def set(self, key, value):
        self._data[key] = value
        self.save()

    def get_ns(self, ns, key, default=None):
        return self._data.get("namespaces", {}).get(ns, {}).get(key, default)

    def set_ns(self, ns, key, value):
        nsmap = self._data.setdefault("namespaces", {}).setdefault(ns, {})
        nsmap[key] = value
        self.save()
