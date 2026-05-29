from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.session_store import session_store
from app.core.config import USE_SIMULATE, MUSE_SERIAL
from app.services.eeg.collector import get_board
from app.services.eeg.processor import apply_bandpass_filter, extract_band_powers, compute_indices
from app.services.eeg.formatter import format_eeg_result
from app.services.sync.synchronizer import synchronize
from app.database.repository import create_session, update_session_eeg
from brainflow.board_shim import BoardShim
import time

router = APIRouter()


class SessionStartRequest(BaseModel):
    ad_id: str


class SessionStopRequest(BaseModel):
    ad_id: str


@router.post("/session/start")
def start_session(body: SessionStartRequest, db: Session = Depends(get_db)):
    try:
        board_shim, board_id = get_board(
            serial_number=MUSE_SERIAL,
            simulate=USE_SIMULATE
        )
        sampling_rate = board_shim.get_sampling_rate(board_id)

        board_shim.prepare_session()
        board_shim.start_stream()

        session_store.set_board(board_shim, board_id, sampling_rate)

        create_session(db, ad_id=body.ad_id, start_time=time.time())

        return {"message": "세션 시작", "ad_id": body.ad_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/session/stop")
def stop_session(body: SessionStopRequest, db: Session = Depends(get_db)):
    try:
        board_shim = session_store.board_shim
        board_id = session_store.board_id
        sampling_rate = session_store.sampling_rate

        if not board_shim:
            raise HTTPException(status_code=400, detail="세션이 시작되지 않았습니다.")

        data = board_shim.get_board_data()
        board_shim.stop_stream()
        board_shim.release_session()

        filtered = apply_bandpass_filter(data, sampling_rate)
        band_powers = extract_band_powers(filtered, sampling_rate)
        indices = compute_indices(band_powers)
        eeg_result = format_eeg_result(data, band_powers, indices, board_id)

        gaze_data = session_store.get_gaze(body.ad_id)
        timestamp_channel = BoardShim.get_timestamp_channel(board_id)
        eeg_timestamps = data[timestamp_channel]
        synced_frames = synchronize(gaze_data, data, eeg_timestamps, indices) if gaze_data else []

        update_session_eeg(db, body.ad_id, eeg_result["eeg"], synced_frames)

        session_store.save_eeg(body.ad_id, data, sampling_rate, board_id)
        session_store.clear_board()

        return {"message": "세션 종료", "ad_id": body.ad_id}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))