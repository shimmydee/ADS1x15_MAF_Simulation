import numpy as np
from src.ads_maf.filters import moving_average
from src.ads_maf.metrics import peak_preservation

def test_peak_preservation_between_0_and_1():
    x = np.zeros(51); x[25] = 10.0  # one peak
    y = moving_average(x, 5)
    r = peak_preservation(x, y)
    assert 0 < r < 1