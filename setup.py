"""
This file is part of famafrench.
Copyright (c) 2020, Christian Jauregui <chris.jauregui@berkeley.edu>
See file LICENSE.txt for license information.

Filename
________
`setup.py`

Note
_____
setuptools-based setup module:
* see https://packaging.python.org/guides/distributing-packages-using-setuptools/
* see https://setuptools.readthedocs.io/en/latest/setuptools.html

Note
_____
For more information on licenses, go to https://choosealicense.com/licenses/
"""
from os import path
from setuptools import setup, find_packages

# Define __version__
exec(open("famafrench/version.py").read())

if '__version__' in locals():
    VERSION = __version__
else:
    VERSION = '0.1.3'

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), "r") as readme:
    long_description = readme.read()

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
    version=VERSION,
    author='Christian Jauregui',
    author_email='chris.jauregui@berkeley.edu',
    description='Python package designed to construct and replicate datasets from Ken French\'s '
                'online library (https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) '
                'via remote access to wrds-cloud. ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/christianjauregui/famafrench',
    license='Apache License 2.0',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    # See https://packaging.python.org/tutorials/packaging-projects/#classifiers
    # https://www.python.org/dev/peps/pep-0440/
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment',
        "Topic :: Scientific/Engineering",
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],

    # What does your project relate to?
    keywords=[
        'alpha',
        'alpha-factors',
        'beta',
        'capm',
        'econometrics',
        'equities',
        'equity-returns',
        'expected-returns'
        'factor-investing',
        'factor-model',
        'factor-returns',
        'fama-french',
        'finance',
        'growth',
        'investment',
        'momentum',
        'portfolio',
        'risk-model',
        'securities',
        'stock-returns',
        'value',
    ],

    project_urls={
        'Documentation': 'https://christianjauregui.github.io/famafrench/',
        'Source': 'https://github.com/christianjauregui/famafrench',
        'Tracker': 'https://github.com/christianjauregui/famafrench/issues',
    },

    # Requirements
    packages=find_packages(exclude=['contrib',
                                    'docs',
                                    'tests*',
                                    '*txt',
                                    '*md',
                                    '*rst']),
    install_requires=REQUIRES,
    include_package_data=True,
    python_requires='>=3.4.0',
    tests_require=['pytest'],
    test_suite="tests"
    )