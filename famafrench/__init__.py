"""
This file is part of famafrench.
Copyright (c) 2020, Christian Jauregui <chris.jauregui@berkeley.edu>
See file LICENSE.txt for license information.

Filename
_________
`famafrench/__init__.py`

Note
____
Python package designed to construct and replicate datasets from Ken French's online library
(https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) via remote access to wrds-cloud.
============================================================================================================

Modules
________
`wrdsconnect.py` : Establishes remote connection to CRSP, Compustat Fundamentals, and other datafiles in wrds-cloud
                   by incorporating code from the `WRDS-Py` library package. The major change involves
                   getting environment variables with user- and account-specific WRDS credentials
                   for securely accessing wrds-cloud datafiles.

`famafrench.py` : Construct and replicate Fama/French style datasets found in Ken French's online data library.

`utils.py` : Utility/Auxiliary functions and routines used in module`famafrench.py`
"""
from famafrench.version import __version__ as version
__version__ = version
__title__ = 'famafrench-py'
__author__ = 'Christian Jauregui <chris.jauregui@berkeley.edu'

# Bring to to-level namespace
from .famafrench import FamaFrench, Error  # this is used to build sphinx-documentation

