import numpy as np
from ecgdetectors import Detectors
import biosppy.signals.ecg as bsp_ecg


def csqi(ecg_signal: list, sampling_frequency: int) -> float:
    """Variability in the R-R Interval

    When an artifact is present, the QRS detector underperforms by either
    missing R-peaks or erroneously identifying noisy peaks as R- peaks. The
    above two problems will lead to a high degree of variability in the
    distribution of R-R intervals;

    Parameters
    ----------
    ecg_signal : list
        Input ECG signal
    sampling_frequency : list
        Input ecg sampling frequency

    Returns
    -------
    c_sqi_score : float

    """
    with np.errstate(invalid='raise'):

        try:

            rri_list = bsp_ecg.hamilton_segmenter(
                    signal=np.array(ecg_signal),
                    sampling_rate=sampling_frequency)[0]

            c_sqi_score = float(np.round(
                np.std(rri_list, ddof=1) / np.mean(rri_list),
                3))

        except Exception:
            c_sqi_score = 0

        return c_sqi_score


def qsqi(ecg_signal: list, sampling_frequency: int) -> float:
    """Matching Degree of R Peak Detection

    Two R wave detection algorithms are compared with their respective number
    of R waves detected.

    * Hamilton
    * SWT (Stationary Wavelet Transform)

    Parameters
    ----------
    ecg_signal : list
        Input ECG signal
    sampling_frequency : list
        Input ecg sampling frequency

    Returns
    -------
    q_sqi_score : float

    """
    detectors = Detectors(sampling_frequency)
    qrs_frames_swt = detectors.swt_detector(ecg_signal)
    qrs_frames_hamilton = bsp_ecg.hamilton_segmenter(
            signal=np.array(ecg_signal),
            sampling_rate=sampling_frequency)[0]

    q_sqi_score = compute_qrs_frames_correlation(qrs_frames_hamilton,
                                                 qrs_frames_swt,
                                                 sampling_frequency)

    return q_sqi_score


def compute_qrs_frames_correlation(qrs_frames_1: list,
                                   qrs_frames_2: list,
                                   sampling_frequency: int,
                                   matching_qrs_frames_tolerance=50) -> float:

    single_frame_duration = 1/sampling_frequency

    frame_tolerance = matching_qrs_frames_tolerance * (
        0.001 / single_frame_duration)

    # Catch complete failed QRS detection
    if (len(qrs_frames_1) == 0 or len(qrs_frames_2) == 0):
        return 0

    i = 0
    j = 0
    matching_frames = 0

    while i < len(qrs_frames_1) and j < len(qrs_frames_2):
        min_qrs_frame = min(qrs_frames_1[i], qrs_frames_2[j])
        # Get missing detected beats intervals

        # Matching frames

        if abs(qrs_frames_2[j] - qrs_frames_1[i]) < frame_tolerance:
            matching_frames += 1
            i += 1
            j += 1
        else:
            # increment first QRS in frame list
            if min_qrs_frame == qrs_frames_1[i]:
                i += 1
            else:
                j += 1

    correlation_coefs = 2 * matching_frames / (len(qrs_frames_1) +
                                               len(qrs_frames_2))

    correlation_coefs = round(correlation_coefs, 3)

    return correlation_coefs
