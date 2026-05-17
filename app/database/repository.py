from sqlalchemy.orm import Session
from app.database.models import Session as SessionModel
import uuid


def create_session(db: Session, ad_id: str, start_time: float) -> SessionModel:
    session = SessionModel(
        id=str(uuid.uuid4()),
        ad_id=ad_id,
        start_time=start_time,
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def update_session_gaze(db: Session, ad_id: str, gaze_data: list) -> SessionModel:
    session = db.query(SessionModel).filter(
        SessionModel.ad_id == ad_id
    ).order_by(SessionModel.created_at.desc()).first()

    if session:
        session.gaze_data = gaze_data
        db.commit()
        db.refresh(session)

    return session


def update_session_eeg(db: Session, ad_id: str, eeg_data: dict, synced_frames: list) -> SessionModel:
    session = db.query(SessionModel).filter(
        SessionModel.ad_id == ad_id
    ).order_by(SessionModel.created_at.desc()).first()

    if session:
        session.eeg_data = eeg_data
        session.synced_frames = synced_frames
        db.commit()
        db.refresh(session)

    return session


def get_session_by_ad_id(db: Session, ad_id: str) -> SessionModel:
    return db.query(SessionModel).filter(
        SessionModel.ad_id == ad_id
    ).order_by(SessionModel.created_at.desc()).first()