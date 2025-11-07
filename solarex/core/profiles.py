import os
from pathlib import Path

class ProfileManager:
    def __init__(self, app_name="SolarEx", profile_name="Default", incognito=False):
        self.app_name = app_name
        self.profile_name = "Incognito" if incognito else profile_name
        self.incognito = incognito
        base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home()/".config"))
        self.root = base / app_name / "profiles" / self.profile_name
        if not incognito:
            self.root.mkdir(parents=True, exist_ok=True)
    @property
    def cache_path(self): return str(self.root / "cache")
    @property
    def storage_path(self): return str(self.root / "storage")
    def __repr__(self): return f"<Profile {self.profile_name} incognito={self.incognito}>"
