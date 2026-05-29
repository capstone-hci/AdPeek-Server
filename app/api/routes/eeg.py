from fastapi import APIRouter
from app.core.session_store import session_store
from app.core.config import USE_SIMULATE, MUSE_SERIAL
from app.services.eeg.collector import connect_board
from brainflow.board_shim import BoardShim

router = APIRouter()


@router.get("/eeg/connect")
def connect_eeg():
    try:
        if session_store.board_shim:
            return {
                "connected": True,
                "message": "이미 연결됨",
            }

        board_shim, board_id = connect_board(
            serial_number=MUSE_SERIAL,
            simulate=USE_SIMULATE
        )
        sampling_rate = BoardShim.get_sampling_rate(board_id)
        session_store.set_board(board_shim, board_id, sampling_rate)

        return {
            "connected": True,
            "message": "연결 성공",
        }

    except Exception as e:
        return {
            "connected": False,
            "message": f"연결 실패: {str(e)}",
        }