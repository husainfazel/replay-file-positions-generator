import logging
from typing import Optional

logger = logging.getLogger(__name__)

class CameraSettings:
    def __init__(self, distance: int, field_of_view: int, transition_speed: float,
                 pitch: int, swivel_speed: int, stiffness: float,
                 height: int):
        self.distance = distance
        self.fieldOfView = field_of_view
        self.transitionSpeed = transition_speed
        self.pitch = pitch
        self.swivelSpeed = swivel_speed
        self.stiffness = stiffness
        self.height = height

class ReplayPlayer:
    def __init__(self, id_: str, name: str, is_orange: bool,
                 score: int, goals: int, assists: int, saves: int, shots: int,
                 camera_settings: Optional[CameraSettings], rank: Optional[int],
                 mmr: Optional[int]):
        self.id = id_
        self.name = name
        self.isOrange = is_orange
        self.score = score
        self.goals = goals
        self.assists = assists
        self.saves = saves
        self.shots = shots
        if camera_settings is not None:
            self.cameraSettings = camera_settings.__dict__
        self.rank = rank
        self.mmr = mmr