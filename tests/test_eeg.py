from app.services.eeg.collector import get_board, collect_eeg
from app.services.eeg.processor import apply_bandpass_filter, extract_band_powers, compute_indices
from app.services.eeg.formatter import format_eeg_result

board_shim, board_id = get_board(simulate=True)
data, sampling_rate = collect_eeg(board_shim, board_id, duration_sec=5)

filtered = apply_bandpass_filter(data, sampling_rate)
band_powers = extract_band_powers(filtered, sampling_rate)
indices = compute_indices(band_powers)
result = format_eeg_result(data, band_powers, indices, board_id)

print(result)