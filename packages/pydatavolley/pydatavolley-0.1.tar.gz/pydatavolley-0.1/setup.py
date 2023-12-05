from setuptools import setup, find_packages

setup(
    name='pydatavolley',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.23.3',
        'pandas>=1.5.0',
    ],
)