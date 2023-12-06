# setup.py
from setuptools import setup, find_packages

setup(
    name='ewire',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        'Flask',
    ],
)
