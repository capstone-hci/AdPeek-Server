from typing import Optional
from time import sleep
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds


def get_board(serial_number: Optional[str] = None, simulate: bool = False):
    """
    Muse 2 보드 연결 설정
    - simulate: True면 시뮬레이터 모드
    - serial_number: 실제 기기 연결 시 시리얼 넘버 (예: "Muse-0465")
    """
    params = BrainFlowInputParams()

    if simulate:
        board_id = BoardIds.SYNTHETIC_BOARD
    else:
        board_id = BoardIds.MUSE_2_BOARD
        if serial_number:
            params.serial_number = serial_number

    return BoardShim(board_id, params), board_id


def collect_eeg(board_shim: BoardShim, board_id: int, duration_sec: int = 10):
    """
    EEG 데이터 수집
    - duration_sec: 수집할 시간 (초)
    """
    sampling_rate = BoardShim.get_sampling_rate(board_id)
    num_points = duration_sec * sampling_rate

    board_shim.prepare_session()
    board_shim.start_stream()

    sleep(duration_sec + 1)  # 1초 여유

    data = board_shim.get_current_board_data(num_points)

    board_shim.stop_stream()
    board_shim.release_session()

    return data, sampling_rate