
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

