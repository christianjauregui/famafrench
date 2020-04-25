"""
# This file is part of famafrench
# Copyright 2020, Christian Jauregui <chris.jauregui@berkeley.edu>
# See file LICENSE.txt for license information.

Filename
________
`docs/setup.py`

Note
_____
setuptools-based setup module:
* see https://packaging.python.org/guides/distributing-packages-using-setuptools/
* see https://setuptools.readthedocs.io/en/latest/setuptools.html

Note
_____
For more information on licenses, go to https://choosealicense.com/licenses/
"""
from setuptools import setup

# Define __version__
exec(open("famafrench/version.py").read())

NAME = 'famafrench'

packages = ['famafrench']

REQUIRES = [
    'IPython >= 7.12.0',
    'numpy >= 1.16.1',
    'numpydoc >=0.9.2',
    'numba >= 0.48.0',
    'methodtools >= 0.1.0',
    'pandas >= 0.24.2',
    'pandas_datareader >= 0.7.0',
    'pandas_market_calendars >= 1.1',
    'python_dateutil >= 2.8.1',
    'python_dotenv >= 0.13.0',
    'sqlalchemy >= 1.3.13',
    'sphinx >= 2.0',
    'termcolor >= 1.1.0',
    'tqdm >= 4.41.1',
    'wrds >= 3.0.8'
]

setup(
    # Package meta-data
    name=NAME,
    version= __version__,
    author='Christian Jauregui',
    author_email='chris.jauregui@berkeley.edu',
    description='docs/setup.py',
    long_description='',
    long_description_content_type='text/markdown',
    url='https://https://github.com/christianjauregui/famafrench',
    license='Apache License 2.0',

    # Requirements
    packages=packages,
    install_requires=REQUIRES,
    )