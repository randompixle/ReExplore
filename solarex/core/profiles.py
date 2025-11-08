import os
from pathlib import Path

class ProfileManager:
    def __init__(self, app_name="SolarEx", profile_name="Default", incognito=False):
        self.app_name = app_name
        self.profile_name = "Incognito" if incognito else profile_name
        self.incognito = incognito

        cfg_base = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        data_base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))
        self.config_root = cfg_base / app_name / "profiles" / self.profile_name
        self.data_root = data_base / app_name / "profiles" / self.profile_name

        if not incognito:
            self.config_root.mkdir(parents=True, exist_ok=True)
            self.data_root.mkdir(parents=True, exist_ok=True)

    @property
    def cache_path(self): return str(self.data_root / "cache")
    @property
    def storage_path(self): return str(self.data_root / "storage")
    @property
    def cookies_path(self): return str(self.data_root / "cookies.sqlite")
    def __repr__(self): return f"<Profile {self.profile_name} incognito={self.incognito}>"
