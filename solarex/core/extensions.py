import json
from pathlib import Path
EXTS_DIR_NAME = "extensions"
class Extension:
    def __init__(self, manifest_path: Path):
        self.manifest_path = manifest_path
        with open(manifest_path, "r", encoding="utf-8") as f:
            self.manifest = json.load(f)
    @property
    def name(self): return self.manifest.get("name", self.manifest_path.stem)
    @property
    def userscripts(self): return self.manifest.get("userscripts", [])
class ExtensionManager:
    def __init__(self, profile_root: Path):
        self.ext_root = Path(profile_root).parents[2] / EXTS_DIR_NAME
        self.ext_root.mkdir(parents=True, exist_ok=True)
        self.extensions = []
    def discover(self):
        for p in self.ext_root.glob("*/manifest.json"):
            try:
                self.extensions.append(Extension(p))
            except Exception as e:
                print(f"[SolarEx][ext] Failed to load {p}: {e}")
    def list(self): return [e.name for e in self.extensions]
