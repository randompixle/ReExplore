import importlib.util, json, sys
from pathlib import Path

class Plugin:
    def __init__(self, path: Path, manifest: dict):
        self.path = path
        self.manifest = manifest
        self.name = manifest.get("name", path.name)
        self.entry = manifest.get("entry", "main.py")
        self.version = manifest.get("version", "0.0.1")
        self.module = None

    def __repr__(self): return f"<Plugin {self.name} v{self.version}>"

class PluginManager:
    def __init__(self, core_root: Path):
        self.core_root = Path(core_root)
        self.user_root = Path.home() / ".config" / "SolarEx" / "plugins"
        self.plugins = []
        self.by_name = {}

    def discover(self):
        search_dirs = [self.core_root / "Plugins", self.user_root]
        for d in search_dirs:
            if not d.exists():
                continue
            for p in d.glob("*/plugin.json"):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        manifest = json.load(f)
                    pl = Plugin(p.parent, manifest)
                    self.plugins.append(pl)
                    self.by_name[pl.name] = pl
                except Exception as e:
                    print(f"[SolarEx][plugin] Error reading {p}: {e}")
        return self.plugins

    def load_plugin(self, core, plugin: Plugin):
        main_py = plugin.path / plugin.entry
        if not main_py.exists():
            print(f"[SolarEx][plugin] {plugin.name}: no entry file")
            return
        try:
            spec = importlib.util.spec_from_file_location(plugin.name, main_py)
            mod = importlib.util.module_from_spec(spec)
            sys.modules[plugin.name] = mod
            spec.loader.exec_module(mod)
            if hasattr(mod, "init"):
                mod.init(core)
            plugin.module = mod
            print(f"[SolarEx][plugin] Loaded {plugin.name}")
        except Exception as e:
            print(f"[SolarEx][plugin] Failed {plugin.name}: {e}")

    def load_all(self, core):
        for pl in self.plugins:
            self.load_plugin(core, pl)

    def reload(self, core, name: str):
        pl = self.by_name.get(name)
        if not pl:
            print(f"[SolarEx][plugin] No plugin named {name}")
            return
        # drop from sys.modules then reload
        if pl.module and pl.name in sys.modules:
            del sys.modules[pl.name]
        self.load_plugin(core, pl)
