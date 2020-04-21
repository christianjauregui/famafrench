"""
`setup.py`

setuptools-based setup module: (see https://packaging.python.org/guides/distributing-packages-using-setuptools/)
For more information on licenses, go to https://choosealicense.com/licenses/
"""
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

NAME = 'famafrench'

packages = [
    'famafrench'
]

requires = [
    'numpy >= 1.16.1',
    'numpydoc >=0.9.2'
    'numba >= 0.48.0',
    'methodtools >= 0.1.0',
    'pandas >= 0.24.2',
    'pandas_datareader >= 0.7.0',
    'pandas_market_calendars >= 1.1',
    'termcolor >= 1.1.0',
    'tqdm >= 4.41.1'
]

setup(
    # Package meta-data
    name=NAME,
    version='0.1.0',
    author='Christian Jauregui',
    author_email='cjauregui@econ.berkeley.edu',
    description='Python package designed to construct and replicate datasets from Ken French\'s '
                'online library (https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) '
                'via remote access to wrds-cloud. ',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://https://github.com/christianjauregui/famafrench',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment',
        "Topic :: Scientific/Engineering"
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],

    # What does your project relate to?
    keywords=[
        'alpha',
        'alpha-factors',
        'beta',
        'capm',
        'econometrics',
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
                                    'examples',
                                    'tests*',
                                    '*txt',
                                    '*md',
                                    '*rst']),
    install_requires=requires,
    python_requires='>=3.4.0',
    tests_require=['pytest'],
    test_suite="tests"
    )