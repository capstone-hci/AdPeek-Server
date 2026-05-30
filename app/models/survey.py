from pydantic import BaseModel
from typing import Optional


class SurveyRequest(BaseModel):
    ad_id: str
    session_id: Optional[str] = None
    recall: str        # "yes" / "unsure" / "no"
    brand_score: int   # 1~5
    emotion: str       # "positive" / "neutral" / "negative"
    comment: Optional[str] = None