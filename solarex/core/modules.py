from importlib import import_module
from pathlib import Path
from .registry import ModuleRegistry
from .profiles import ProfileManager
from .plugins import PluginManager
from .uiapi import UIAPI
import os

class SolarCore:
    def __init__(self):
        self.registry = ModuleRegistry()
        self.args = None
        self.profile = None
        self.plugin_manager = None
        self.ui_api = UIAPI(self)
        # events
        self._window_created_listeners = []

    def boot(self):
        print("[SolarEx] Booting modular web system…")
        core_root = Path(__file__).resolve().parent.parent  # solarex/
        self.plugin_manager = PluginManager(core_root)
        self.plugin_manager.discover()
        self.profile = ProfileManager(profile_name="Default", incognito=False)

    def set_profile(self, name: str = "Default", incognito: bool = False):
        self.profile = ProfileManager(profile_name=name, incognito=incognito)
        print(f"[SolarEx] Using profile: {self.profile}")

    def load(self, dotted: str, as_name: str = None):
        mod = import_module(dotted)
        name = as_name or dotted.split('.')[-1]
        if hasattr(mod, "init"):
            mod.init(self)
        self.registry.register(name, mod)
        print(f"[SolarEx] Loaded module '{name}' from '{dotted}'")

    def require(self, name: str):
        return self.registry.require(name)

    # events for plugins
    def on_window_created(self, fn):
        self._window_created_listeners.append(fn)
    def emit_window_created(self, win):
        for fn in list(self._window_created_listeners):
            try: fn(win)
            except Exception as e: print("[SolarEx][event] window_created error:", e)
