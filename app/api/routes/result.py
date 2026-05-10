from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/result/{ad_id}")
def get_result(ad_id: str):
    try:
        # 추후 실제 분석 결과 반환 로직 연결 예정
        return {
            "ad_id": ad_id,
            "message": "분석 결과 조회 준비 중",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))