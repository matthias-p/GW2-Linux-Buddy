from pathlib import Path
import json
from typing import List


class LaunchSettings:
    def __init__(self, name, autologin=True, bmp=False, dx11=False, dx9=False, forwardrenderer=False,
                 image=False, log=False, mapLoadInfo=False, nodelta=False, nomusic=False,
                 nosound=False, noui=False, prefreset=False, repair=False, uispanallmonitors=False,
                 useOldFov=False, verify=False, windowed=False):
        self.settingsfile_path: Path = Path(f"~/.linux_buddy/{name}.json").expanduser().resolve()

        self.autologin = autologin
        self.bmp = bmp
        self.dx11 = dx11
        self.dx9 = dx9
        self.forwardrenderer = forwardrenderer
        self.image = image
        self.log = log
        self.mapLoadInfo = mapLoadInfo
        self.nodelta = nodelta
        self.nomusic = nomusic
        self.nosound = nosound
        self.noui = noui
        self.prefreset = prefreset
        self.repair = repair
        self.uispanallmonitors = uispanallmonitors
        self.useOldFov = useOldFov
        self.verify = verify
        self.windowed = windowed

        if self.settingsfile_path.exists():
            self.load()
        else:
            self.write()

    def get_launch_parameter_dict(self) -> dict:
        return {
            "autologin": self.autologin,
            "bmp": self.bmp,
            "dx11": self.dx11,
            "dx9": self.dx9,
            "forwardrenderer":self.forwardrenderer,
            "image": self.image,
            "mapLoadInfo": self.mapLoadInfo,
            "nodelta": self.nodelta,
            "nomusic": self.nomusic,
            "noui": self.noui,
            "prefreset": self.prefreset,
            "repair": self.repair,
            "uispanallmonitors": self.uispanallmonitors,
            "useOldFov": self.useOldFov,
            "verify": self.verify,
            "windowed": self.windowed,
        }

    def write(self):
        with open(self.settingsfile_path, "w", encoding="utf-8") as settings_file:
            json.dump(self.get_launch_parameter_dict(), settings_file, indent=4)

    def load(self):
        with open(self.settingsfile_path, "r", encoding="utf-8") as settings_file:
            settings_dict: dict = json.load(settings_file)

        for key in settings_dict:
            self.__dict__[key] = settings_dict.get(key)

    def make_parameters(self) -> List[str]:
        parameters = []
        for name, value in self.get_launch_parameter_dict().items():
            if value:
                parameters.append(f"-{name}")
        return parameters
