import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.database import SessionLocal
from app.database.models import Ad

ad_data = {
    "id": "ad_001",
    "name": "건강 깔창 광고",
    "duration": 30.03,
    "scene_data": [
        {"scene": 1, "start": 0.00, "end": 1.67, "description": "숲 배경, 등산객 뒷모습"},
        {"scene": 2, "start": 1.67, "end": 4.07, "description": "남성 얼굴 클로즈업, 목 디스크/어깨 통증 텍스트"},
        {"scene": 3, "start": 4.07, "end": 5.97, "description": "무릎 잡는 손·다리, 무릎 통증 텍스트"},
        {"scene": 4, "start": 5.97, "end": 8.04, "description": "허리 숙인 남성, 제품 설명 자막"},
        {"scene": 5, "start": 8.04, "end": 8.88, "description": "남성 얼굴, 신발 클로즈업, 깔창 꺼내는 손"},
        {"scene": 6, "start": 8.88, "end": 10.81, "description": "깔창 손에 들고 있는 장면, 신발 본체"},
        {"scene": 7, "start": 10.81, "end": 11.58, "description": "청년 신발 끈 묶는 모습"},
        {"scene": 8, "start": 11.58, "end": 12.58, "description": "신발 끈 묶는 손 클로즈업, 운동화 클로즈업"},
        {"scene": 9, "start": 12.58, "end": 14.28, "description": "걷는 발·운동화, 제품 효능 자막"},
        {"scene": 10, "start": 14.28, "end": 17.08, "description": "가을 단풍 숲 드론뷰, 제품 효능 자막"},
        {"scene": 11, "start": 17.08, "end": 17.85, "description": "젊은 여성 얼굴 (웃는 표정)"},
        {"scene": 12, "start": 17.85, "end": 18.92, "description": "중년 남성 얼굴 (웃는 표정)"},
        {"scene": 13, "start": 18.92, "end": 19.19, "description": "핑크빛 화면전환 효과"},
        {"scene": 14, "start": 19.19, "end": 20.72, "description": "남성 얼굴·상반신 정면"},
        {"scene": 15, "start": 20.72, "end": 30.03, "description": "하늘·산 능선, 강 전경, 제로였던 내 삶에 새로운 활력이 찾아왔다 자막"},
    ]
}

def seed():
    db = SessionLocal()
    try:
        existing = db.query(Ad).filter(Ad.id == ad_data["id"]).first()
        if existing:
            print(f"이미 존재함: {ad_data['id']}")
            return
        db.add(Ad(**ad_data))
        db.commit()
        print(f"삽입 완료: {ad_data['name']}")
    finally:
        db.close()

if __name__ == "__main__":
    seed()