import numpy as np


def sSQI(ecg_signal: list) -> float:
    num = np.mean((ecg_signal - np.mean(ecg_signal))**3)
    s_sqi = num / (np.std(ecg_signal, ddof=1)**3)
    s_sqi_score = float(round(s_sqi, 2))

    return s_sqi_score


def kSQI(ecg_signal: list) -> float:
    num = np.mean((ecg_signal - np.mean(ecg_signal))**4)
    k_sqi = num / (np.std(ecg_signal, ddof=1)**4)
    k_sqi_fischer = k_sqi - 3.0
    k_sqi_score = float(round(k_sqi_fischer, 2))

    return k_sqi_score
