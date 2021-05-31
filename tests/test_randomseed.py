import numpy as np
import torch

from seedpy import randomseed

np_fix_10100 = np.array([0.27896153, 0.0217155, 0.49127331, 0.24049215, 0.73577514])
torch_fix_10100 = np.array([0.4141509, 0.63924634, 0.55916786, 0.3014046, 0.7659669])

def test_with_randomseed_numpy_basic():

    np.random.seed(0)
    before_randomseed_1 = np.random.rand(5)

    with randomseed(np):
        inside_randomseed_1 = np.random.rand(5)

    after_randomseed_1 = np.random.rand(5)

    np.random.seed(0)
    before_randomseed_2 = np.random.rand(5)

    with randomseed(np):
        inside_randomseed_2 = np.random.rand(5)

    after_randomseed_2 = np.random.rand(5)

    # Check whether before and after coincide, but inside does not
    assert np.all(before_randomseed_1 == before_randomseed_2)
    assert np.all(after_randomseed_1 == after_randomseed_2)
    assert np.all(inside_randomseed_1 != inside_randomseed_2)

def test_with_randomseed_numpy_correct_reset():

    with randomseed(np):
        inside_randomseed = np.random.rand(5)

    after_randomseed_1 = np.random.rand(5)

    with randomseed(np):
        inside_randomseed = np.random.rand(5)

    after_randomseed_2 = np.random.rand(5)

    # Check whether the seed was returned correctly
    # If both numbers are identical then the seed stayed like it is
    assert np.all(after_randomseed_1 != after_randomseed_2)


'''
print("Fixed seed")
print(np.random.rand(5))

with fixedseed(seed=10100):
    print(np.random.rand(5))

print(np.random.rand(5))

print("Randomize only in with-statement")

np.random.seed(0)
print(np.random.rand(5))

with randomseed():
    print(np.random.rand(5))

print(np.random.rand(5))
'''
