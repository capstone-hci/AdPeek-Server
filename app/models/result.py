from pydantic import BaseModel
from app.models.gaze import GazePoint


class EEGBands(BaseModel):
    alpha: float
    beta: float
    theta: float


class EEGResult(BaseModel):
    attention: float
    arousal: float
    bands: EEGBands


class SessionResult(BaseModel):
    ad_id: str
    timestamp: float
    gaze: list[GazePoint]
    eeg: EEGResult