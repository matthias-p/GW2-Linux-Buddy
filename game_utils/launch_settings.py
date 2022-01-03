from pathlib import Path
import json
from typing import List


class LaunchSettings:
    def __init__(self, name, autologin=True, bmp=False, dx11=False, dx9=False, forwardrenderer=False,
                 image=False, log=False, mapLoadInfo=False, nodelta=False, nomusic=False,
                 nosound=False, noui=False, prefreset=False, repair=False, uispanallmonitors=False,
                 useOldFov=False, verify=False, windowed=False):
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

        if Path(f"~/.linux_buddy/{name}.json").expanduser().resolve().exists():
            self.load(Path(f"~/.linux_buddy/{name}.json").expanduser().resolve())
        else:
            self.write(Path(f"~/.linux_buddy/{name}.json").expanduser().resolve())

    def write(self, path: Path):
        with open(path, "w", encoding="utf-8") as settings_file:
            json.dump(self.__dict__, settings_file, indent=4)

    def load(self, path: Path):
        with open(path, "r", encoding="utf-8") as settings_file:
            settings_dict: dict = json.load(settings_file)

        for key in self.__dict__:
            self.__dict__[key] = settings_dict.get(key)

    def make_parameters(self) -> List[str]:
        parameters = []
        for name, value in self.__dict__.items():
            if value:
                parameters.append(f"-{name}")
        return parameters
