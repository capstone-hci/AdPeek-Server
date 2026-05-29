import numpy as np
from sqlalchemy.orm import Session
from app.database.models import Session as SessionModel, AdResult, Ad
import uuid


def aggregate_ad_results(db: Session, ad_id: str) -> dict:
    sessions = db.query(SessionModel).filter(
        SessionModel.ad_id == ad_id,
        SessionModel.eeg_data.isnot(None),
    ).all()

    if not sessions:
        return None

    ad = db.query(Ad).filter(Ad.id == ad_id).first()
    scene_data = ad.scene_data if ad else []

    participant_count = len(sessions)
    attention_list = []
    arousal_list = []
    heatmap_points = []
    gaze_durations = []
    all_frames = []

    for session in sessions:
        if session.eeg_data:
            attention_list.append(session.eeg_data.get("attention", 0))
            arousal_list.append(session.eeg_data.get("arousal", 0))

        if session.synced_frames:
            gaze_durations.append(len(session.synced_frames) * (1 / 30))
            for frame in session.synced_frames:
                heatmap_points.append({
                    "x": frame["gaze"]["x_norm"],
                    "y": frame["gaze"]["y_norm"],
                })
            all_frames.extend(session.synced_frames)

    # 씬별 집계
    scene_results = []
    for scene in scene_data:
        scene_frames = [
            f for f in all_frames
            if scene["start"] <= f["elapsed_ms"] / 1000 < scene["end"]
        ]

        scene_attention = [f["eeg"]["attention"] for f in scene_frames if "eeg" in f]
        scene_arousal = [f["eeg"]["arousal"] for f in scene_frames if "eeg" in f]
        scene_heatmap = [
            {"x": f["gaze"]["x_norm"], "y": f["gaze"]["y_norm"]}
            for f in scene_frames if "gaze" in f
        ]

        scene_results.append({
            "scene": scene["scene"],
            "start": scene["start"],
            "end": scene["end"],
            "description": scene["description"],
            "avg_attention": round(float(np.mean(scene_attention)), 4) if scene_attention else None,
            "avg_arousal": round(float(np.mean(scene_arousal)), 4) if scene_arousal else None,
            "heatmap_data": scene_heatmap,
        })

    result = {
        "ad_id": ad_id,
        "participant_count": participant_count,
        "avg_attention": round(float(np.mean(attention_list)), 4) if attention_list else None,
        "avg_arousal": round(float(np.mean(arousal_list)), 4) if arousal_list else None,
        "avg_gaze_duration": round(float(np.mean(gaze_durations)), 4) if gaze_durations else None,
        "heatmap_data": heatmap_points,
        "scenes": scene_results,
    }

    existing = db.query(AdResult).filter(AdResult.ad_id == ad_id).first()
    if existing:
        for key, value in result.items():
            setattr(existing, key, value)
    else:
        db.add(AdResult(id=str(uuid.uuid4()), **result))

    db.commit()

    return result