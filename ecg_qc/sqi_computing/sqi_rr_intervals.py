import numpy as np
from ecgdetectors import Detectors
import biosppy.signals.ecg as bsp_ecg


def cSQI(ecg_signal: list, sampling_frequency: int) -> float:

    RRI_list = bsp_ecg.hamilton_segmenter(
            signal=np.array(ecg_signal),
            sampling_rate=sampling_frequency)[0]

    cSQI_score = float(round(np.std(RRI_list, ddof=1) / np.mean(RRI_list), 2))

    return cSQI_score


def qSQI(ecg_signal: list, sampling_frequency: int) -> float:

    detectors = Detectors(sampling_frequency)
    qrs_frames_swt = detectors.swt_detector(ecg_signal)
    qrs_frames_hamilton = bsp_ecg.hamilton_segmenter(
            signal=np.array(ecg_signal),
            sampling_rate=sampling_frequency)[0]

    qSQI_score = compute_qrs_frames_correlation(qrs_frames_hamilton,
                                                qrs_frames_swt,
                                                sampling_frequency)

    return qSQI_score


def compute_qrs_frames_correlation(qrs_frames_1,
                                   qrs_frames_2,
                                   sampling_frequency,
                                   MATCHING_QRS_FRAMES_TOLERANCE=50,
                                   MAX_SINGLE_BEAT_DURATION=1800):

    single_frame_duration = 1/sampling_frequency

    frame_tolerance = MATCHING_QRS_FRAMES_TOLERANCE * (
        0.001 / single_frame_duration)
    max_single_beat_frame_duration = MAX_SINGLE_BEAT_DURATION * (
        0.001 / single_frame_duration)

    # Catch complete failed QRS detection
    if (len(qrs_frames_1) == 0 or len(qrs_frames_2) == 0):
        return 0

    i = 0
    j = 0
    matching_frames = 0

    previous_min_qrs_frame = min(qrs_frames_1[0], qrs_frames_2[0])
    missing_beats_frames_count = 0

    while i < len(qrs_frames_1) and j < len(qrs_frames_2):
        min_qrs_frame = min(qrs_frames_1[i], qrs_frames_2[j])
        # Get missing detected beats intervals
        if (min_qrs_frame - previous_min_qrs_frame) > (
                max_single_beat_frame_duration):
            missing_beats_frames_count += (min_qrs_frame -
                                           previous_min_qrs_frame)

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
        previous_min_qrs_frame = min_qrs_frame

    correlation_coefs = 2 * matching_frames / (len(qrs_frames_1) +
                                               len(qrs_frames_2))

    correlation_coefs = round(correlation_coefs, 2)

    return correlation_coefs
