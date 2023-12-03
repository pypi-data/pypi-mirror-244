from typing import Iterator
from minecraft_launch.modules.models.install.game_core_entity import GameCoreEntity



class GameCoresEntity():
    def __init__(self, json: dict) -> None:
        self.latest: dict[str, str] = json["latest"]
        cores: list[dict] = json["versions"]
        self.cores: list[GameCoreEntity] = []
        for i in cores:
            core = GameCoreEntity(i)
            self.cores.append(core)

    def __iter__(self) -> Iterator[GameCoreEntity]:
        return iter(self.cores)