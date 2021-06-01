# seedpy
Easily seed frameworks used for machine learning like Numpy and PyTorch using context managers.

# Disclaimer
This is almost entirely untested software (especially the torch part). Use at your own risk.
If you have feature suggestions, found bugs, or want to contribute, feel free to open up issues and / or pull-requests.

# Installation
`pip install git+https://github.com/MatthiasJakobs/seedpy.git`

# Usage
Use `fixedseed` to fix the seed of the global Numpy inside the context manager:

```python
np.random.seed(0)

# Number generated using seed "0"
before_fixedseed = np.random.rand(5)

with fixedseed(np, seed=10100):
    # Number generated using seed "10100"
    inside_fixedseed = np.random.rand(5)

# Number generated using seed "0"
after_fixedseed = np.random.rand(5)
```

You can also pass in the `torch` global object, or even a list of both: 
```python
with fixedseed([torch, np], seed=10100):
    ...
```

The same syntax can be used for the `randomseed` context in order to randomize calculations inside an otherwise fixed environment:
```python
with randomseed([torch, np]):
    ...
```
