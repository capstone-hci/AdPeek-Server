from typing import Optional
from time import sleep
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds


def get_board(serial_number: Optional[str] = None, simulate: bool = False):
    params = BrainFlowInputParams()

    if simulate:
        board_id = BoardIds.SYNTHETIC_BOARD
    else:
        board_id = BoardIds.MUSE_2_BOARD
        if serial_number:
            params.serial_number = serial_number

    return BoardShim(board_id, params), board_id


def connect_board(serial_number: Optional[str] = None, simulate: bool = False):
    board_shim, board_id = get_board(serial_number, simulate)
    board_shim.prepare_session()
    return board_shim, board_id


def start_stream(board_shim: BoardShim):
    board_shim.start_stream()


def collect_eeg(board_shim: BoardShim, board_id: int, duration_sec: int = 10):
    sampling_rate = BoardShim.get_sampling_rate(board_id)
    num_points = duration_sec * sampling_rate

    sleep(duration_sec + 1)

    data = board_shim.get_current_board_data(num_points)
    board_shim.stop_stream()
    board_shim.release_session()

    return data, sampling_rate