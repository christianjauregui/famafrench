# `famafrench`

`famafrench` is a Python package designed to replicate and construct datasets from Ken French's 
[online data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) 
via remote access to the [wrds-cloud](https://wrds-www.wharton.upenn.edu/pages/support/getting-started/3-ways-use-wrds/#the-wrds-cloud)
by querying [CRSP](http://www.crsp.org/products/research-products/crsp-us-stock-databases), 
[Compustat Fundamental Annuals](https://wrds-web.wharton.upenn.edu/wrds/support/Data/_001Manuals%20and%20Overviews/_001Compustat/_001North%20America%20-%20Global%20-%20Bank/_000dataguide/index.cfm0), and other datafiles. 

This module uses the [`WRDS-Py`](https://github.com/wharton/wrds) library package to extract data from CRPS and Compustat Fundamental Annuals via the cloud
for use with the [`Pandas-Py`](https://github.com/pandas-dev/pandas/issues/25571) package. 

`famafrench`'s efficient performance results from features such as the use of a [least recently used (LRU) cache](https://docs.python.org/3/library/functools.html).


| Metric                     |                                                                                                                                                                                                                                          |
| :------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Latest Release**         | [![PyPI version](https://badge.fury.io/py/arch.svg)](https://badge.fury.io/py/arch)                                                                                                                                                      |
|                            | [![Anaconda-Server Badge](https://anaconda.org/bashtage/arch/badges/version.svg)](https://anaconda.org/bashtage/arch)                                                                                                                    |
| **Continuous Integration** | [![Travis Build Status](https://travis-ci.org/bashtage/arch.svg?branch=master)](https://travis-ci.org/bashtage/arch)                                                                                                                     |
|                            | [![Appveyor Build Status](https://ci.appveyor.com/api/projects/status/nmt02u7jwcgx7i2x?svg=true)](https://ci.appveyor.com/project/bashtage/arch/branch/master)                                                                           |
| **Coverage**               | [![Coverage Status](https://coveralls.io/repos/github/bashtage/arch/badge.svg?branch=master)](https://coveralls.io/r/bashtage/arch?branch=master)                                                                                        |
|                            | [![codecov](https://codecov.io/gh/bashtage/arch/branch/master/graph/badge.svg)](https://codecov.io/gh/bashtage/arch)                                                                                                                     |
| **Code Quality**           | [![Code Quality: Python](https://img.shields.io/lgtm/grade/python/g/bashtage/arch.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/bashtage/arch/context:python)                                                                 |
|                            | [![Total Alerts](https://img.shields.io/lgtm/alerts/g/bashtage/arch.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/bashtage/arch/alerts)                                                                                       |
|                            | [![Codacy Badge](https://api.codacy.com/project/badge/Grade/93f6fd90209842bf97fd20fda8db70ef)](https://www.codacy.com/manual/bashtage/arch?utm_source=github.com&utm_medium=referral&utm_content=bashtage/arch&utm_campaign=Badge_Grade) |
|                            | [![codebeat badge](https://codebeat.co/badges/18a78c15-d74b-4820-b56d-72f7e4087532)](https://codebeat.co/projects/github-com-bashtage-arch-master)                                                                                       |
| **Citation**               | [![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.3551028.svg)](https://doi.org/10.5281/zenodo.3551028)                                                                                                                                |
| **Documentation**          | [![Documentation Status](https://readthedocs.org/projects/arch/badge/?version=latest)](http://arch.readthedocs.org/en/latest/)                                                                                                           |

To best explore `famafrench`....

**Installation**

`famafrench` is available via [PyPI](https://pypi.python.org/pypi/pyfinance/).  The latest version is 0.1.0 as of April 2020.  Install with pip:

```
$ pip install `famafrench`
```

