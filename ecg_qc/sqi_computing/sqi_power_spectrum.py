import numpy as np


def psqi(ecg_signal: list, sampling_frequency: int) -> float:
    """Computes the power spectrum Distribution of QRS Wave.

    It corresponds to the ratio of the energy of the QRS wave and the energy of
    the ECG signal. The energy of the QRS wave is computed on frequencies
    ranging from 5Hz to 15Hz, the energy of the ECG signal is computed on
    frequencies ranging from 5Hz to 40Hz.

    If interference exists, the high-frequency component increases, and pSQI
    decreases.


    Parameters
    ----------
    ecg_signal : list
        Input ECG signal
    sampling_frequency : list
        Input ecg sampling frequency

    Returns
    -------
    p_sqi_score : float

    """
    n = len(ecg_signal)
    t = 1 / sampling_frequency

    yf = np.fft.fft(ecg_signal)
    xf = np.linspace(0.0, 1.0/(2.0*t), n//2)

    pds_num = [np.abs(yf[idx]) for idx in range(len(xf)) if
               xf[idx] >= 5 and xf[idx] <= 15]
    pds_denom = [np.abs(yf[idx]) for idx in range(len(xf)) if
                 xf[idx] >= 5 and xf[idx] <= 40]
    p_sqi_score = float(np.round(sum(pds_num) / sum(pds_denom), 3))

    return p_sqi_score


def bassqi(ecg_signal: list, sampling_frequency: int) -> float:
    """Computes the relative power in the Baseline.

    It corresponds to the ratio of the energy of the QRS wave and the energy of
    the ECG signal. The energy of the baseline is computed on frequencies
    ranging from 0Hz to 1Hz, the energy of the ECG signal is computed on
    frequencies ranging from 0Hz to 40Hz.

    If there is no baseline drift interference, the basSQI value is close to 1.
    An abnormal shift in the baseline causes the bassqi to decrease.


    Parameters
    ----------
    ecg_signal : list
        Input ECG signal
    sampling_frequency : list
        Input ecg sampling frequency

    Returns
    -------
    bas_sqi_score : float

    """
    n = len(ecg_signal)
    t = 1 / sampling_frequency

    yf = np.fft.fft(ecg_signal)
    xf = np.linspace(0.0, 1.0/(2.0*t), n//2)

    pds_num = [np.abs(yf[idx]) for idx in range(len(xf)) if
               xf[idx] >= 0 and xf[idx] <= 1]
    pds_denom = [np.abs(yf[idx]) for idx in range(len(xf)) if
                 xf[idx] >= 0 and xf[idx] <= 40]

    bas_sqi_score = float(np.round(1 - (sum(pds_num) / sum(pds_denom)), 3))

    return bas_sqi_score
