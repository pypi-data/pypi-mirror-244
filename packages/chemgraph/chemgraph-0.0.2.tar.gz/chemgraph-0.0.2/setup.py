# mypy: ignore-errors
from setuptools import setup, find_packages

# Read deps
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='chemgraph',
    version='0.0.2',
    description='Chemical data plotting',
    author='Eduardo Bogado',
    author_email='eduardob1999@gmail.com',
    url='https://github.com/eduardob999/chemgraph',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'chemgraph=chemgraph.plot_module:plot_from_csv',
        ],
    },
)
