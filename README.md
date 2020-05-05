# `famafrench`

`famafrench` is a Python library package designed to replicate and construct datasets from  
[Ken French's online data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) 
via remote access to the [wrds-cloud](https://wrds-www.wharton.upenn.edu/pages/support/getting-started/3-ways-use-wrds/#the-wrds-cloud)
by querying [CRSP](http://www.crsp.org/products/research-products/crsp-us-stock-databases), 
[Compustat Fundamentals Annual](https://wrds-web.wharton.upenn.edu/wrds/support/Data/_001Manuals%20and%20Overviews/_001Compustat/_001North%20America%20-%20Global%20-%20Bank/_000dataguide/index.cfm0), and other datafiles. 

This module uses the [`WRDS-Py`](https://github.com/wharton/wrds) library package to extract data from CRPS, Compustat Fundamentals Annual, and other datafiles via the cloud
for use with the [`Pandas-Py`](https://github.com/pandas-dev/pandas) package. 

`famafrench`'s current efficient performance results from features such as the use of a [least recently used (LRU) cache](https://medium.com/lambda-automotive/python-and-lru-cache-f812bbdcbb51) implemented using the Python decorator
[``functools.lru_cache``](https://github.com/python/cpython/blob/3.8/Lib/functools.py).

| Metric                     |                                                                                                                                                                                                                                                                                   |
| :------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------                                                                                                               |
| **Supports**               | Python 3.4+                                                                                                                                                                                                                                                                       | 
|                            | [![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                                                                                                                                                             |                                             
|                            | [![Python 3](https://pyup.io/repos/github/christianjauregui/famafrench/python-3-shield.svg)](https://pyup.io/repos/github/christianjauregui/famafrench/)                                                                                                                          |
| **Latest Release**         | ![GitHub Release Date](https://img.shields.io/github/release-date/christianjauregui/famafrench)                                                                                                                                                                                   |
|                            | [![PyPI version](https://d25lcipzij17d.cloudfront.net/badge.svg?id=py&type=6&v=0.1.3&x2=0)](https://pypi.org/project/famafrench/)                                                                                                                                                 |
| **Code Quality**           | [![Updates](https://pyup.io/repos/github/christianjauregui/famafrench/shield.svg)](https://pyup.io/repos/github/christianjauregui/famafrench/)                                                                                                                                    |
|                            | [![Codacy Badge](https://api.codacy.com/project/badge/Grade/a81ccb9c22144f6bbf7b25d6926c5217)](https://app.codacy.com/manual/christianjauregui/famafrench?utm_source=github.com&utm_medium=referral&utm_content=christianjauregui/famafrench&utm_campaign=Badge_Grade_Dashboard)  |                                                                                                                                                                                          |
| **Citation**               | [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3785913.svg)](https://doi.org/10.5281/zenodo.3785913)                                                                                                                                                                         |
| **License**                | [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/christianjauregui/famafrench/blob/master/LICENSE.txt)                                                                                                                                 |
| **Documentation**          | [![made-with-sphinx-doc](https://img.shields.io/badge/Made%20with-Sphinx-1f425f.svg)](https://www.sphinx-doc.org/)                                                                                                                                                                |
|                            | [![documentation Status](https://img.shields.io/badge/Documentation-latest-brightgreen)](https://christianjauregui.github.io/famafrench/)                                                                                                                                         |   
| **Contributing**           | [![contributions welcome](https://img.shields.io/badge/Contributions-welcome-brightgreen.svg?style=flat)](https://github.com/christianjauregui/famafrench/issues)                                                                                                                 |
| **HitCount!**              | [![HitCount](http://hits.dwyl.com/christianjauregui/famafrench.svg)](http://hits.dwyl.com/christianjauregui/famafrench)                                                                                                                                                           |

`famafrench` is best explored by going through applications and examples provided in the released documentation hosted on [Github Pages](https://christianjauregui.github.io/famafrench/).

## Module Contents
| Module            | Description                                                                                                                                      |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `famafrench.py`   | Main module w/ tools for constructing and replicating datasets from Ken French’s online library via queries to WRDS.                             |
| `utils.py`        | Auxiliary functions and utilities for use in the main module `famafrench.py`.                                                                    |
| `wrdsconnect.py`  | Enables remote connection to wrds-cloud largely building on the ``Connection()`` class in the [WRDS-Py](https://pypi.org/project/wrds/) library. |
| `version.py`      | Module w/ package's version number.                                                                                                              |

## Installation
The latest release is **Release 0.1.3** as of May 5, 2020 (see [documentation](https://christianjauregui.github.io/famafrench/changes/changes.html#)).

### Python Package Index (`pip`)
Releases are available via [PyPI](https://pypi.org/project/famafrench/) and can be installed with `pip`.  
```bash
pip install famafrench
```
### Anaconda (`conda`)
Conda users will soon be able to install from my [Anaconda](https://anaconda.org/) channel. Stay tuned.

## Dependencies
`famafrench` relies on a suite of Python libraries, which include Python's scientific computing stack (e.g. [NumPy](https://numpy.org/) and [Pandas](https://pandas.pydata.org/)). Other dependencies include [Numba](http://numba.pydata.org/) and [SQLAlchemy](https://www.sqlalchemy.org/). 

Please see [``setup.py``](https://github.com/christianjauregui/famafrench/blob/master/setup.py) or [``requirements.txt``](https://github.com/christianjauregui/famafrench/blob/master/docs/requirements.txt) for specific version threshold requirements.

## Documentation
Released documentation is hosted on [Github Pages](https://christianjauregui.github.io/famafrench/). Look out for future updated documentation from my master branch hosted on Github.

## Contributing
I welcome recommendations, contributions and/or future collaborations. I am ambitious and plan to expand the module to include construction of additional factor-based datasets relevant for empirical asset pricing. These include the following:

-   [AQR Capital Management](https://www.aqr.com/library/data-sets): 

    -   *Betting Against Beta* (BAB)
    -   *Quality Minus Junk* (QMJ)
    -   *Modified Value - High Minus Low* (HMLD)

-   [Lettau, Ludvigson, and Ma (2019)](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12772) Capital Share Factor:   
 
    -   *Capital Share of Aggregate Income* (KS)

-   [Pastor and Stambaugh (2003)](https://faculty.chicagobooth.edu/-/media/faculty/lubos-pastor/data/liq_data_1962_2019.txt) Liquidity Factors: 
 
    -   *Non-Traded Liquidity Factor*
    -   *Traded Liquidity Factor*

-   [Sadka (2006)](https://drive.google.com/file/d/1hTnBk7uasanA3x1gRFBNg6hFE1A0JJEO/view) Liquidity Factors:

    -   *Fixed-Transitory Factor*
    -   *Variable-Permanent Factor*

-   [Stambaugh and Yuan (2017)](https://academic.oup.com/rfs/article/30/4/1270/2965095) *Clustered* Mispricing Factors: 
 
    -   *Management-related Factor* (MGMT)
    -   *Performance-related Factor* (PERF)
    -   *Mispricing (non-clustered) Factor* (UMO)
    

Performance and speed improvements are also appreciated. 

Please report any bugs or errors to [my github page](https://github.com/christianjauregui/famafrench/issues) or please send me an email at chris.jauregui@berkeley.edu.  

## API
For in-depth call syntaxes, please see the source code doctrings. 