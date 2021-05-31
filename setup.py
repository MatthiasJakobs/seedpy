import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(name='seedpy',
      version='0.1',
      description='Easy seeding for machine learning frameworks',
      long_description=long_description,
      long_description_content_type='text/markdown',
      keywords=['machine learning', 'seed', 'random', 'numpy', 'pytorch'],
      author='Matthias Jakobs',
      author_email='matthias.jakobs@tu-dortmund.de',
      url='https://github.com/MatthiasJakobs/seedpy',
      license='GNU GPLv3',
      packages=setuptools.find_packages(),
      python_requires='>=3.5',
      install_requires=['numpy', 'torch'])
