from typing import List

from replay_player import ReplayPlayer

class ReplayPositions:
    def __init__(self, id_: str,
                 ball: List[float], players: List[ReplayPlayer], colors: List[int], names: List[str],
                 frames: List[float]):
        self.ball = ball
        self.players = players
        self.colors = colors
        self.names = names
        self.frames = frames