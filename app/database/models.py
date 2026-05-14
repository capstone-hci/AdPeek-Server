from sqlalchemy import Column, String, Float, Integer, JSON, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Ad(Base):
    __tablename__ = "ads"

    id = Column(String, primary_key=True)  # ad_id
    name = Column(String, nullable=False)
    duration = Column(Float, nullable=False)  # 광고 길이 (초)
    created_at = Column(DateTime, server_default=func.now())


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)  # session_id
    ad_id = Column(String, nullable=False)
    start_time = Column(Float, nullable=False)
    gaze_data = Column(JSON, nullable=True)   # gaze 데이터 배열
    eeg_data = Column(JSON, nullable=True)    # EEG 분석 결과
    synced_frames = Column(JSON, nullable=True)  # 동기화 결과
    created_at = Column(DateTime, server_default=func.now())