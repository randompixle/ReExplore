from importlib import import_module
from pathlib import Path
from .registry import ModuleRegistry
from .profiles import ProfileManager
from .plugins import PluginManager
from .uiapi import UIAPI
from .settings import Settings

class SolarCore:
    def __init__(self):
        self.registry = ModuleRegistry()
        self.args = None
        self.profile = None
        self.plugin_manager = None
        self.ui_api = UIAPI(self)
        self.settings = Settings()
        self._window_created_listeners = []

    def boot(self):
        print("[SolarEx] Booting modular web system…")
        core_root = Path(__file__).resolve().parent.parent
        self.plugin_manager = PluginManager(core_root)
        self.plugin_manager.discover()
        self.profile = ProfileManager(profile_name="Default", incognito=False)

    def set_profile(self, name="Default", incognito=False):
        self.profile = ProfileManager(profile_name=name, incognito=incognito)
        print(f"[SolarEx] Using profile: {self.profile}")

    def load(self, dotted, as_name=None):
        mod = import_module(dotted)
        if hasattr(mod, "init"): mod.init(self)
        self.registry.register(as_name or dotted.split('.')[-1], mod)
        print(f"[SolarEx] Loaded module '{as_name or dotted.split('.')[-1]}' from '{dotted}'")

    def require(self, name): return self.registry.require(name)

    def on_window_created(self, fn): self._window_created_listeners.append(fn)
    def emit_window_created(self, win):
        for fn in list(self._window_created_listeners):
            try: fn(win)
            except Exception as e: print("[SolarEx][event] window_created error:", e)
