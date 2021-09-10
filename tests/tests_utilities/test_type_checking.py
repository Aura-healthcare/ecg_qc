from ecg_qc.utilities.type_checking import check_type_ecg 
import pytest


def test_test_type_ecg():

    with pytest.raises(SystemExit):
        wrong_ecg_signal_type = (4, 8, 15, 16, 42)
        check_type_ecg(wrong_ecg_signal_type)

    with pytest.raises(SystemExit):
        wrong_ecg_signal_size = [[10, 2, 3], [4, 9, 15]]
        check_type_ecg(wrong_ecg_signal_size)
