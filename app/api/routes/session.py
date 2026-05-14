from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.session_store import session_store
from app.services.eeg.collector import get_board

router = APIRouter()


class SessionStartRequest(BaseModel):
    ad_id: str


class SessionStopRequest(BaseModel):
    ad_id: str


@router.post("/session/start")
def start_session(body: SessionStartRequest):
    try:
        board_shim, board_id = get_board(simulate=True)
        sampling_rate = board_shim.get_sampling_rate(board_id)

        board_shim.prepare_session()
        board_shim.start_stream()

        session_store.set_board(board_shim, board_id, sampling_rate)

        return {"message": "세션 시작", "ad_id": body.ad_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/stop")
def stop_session(body: SessionStopRequest):
    try:
        board_shim = session_store.board_shim
        board_id = session_store.board_id
        sampling_rate = session_store.sampling_rate

        if not board_shim:
            raise HTTPException(status_code=400, detail="세션이 시작되지 않았습니다.")

        data = board_shim.get_board_data()

        board_shim.stop_stream()
        board_shim.release_session()

        session_store.save_eeg(body.ad_id, data, sampling_rate, board_id)
        session_store.clear_board()

        return {"message": "세션 종료", "ad_id": body.ad_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))