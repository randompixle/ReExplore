import importlib, pkgutil
from dataclasses import dataclass
from typing import Callable, Dict, Optional

@dataclass
class BackendEntry:
    id: str
    name: str
    desc: str
    factory: Callable[[], object]
    settings_schema: list

class RenderManager:
    def __init__(self, core):
        self.core = core
        self.backends: Dict[str, BackendEntry] = {}
        self.active_id: Optional[str] = None
        self._discover()
    def _discover(self):
        import solarex.render.modules as mods
        for m in pkgutil.iter_modules(mods.__path__):
            mod = importlib.import_module(f"solarex.render.modules.{m.name}")
            meta = getattr(mod, "metadata", None)
            factory = getattr(mod, "new_view", None)
            if not meta or not factory: continue
            entry = BackendEntry(
                id=meta.get("id", m.name),
                name=meta.get("name", m.name),
                desc=meta.get("description",""),
                factory=lambda mod=mod: mod,
                settings_schema=getattr(mod, "get_settings_schema", lambda core: [])
            )
            self.backends[entry.id] = entry
    def list_backends(self): return list(self.backends.values())
    def set_active(self, backend_id: str):
        if backend_id not in self.backends: raise RuntimeError(f"Unknown backend '{backend_id}'")
        self.active_id = backend_id
        print(f"[SolarEx] Renderer set to '{backend_id}'")
    def new_view(self, *a, **kw):
        if not self.active_id: raise RuntimeError("No active renderer backend")
        mod = self.backends[self.active_id].factory()
        return mod.new_view(self.core, *a, **kw)

def init(core): core.render = RenderManager(core)
