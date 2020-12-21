import wfdb
import sys
from pathlib import Path
sys.path.append(str(Path(sys.path[0]).parent))
from ecg_qc.ecg_qc import ecg_qc


def main():

	ecg_path = 'datasets/0_physionet_ecg/103001_ECG'
	sampling_frequency = 1000
	window_size_sec = 10
	window_size_sample = window_size_sec * sampling_frequency

	offset_start = 	58686000
	offset_stop = offset_start + window_size_sample

	ecg_record = wfdb.rdrecord(ecg_path)
	last_sample = len(ecg_record.p_signal[:, 0])
	SQI_class = ecg_qc()

	for offset in list(range(offset_start, last_sample, window_size_sample)):

		ecg_data = ecg_record.p_signal[offset : offset + window_size_sample, 0]
		print(SQI_class.get_signal_quality(ecg_data, sampling_frequency))

main()
