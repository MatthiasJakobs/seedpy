from hashlib import md5
from typing  import Union

try:
    from numpy.random import RandomState
except ImportError as e:
    RandomState = e


#
# classes for "with" statements
#

class fixedseed:

    def __init__(self, to_randomize, seed=0):
        if not isinstance(to_randomize, list):
            to_randomize = [to_randomize]

        self.to_randomize = to_randomize

        # Seed set during `with` context
        self.context_seed = seed
        #self.random = self.numpy_object.random.RandomState(seed)

    def __enter__(self):
        self.old_states = []
        for lib in self.to_randomize:
            if lib.__name__ == "numpy":
                self.old_states.append(lib.random.get_state())
                lib.random.seed(self.context_seed)
            elif lib.__name__ == "torch":
                if self.context_seed is not None:
                    self.old_states.append(lib.get_rng_state())
                    lib.manual_seed(self.context_seed)
            else:
                raise NotImplementedError("Library {} not currently implemented".format(lib.__name__))

        #self.old_seed = self.numpy_object.random.get_state()
        #self.numpy_object.random.seed(self.context_seed)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        #self.numpy_object.random.set_state(self.old_seed)
        for old_state, lib in zip(self.old_states, self.to_randomize):
            if lib.__name__ == "numpy":
                lib.random.set_state(old_state)
            elif lib.__name__ == "torch":
                if self.context_seed is not None:
                    lib.set_rng_state(old_state)


class randomseed(fixedseed):

    def __init__(self, to_randomize):
        return super().__init__(to_randomize, seed=None)


#
# methods for seed conversion
#

SeedLike = Union[str, int]


def to_int_seed(seed: SeedLike) -> int:
    """Convert seed-like object (int or string) to integer seed.

    Args:
        seed (SeedLike): Seed-like object to convert.

    Returns:
        int: Integer seed.
    """
    try:
        seed_ = int(seed)
    except ValueError:
        # use hash digest when seed is a (non-numerical) string
        seed_ = int(md5(seed.encode('utf-8')).hexdigest(), 16) & 0xffffffff
    return seed_


def get_random_state(state: Union[SeedLike, RandomState]=None) -> RandomState:
    """Get a Numpy RandomState from a seed-like object or an existing RandomState,
    which is particularly useful for offering flexible function arguments for
    reproducibility.

    Args:
        state (Union[SeedLike, np.random.RandomState], optional): Input seed or RandomState. If this is None (default), a random seed is used.

    Raises:
        ImportError: If Numpy is not installed.

    Returns:
        np.random.RandomState: RandomState object with given seed, or, if the input was a RandomState object, that unaltered RandomState object.
    """
    # check if RandomState was successfully imported
    if isinstance(RandomState, ImportError):
        raise RandomState

    if isinstance(state, RandomState):
        return state
    if state is None:
        return RandomState()

    seed = to_int_seed(state)
    return RandomState(seed)


class generate_seeds:
    """Iterator that generates integer random seeds between 0 and (2**32)-1
    """

    def __init__(self, state: Union[SeedLike, RandomState]=None):
        """Create integer seed generator.

        Args:
            state (Union[SeedLike, np.random.RandomState], optional): Seed or RandomState for reproducing the same sequence of seeds. Defaults to None, which uses a random seed.
        """
        self.__state = get_random_state(state)

    def __iter__(self):
        return self

    def __next__(self):
        return self.__state.randint(1 << 32)
