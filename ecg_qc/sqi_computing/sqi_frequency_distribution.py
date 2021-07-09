import numpy as np


def ssqi(ecg_signal: list) -> float:
    """Computes the skewness sqi.

    Skewness represents how asymetrical a distribution is.

    * Symetrical distribution : skewness = 0
    * Asymetrical distribution skewed on the left : skewness < 0
    * Asymetrical distribution skewed on the right : skewness > 0


    Parameters
    ----------
    ecg_signal : list
        Input ECG signal

    Returns
    -------
    s_sqi_score : float
        rounded skewness sqi score

    """
    num = np.mean((ecg_signal - np.mean(ecg_signal))**3)
    s_sqi = num / (np.std(ecg_signal, ddof=1)**3)
    s_sqi_score = float(round(s_sqi, 3))

    return s_sqi_score


def ksqi(ecg_signal: list) -> float:
    """Computes the excess kurtosis sqi.

    Kurtosis represents how spread a distribution is.

    * Mesokurtic distribution : excess kurtosis = 0
    * Leptokurtic distribution : excess kurtosis > 0
    * Platykurtic distribution : excess kurtosis < 0


    Parameters
    ----------
    ecg_signal : list
        Input ECG signal

    Returns
    -------
    k_sqi_score : float
        rounded excess kurtosis sqi score

    """
    num = np.mean((ecg_signal - np.mean(ecg_signal))**4)
    k_sqi = num / (np.std(ecg_signal, ddof=1)**4)
    k_sqi_fischer = k_sqi - 3.0
    k_sqi_score = float(round(k_sqi_fischer, 3))

    return k_sqi_score
