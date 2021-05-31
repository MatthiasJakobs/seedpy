import numpy as np
import torch

from seedpy import fixedseed

np_fix_10100 = np.array([0.27896153, 0.0217155, 0.49127331, 0.24049215, 0.73577514])
torch_fix_10100 = np.array([0.4141509, 0.63924634, 0.55916786, 0.3014046, 0.7659669])

def test_with_fixseed_numpy_basic():

    np.random.seed(0)
    before_fixedseed = np.random.rand(5)

    with fixedseed(np, seed=10100):
        inside_fixedseed = np.random.rand(5)

    after_fixedseed_1 = np.random.rand(5)

    # Check whether the desired number was generated
    assert np.all(np.isclose(inside_fixedseed, np_fix_10100))

def test_with_fixseed_numpy_correct_reset():

    with fixedseed(np, seed=10100):
        inside_fixedseed = np.random.rand(5)

    after_fixedseed_1 = np.random.rand(5)

    with fixedseed(np, seed=10100):
        inside_fixedseed = np.random.rand(5)

    after_fixedseed_2 = np.random.rand(5)

    # Check whether the seed was returned correctly
    # If both numbers are identical then the seed stayed like it is
    assert np.all(after_fixedseed_1 != after_fixedseed_2)

