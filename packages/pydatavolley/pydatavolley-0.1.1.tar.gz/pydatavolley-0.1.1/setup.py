from setuptools import setup, find_packages
from __init__ import __version__

setup(
    name='pydatavolley',
    version=__version__,
    packages=find_packages(),
    install_requires=[
        'numpy>=1.23.3',
        'pandas>=1.5.0',
    ],
)
