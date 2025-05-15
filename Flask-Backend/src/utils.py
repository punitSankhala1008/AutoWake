# src/utils.py

import numpy as np
from scipy.spatial import distance as dist

def eye_aspect_ratio(eye):
    # eye: list of 6 (x,y) tuples for one eye
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])
    return (A + B) / (2.0 * C)

def mouth_aspect_ratio(mouth):
    # mouth: list of 8 (x,y) tuples for mouth landmarks
    A = dist.euclidean(mouth[13], mouth[19])  # inner lip vertical
    B = dist.euclidean(mouth[14], mouth[18])
    C = dist.euclidean(mouth[12], mouth[16])  # inner lip horizontal
    return (A + B) / (2.0 * C)
