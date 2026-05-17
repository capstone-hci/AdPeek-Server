import numpy as np
from sqlalchemy.orm import Session
from app.database.models import Session as SessionModel, AdResult
import uuid


def aggregate_ad_results(db: Session, ad_id: str) -> dict:
    """
    특정 광고의 전체 세션 데이터를 집계
    """
    sessions = db.query(SessionModel).filter(
        SessionModel.ad_id == ad_id,
        SessionModel.eeg_data.isnot(None),
    ).all()

    if not sessions:
        return None

    participant_count = len(sessions)
    attention_list = []
    arousal_list = []
    heatmap_points = []
    gaze_durations = []

    for session in sessions:
        if session.eeg_data:
            attention_list.append(session.eeg_data.get("attention", 0))
            arousal_list.append(session.eeg_data.get("arousal", 0))

        if session.synced_frames:
            gaze_durations.append(len(session.synced_frames) * (1 / 30))  # 30Hz 기준
            for frame in session.synced_frames:
                heatmap_points.append({
                    "x": frame["gaze"]["x_norm"],
                    "y": frame["gaze"]["y_norm"],
                })

    result = {
        "ad_id": ad_id,
        "participant_count": participant_count,
        "avg_attention": round(float(np.mean(attention_list)), 4) if attention_list else None,
        "avg_arousal": round(float(np.mean(arousal_list)), 4) if arousal_list else None,
        "avg_gaze_duration": round(float(np.mean(gaze_durations)), 4) if gaze_durations else None,
        "heatmap_data": heatmap_points,
    }

    # DB에 집계 결과 저장
    existing = db.query(AdResult).filter(AdResult.ad_id == ad_id).first()
    if existing:
        for key, value in result.items():
            setattr(existing, key, value)
    else:
        db.add(AdResult(id=str(uuid.uuid4()), **result))

    db.commit()

    return result