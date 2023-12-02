# setup.py
from setuptools import setup

setup(
    name='async_pyarrow',
    version='0.2.0',
    packages=['async_pyarrow'],
    install_requires=[
      'pyarrow', 'grpcio', 'protobuf'
    ],
)
