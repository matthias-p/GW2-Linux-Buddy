from pathlib import Path
import json

from game_utils.gw2_api import Gw2API


class Settings:
    settings_path: Path = Path("~/.linux_buddy/settings.json").expanduser().resolve()
    wineprefix_path: Path = None
    gamelauncher_path: Path = None
    game_version: str = None

    def __init__(self, wineprefix_path: str = "~/.linux_buddy/wineprefixes/",
                 gamelauncher_path: str = "~/.linux_buddy/Guild Wars 2/"):
        self.set_wineprefix_path(wineprefix_path)
        self.set_gamelauncher_path(gamelauncher_path)
        self.game_version = Gw2API.get_build()

        self.wineprefix_path.mkdir(parents=True, exist_ok=True)
        self.gamelauncher_path.mkdir(parents=True, exist_ok=True)

        if not self.settings_path.exists():
            self.save()
        self.load()

    def set_wineprefix_path(self, path: str):
        self.wineprefix_path = Path(path).expanduser().resolve()

    def set_gamelauncher_path(self, path: str):
        self.gamelauncher_path = Path(path).expanduser().resolve()

    def save(self):
        with open(self.settings_path, "w", encoding="utf-8") as settings_file:
            json.dump({
                "wineprefix_path": str(self.wineprefix_path),
                "gamelauncher_path": str(self.gamelauncher_path),
                "game_version": self.game_version,
            }, settings_file, indent=4)

    def load(self):
        with open(self.settings_path, "r", encoding="utf-8") as settings_file:
            json_dict: dict = json.load(settings_file)

        self.set_wineprefix_path(json_dict.get("wineprefix_path"))
        self.set_gamelauncher_path(json_dict.get("gamelauncher_path"))
        self.game_version = json_dict.get("game_version")
