from . import fixedseed  as fixedseed_
from . import randomseed as randomseed_


def fixedseed(*args, **kwargs):
    def f1(func):
        def f2(*args2, **kwargs2):
            with fixedseed_(*args, **kwargs):
                func(*args2, **kwargs2)
        return f2
    return f1

def randomseed(*args, **kwargs):
    def f1(func):
        def f2(*args2, **kwargs2):
            with randomseed_(*args, **kwargs):
                func(*args2, **kwargs2)
        return f2
    return f1
