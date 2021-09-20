from typing import Union
import numpy as np


def check_type_ecg(ecg_signal: Union[list, np.ndarray]) -> np.ndarray:
    """Checks the type of the ECG and transforms it in np.ndarry if necessary.

    Parameters
    ----------
    ecg_signal : Union[list, np.ndarray]
        Input ECG signal

    Returns
    -------
    ecg_signal : np.ndarray
        ECG signal in proper np.ndarray format
    """
    try:
        assert isinstance(ecg_signal, np.ndarray)
    except AssertionError:
        if isinstance(ecg_signal, list):
            ecg_signal = np.array(ecg_signal)
        else:
            print('Please input a list or a numpy array')
            exit(1)

    try:
        assert len(ecg_signal.shape) == 1
    except AssertionError:
        print('Please input an ecg_signal with shape (1, ) ')
        exit(1)

    return ecg_signal
