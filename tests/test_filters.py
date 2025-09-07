import numpy as np
from src.ads_maf.filters import moving_average
import pytest

def test_window_one_is_identity():
    x = np.random.randn(200)
    y = moving_average(x, 1)
    assert np.allclose(x, y)

def test_constant_signal_stays_constant():
    x = np.ones(100) * 3.14
    y = moving_average(x, 7)
    assert np.allclose(y, x)

def test_raises_on_bad_window():
    with pytest.raises(ValueError):
        moving_average(np.arange(10), 0)