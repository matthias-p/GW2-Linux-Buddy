from typing import Dict

from game_utils.client import Client
from lb_settings.settings import Settings


class ClientList:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.client_dict: Dict[str: Client] = {}

        self._init_client_dict()

    def __iter__(self):
        yield from self.client_dict

    def _init_client_dict(self) -> None:
        for wineprefix_dir in sorted(self.settings.wineprefix_path.iterdir()):
            self.client_dict[wineprefix_dir.name] = Client(wineprefix_dir.name, wineprefix_dir,
                                                           self.settings.gamelauncher_path)

    def get_client(self, name: str) -> Client:
        return self.client_dict.get(name)

    def add_client(self, name: str) -> Client:
        new_client = Client(name, self.settings.wineprefix_path / name,
                            self.settings.gamelauncher_path)
        self.client_dict[name] = new_client
        return new_client

    def remove_client(self, name: str) -> bool:
        client: Client = self.client_dict.get(name)
        if client is not None:
            client.remove()
            self.client_dict.pop(name)
            return True
        return False

    def patch_all(self) -> None:
        for client in self.client_dict.values():
            client.launch(["-image"], wait_for_exit=True)
