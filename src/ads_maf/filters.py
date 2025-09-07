from __future__ import annotations
import numpy as np

def moving_average(x: np.ndarray, window: int) -> np.ndarray:
    """
    Centered moving average with edge-value padding.
    - Preserves constant signals exactly.
    - Returns an array the same length as x.
    """
    x = np.asarray(x, dtype=float)
    w = int(window)
    if w <= 0:
        raise ValueError("window must be > 0")
    if x.size == 0 or w == 1:
        return x.copy()

    # For odd w, pads are equal; for even w, right gets one more to keep centering sensible
    pad_left = (w - 1) // 2
    pad_right = w // 2

    # Edge padding avoids zero-padding artifacts at boundaries
    xpad = np.pad(x, (pad_left, pad_right), mode="edge")

    kernel = np.ones(w, dtype=float) / float(w)
    # 'valid' on the padded signal yields same-length output as x
    y = np.convolve(xpad, kernel, mode="valid")
    return y
