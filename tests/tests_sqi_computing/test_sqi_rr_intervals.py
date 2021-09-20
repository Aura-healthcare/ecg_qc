import pandas as pd
import numpy as np
from ecg_qc.sqi_computing.sqi_rr_intervals import (
    csqi,
    qsqi,
    compute_qrs_frames_correlation)
from ecgdetectors import Detectors
import biosppy.signals.ecg as bsp_ecg


time_window = 9
fs = 1000

ecg_signal = pd.read_csv('tests/tests_datasets/ecg_record_sample.csv')
ecg_signal = ecg_signal.iloc[:time_window * fs]['ecg_record'].values
ecg_signal_nan = [0, 0, 0]

qrs_frames_none = []


def test_qsqi(ecg_signal=ecg_signal, fs=fs):

    q_sqi_score = qsqi(ecg_signal, fs)

    assert isinstance(q_sqi_score, float)


def test_csqi(ecg_signal=ecg_signal, fs=fs):

    c_sqi_score = csqi(ecg_signal, fs)

    assert isinstance(c_sqi_score, float)


def test_csqi_nan(ecg_signal=ecg_signal_nan, fs=fs):

    c_sqi_score = csqi(ecg_signal, fs)
    assert c_sqi_score == 0


def test_compute_qrs_frames_correlation(ecg_signal=ecg_signal,
                                        qrs_frames_none=qrs_frames_none,
                                        fs=fs):
    detectors = Detectors(fs)
    qrs_frames_swt = detectors.swt_detector(ecg_signal)
    qrs_frames_hamilton = bsp_ecg.hamilton_segmenter(
            signal=np.array(ecg_signal),
            sampling_rate=fs)[0]

    correlation_coefs = compute_qrs_frames_correlation(
        qrs_frames_1=qrs_frames_swt,
        qrs_frames_2=qrs_frames_hamilton,
        sampling_frequency=fs)

    assert isinstance(correlation_coefs, float)

    # test for qrs without length

    correlation_coefs_none_1 = compute_qrs_frames_correlation(
        qrs_frames_1=qrs_frames_none,
        qrs_frames_2=qrs_frames_hamilton,
        sampling_frequency=fs)

    assert correlation_coefs_none_1 == 0

    correlation_coefs_none_2 = compute_qrs_frames_correlation(
        qrs_frames_1=qrs_frames_swt,
        qrs_frames_2=qrs_frames_none,
        sampling_frequency=fs)

    assert correlation_coefs_none_2 == 0
