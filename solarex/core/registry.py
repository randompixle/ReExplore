class ModuleRegistry:
    def __init__(self):
        self._mods = {}
    def register(self, name: str, mod):
        if name in self._mods:
            print(f"[SolarEx] Module '{name}' already registered, replacing.")
        self._mods[name] = mod
    def get(self, name: str):
        return self._mods.get(name)
    def require(self, name: str):
        mod = self.get(name)
        if not mod:
            raise RuntimeError(f"[SolarEx] Required module '{name}' not loaded")
        return mod
    def all(self):
        return dict(self._mods)
