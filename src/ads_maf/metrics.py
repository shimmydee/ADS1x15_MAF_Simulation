import numpy as np

def peak_preservation(x: np.ndarray, y: np.ndarray) -> float:
    denom = np.max(np.abs(x)) if x.size else 1.0
    return float(np.max(np.abs(y)) / denom) if denom != 0 else 1.0
