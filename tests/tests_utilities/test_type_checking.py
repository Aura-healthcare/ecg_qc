from ecg_qc.utilities.type_checking import check_type_ecg
import pytest
import pandas as pd
import numpy as np


time_window = 9
fs = 1000

ecg_signal = pd.read_csv('tests/tests_datasets/ecg_record_sample.csv')
ecg_signal = ecg_signal.iloc[:time_window * fs]['ecg_record'].values


def test_test_type_ecg():

    with pytest.raises(SystemExit):
        wrong_ecg_signal_type = (4, 8, 15, 16, 42)
        check_type_ecg(wrong_ecg_signal_type)

    with pytest.raises(SystemExit):
        wrong_ecg_signal_size = [[10, 2, 3], [4, 9, 15]]
        check_type_ecg(wrong_ecg_signal_size)


def test_ecg_signal_input_format(ecg_signal=ecg_signal):

    assert isinstance(check_type_ecg(list(ecg_signal)), np.ndarray)
    assert isinstance(check_type_ecg(ecg_signal), np.ndarray)
