from sqlalchemy import Column, String, Float, Integer, JSON, DateTime
from sqlalchemy.sql import func
from app.core.database import Base


class Ad(Base):
    __tablename__ = "ads"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    duration = Column(Float, nullable=False)
    scene_data = Column(JSON, nullable=True)  # 추가
    created_at = Column(DateTime, server_default=func.now())


class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True)
    ad_id = Column(String, nullable=False)
    start_time = Column(Float, nullable=False)
    gaze_data = Column(JSON, nullable=True)
    eeg_data = Column(JSON, nullable=True)
    synced_frames = Column(JSON, nullable=True)
    created_at = Column(DateTime, server_default=func.now())


class AdResult(Base):
    __tablename__ = "ad_results"

    id = Column(String, primary_key=True)
    ad_id = Column(String, nullable=False)
    participant_count = Column(Integer, default=0)
    avg_attention = Column(Float, nullable=True)
    avg_arousal = Column(Float, nullable=True)
    avg_gaze_duration = Column(Float, nullable=True)
    peak_attention_time = Column(Float, nullable=True)
    heatmap_data = Column(JSON, nullable=True)
    scenes = Column(JSON, nullable=True)  # 추가
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())