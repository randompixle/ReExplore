class ModuleRegistry:
    def __init__(self):
        self._mods = {}
    def register(self, name: str, mod):
        self._mods[name] = mod
    def require(self, name: str):
        mod = self._mods.get(name)
        if not mod: raise RuntimeError(f"[SolarEx] Required module '{name}' not loaded")
        return mod
