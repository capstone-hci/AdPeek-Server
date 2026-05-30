import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal
from app.database.models import Ad

ad_data = {
    "id": "ad_001",
    "name": "건강 깔창 광고",
    "duration": 30.02,
    "scene_data": {
        "video_analysis": {
            "total_duration": "30.02s",
            "total_scenes": 14,
            "scenes": [
                {"scene": 1, "start": 0.00, "end": 1.67, "grid": {"person": [5, 8], "background": [1, 2, 3, 4, 6, 7, 9], "text": [], "product": []}},
                {"scene": 2, "start": 1.67, "end": 4.07, "grid": {"person": [2, 5, 8], "background": [1, 3, 4, 7], "text": [6, 9], "product": []}},
                {"scene": 3, "start": 4.07, "end": 5.97, "grid": {"person": [1, 2, 4, 5, 7, 8], "background": [3, 6], "text": [9], "product": []}},
                {"scene": 4, "start": 5.97, "end": 8.04, "grid": {"person": [2, 5, 7, 8], "background": [1, 3, 4, 6], "text": [8, 9], "product": []}},
                {"scene": 5, "start": 8.04, "end": 8.88, "grid": {"person": [1, 4, 7], "background": [2, 3], "text": [8, 9], "product": [5, 6]}},
                {"scene": 6, "start": 8.88, "end": 10.81, "grid": {"person": [4, 7], "background": [1, 2], "text": [8, 9], "product": [3, 5, 6]}},
                {"scene": 7, "start": 10.81, "end": 11.58, "grid": {"person": [2, 5, 8], "background": [1, 3, 4, 6, 7], "text": [9], "product": [8]}},
                {"scene": 8, "start": 11.58, "end": 12.58, "grid": {"person": [1, 2, 4, 7], "background": [3], "text": [8, 9], "product": [5, 6]}},
                {"scene": 9, "start": 12.58, "end": 14.28, "grid": {"person": [2], "background": [1, 3, 4], "text": [7, 8, 9], "product": [5, 6]}},
                {"scene": 10, "start": 14.28, "end": 17.08, "grid": {"person": [6], "background": [1, 2, 3, 4, 5], "text": [7, 8, 9], "product": []}},
                {"scene": 11, "start": 17.08, "end": 17.85, "grid": {"person": [2, 5, 8], "background": [1, 3, 4, 6, 7, 9], "text": [], "product": []}},
                {"scene": 12, "start": 17.85, "end": 20.72, "grid": {"person": [2, 5, 8], "background": [1, 3, 4, 6, 7, 9], "text": [], "product": []}},
                {"scene": 13, "start": 20.72, "end": 23.32, "grid": {"person": [5], "background": [1, 2, 3, 4, 6, 7, 8, 9], "text": [], "product": []}},
                {"scene": 14, "start": 25.79, "end": 30.02, "grid": {"person": [], "background": [1, 2, 3, 4, 6, 7, 8, 9], "text": [5], "product": []}},
            ]
        }
    }
}


def seed():
    db = SessionLocal()
    try:
        existing = db.query(Ad).filter(Ad.id == ad_data["id"]).first()
        if existing:
            existing.scene_data = ad_data["scene_data"]
            db.commit()
            print(f"업데이트 완료: {ad_data['name']}")
        else:
            db.add(Ad(**ad_data))
            db.commit()
            print(f"삽입 완료: {ad_data['name']}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()