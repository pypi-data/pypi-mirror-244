# mypy: ignore-errors
from setuptools import setup

# Read deps
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='chemgraph',
    version='0.0.1',
    description='Chemical data plotting',
    author='Eduardo Bogado',
    py_modules=['package.plot_from_csv'],
    install_requires=requirements
)
