import requests
import json


class Gw2API:
    @staticmethod
    def get_build() -> str:
        response = requests.get("https://api.guildwars2.com/v2/build")
        return str(json.loads(response.text).get("id"))
