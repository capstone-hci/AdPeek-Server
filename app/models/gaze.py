from pydantic import BaseModel


class GazePoint(BaseModel):
    x_norm: float
    y_norm: float
    timestamp: float
    elapsed_ms: int


class GazeSessionData(BaseModel):
    ad_id: str
    start_time: float
    data: list[GazePoint]