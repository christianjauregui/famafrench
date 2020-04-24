# `famafrench`

`famafrench` is a Python library package designed to replicate and construct datasets from Ken French's 
[online data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) 
via remote access to the [wrds-cloud](https://wrds-www.wharton.upenn.edu/pages/support/getting-started/3-ways-use-wrds/#the-wrds-cloud)
by querying [CRSP](http://www.crsp.org/products/research-products/crsp-us-stock-databases), 
[Compustat Fundamentals Annual](https://wrds-web.wharton.upenn.edu/wrds/support/Data/_001Manuals%20and%20Overviews/_001Compustat/_001North%20America%20-%20Global%20-%20Bank/_000dataguide/index.cfm0), and other datafiles. 

This module uses the [`WRDS-Py`](https://github.com/wharton/wrds) library package to extract data from CRPS and Compustat Fundamentals Annual via the cloud
for use with the [`Pandas-Py`](https://github.com/pandas-dev/pandas/issues/25571) package. 

`famafrench`'s current efficient performance results from features such as the use of a [least recently used (LRU) cache](https://docs.python.org/3/library/functools.html).


| Metric                     |                                                                                                                                                                                                                                          |
| :------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Supports**         | Python 3.4+                                                                                                                                          |
| **Citation**               | [![DOI](https://img.shields.io/badge/doi-10.26180/5c6e1160b8d8a-blue.svg?style=flat&labelColor=whitesmoke&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAAB8AAAAfCAYAAAAfrhY5AAAJsklEQVR42qWXd1DTaRrHf%2BiB2Hdt5zhrAUKz4IKEYu9IGiGFFJJQ0gkJCAKiWFDWBRdFhCQUF3UVdeVcRQEBxUI3yY9iEnQHb3bdW1fPubnyz%2F11M7lvEHfOQee2ZOYzPyDv%2B3yf9%2Fk95YX4fx%2BltfUt08GcFEuPR4U9hDDZ%2FVngIlhb%2FSiI6InkTgLzgDcgfvtnovhH4BzoVlrbwr55QnhCtBW4QHXnFrZbPBaQoBh4%2FSYH2EnpBEtqcDMVzB93wA%2F8AFwa23XFGcc8CkT3mxz%2BfXWtq9T9IQlLIXYEuHojudb%2BCM7Hgdq8ydi%2FAHiBXyY%2BLjwFlAEnS6Jnar%2FvnQVhvdzasad0eKvWZKe8hvDB2ofLZ%2FZEcWsh%2BhyIuyO5Bxs2iZIE4nRv7NWAb0EO8AC%2FWPxjYAWuOEX2MSXZVgPxzmRL3xKz3ScGpx6p6QnOx4mDIFqO0w6Q4fEhO5IzwxlSwyD2FYHzwAW%2BAZ4fEsf74gCumykwNHskLM7taQxLYjjIyy8MUtraGhTWdkfhkFJqtvuVl%2F9l2ZquDfEyrH8B0W06nnpH3JtIyRGpH1iJ6SfxDIHjRXHJmdQjLpfHeN54gnfFx4W9QRnovx%2FN20aXZeTD2J84hn3%2BqoF2Tqr14VqTPUCIcP%2B5%2Fly4qC%2BUL3sYxSvNj1NwsVYPsWdMUfomsdkYm3Tj0nbV0N1wRKwFe1MgKACDIBdMAhPE%2FwicwNWxll8Ag40w%2BFfhibJkGHmutjYeQ8gVlaN%2BjO51nDysa9TwNUFMqaGbKdRJZFfOJSp6mkRKsv0rRIpEVWjAvyFkxNOEpwvcAVPfEe%2Bl8ojeNTx3nXLBcWRrYGxSRjDEk0VlpxYrbe1ZmaQ5xuT0u3r%2B2qe5j0J5uytiZPGsRL2Jm32AldpxPUNJ3jmmsN4x62z1cXrbedXBQf2yvIFCeZrtyicZZG2U2nrrBJzYorI2EXLrvTfCSB43s41PKEvbZDEfQby6L4JTj%2FfIwam%2B4%2BwucBu%2BDgNK05Nle1rSt9HvR%2FKPC4U6LTfvUIaip1mjIa8fPzykii23h2eanT57zQ7fsyYH5QjywwlooAUcAdOh5QumgTHx6aAO7%2FL52eaQNEShrxfhL6albEDmfhGflrsT4tps8gTHNOJbeDeBlt0WJWDHSgxs6cW6lQqyg1FpD5ZVDfhn1HYFF1y4Eiaqa18pQf3zzYMBhcanlBjYfgWNayAf%2FASOgklu8bmgD7hADrk4cRlOL7NSOewEcbqSmaivT33QuFdHXj5sdvjlN5yMDrAECmdgDWG2L8P%2BAKLs9ZLZ7dJda%2BB4Xl84t7QvnKfvpXJv9obz2KgK8dXyqISyV0sXGZ0U47hOA%2FAiigbEMECJxC9aoKp86re5O5prxOlHkcksutSQJzxZRlPZmrOKhsQBF5zEZKybUC0vVjG8PqOnhOq46qyDTDnj5gZBriWCk4DvXrudQnXQmnXblebhAC2cCB6zIbM4PYgGl0elPSgIf3iFEA21aLdHYLHUQuVkpgi02SxFdrG862Y8ymYGMvXDzUmiX8DS5vKZyZlGmsSgQqfLub5RyLNS4zfDiZc9Edzh%2FtCE%2BX8j9k%2FqWB071rcZyMImne1SLkL4GRw4UPHMV3jjwEYpPG5uW5fAEot0aTSJnsGAwHJi2nvF1Y5OIqWziVCQd5NT7t6Q8guOSpgS%2Fa1dSRn8JGGaCD3BPXDyQRG4Bqhu8XrgAp0yy8DMSvvyVXDgJcJTcr1wQ2BvFKf65jqhvmxXUuDpGBlRvV36XvGjQzLi8KAKT2lYOnmxQPGorURSV0NhyTIuIyqOmKTMhQ%2BieEsgOgpc4KBbfDM4B3SIgFljvfHF6cef7qpyLBXAiQcXvg5l3Iunp%2FWv4dH6qFziO%2BL9PbrimQ9RY6MQphEfGUpOmma7KkGzuS8sPUFnCtIYcKCaI9EXo4HlQLgGrBjbiK5EqMj2AKWt9QWcIFMtnVvQVDQV9lXJJqdPVtUQpbh6gCI2Ov1nvZts7yYdsnvRgxiWFOtNJcOMVLn1vgptVi6qrNiFOfEjHCDB3J%2BHDLqUB77YgQGwX%2Fb1eYna3hGKdlqJKIyiE4nSbV8VFgxmxR4b5mVkkeUhMgs5YTi4ja2XZ009xJRHdkfwMi%2BfocaancuO7h%2FMlcLOa0V%2FSw6Dq47CumRQAKhgbOP8t%2BMTjuxjJGhXCY6XpmDDFqWlVYbQ1aDJ5Cptdw4oLbf3Ck%2BdWkVP0LpH7s9XLPXI%2FQX8ws%2Bj2In63IcRvOOo%2BTTjiN%2BlssfRsanW%2B3REVKoavBOAPTXABW4AL7e4NygHdpAKBscmlDh9Jysp4wxbnUNna3L3xBvyE1jyrGIkUHaqQMuxhHElV6oj1picvgL1QEuS5PyZTEaivqh5vUCKJqOuIgPFGESns8kyFk7%2FDxyima3cYxi%2FYOQCj%2F%2B9Ms2Ll%2Bhn4FmKnl7JkGXQGDKDAz9rUGL1TIlBpuJr9Be2JjK6qPzyDg495UxXYF7JY1qKimw9jWjF0iV6DRIqE%2B%2FeWG0J2ofmZTk0mLYVd4GLiFCOoKR0Cg727tWq981InYynvCuKW43aXgEjofVbxIqrm0VL76zlH3gQzWP3R3Bv9oXxclrlO7VVtgBRpSP4hMFWJ8BrUSBCJXC07l40X4jWuvtc42ofNCxtlX2JH6bdeojXgTh5TxOBKEyY5wvBE%2BACh8BtOPNPkApjoxi5h%2B%2FFMQQNpWvZaMH7MKFu5Ax8HoCQdmGkJrtnOiLHwD3uS5y8%2F2xTSDrE%2F4PT1yqtt6vGe8ldMBVMEPd6KwqiYECHDlfbvzphcWP%2BJiZuL5swoWQYlS%2Br7Yu5mNUiGD2retxBi9fl6RDGn4Ti9B1oyYy%2BMP5G87D%2FCpRlvdnuy0PY6RC8BzTA40NXqckQ9TaOUDywkYsudxJzPgyDoAWn%2BB6nEFbaVxxC6UXjJiuDkW9TWq7uRBOJocky9iMfUhGpv%2FdQuVVIuGjYqACbXf8aa%2BPeYNIHZsM7l4s5gAQuUAzRUoT51hnH3EWofXf2vkD5HJJ33vwE%2FaEWp36GHr6GpMaH4AAPuqM5eabH%2FhfG9zcCz4nN6cPinuAw6IHwtvyB%2FdO1toZciBaPh25U0ducR2PI3Zl7mokyLWKkSnEDOg1x5fCsJE9EKhH7HwFNhWMGMS7%2BqxyYsbHHRUDUH4I%2FAheQY7wujJNnFUH4KdCju83riuQeHU9WEqNzjsJFuF%2FdTDAZ%2FK7%2F1WaAU%2BAWymT59pVMT4g2AxcwNa0XEBDdBDpAPvgDIH73R25teeuAF5ime2Ul0OUIiG4GpSAEJeYW9wDTf43wfwHgHLKJoPznkwAAAABJRU5ErkJggg%3D%3D)](https://doi.org/10.6084/m9.figshare.12170439.v1)                                                                                                                                 |
| **License**  | [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/christianjauregui/famafrench/blob/master/LICENSE)
| **Documentation**          | [![Documentation Status](https://readthedocs.org/projects/famafrench/badge/?version=latest)](https://famafrench.readthedocs.io/en/latest/?badge=latest)                                                                                                           |

`famafrench` is best explored by going through applications and examples provided in the released documentation hosted on [Read The Docs](https://famafrench.readthedocs.io/en/latest/applications/applications.html).


## Module Contents

| Module | Description |
| ------ | ----------- |
| `famafrench.py`  | Main module w/ tools for constructing and replicating datasets from Ken French’s online library via queries to WRDS. |
| `utils.py`   | Auxiliary functions and utilities for use in the main module `famafrench.py`. |
| `wrdsconnect.py`       | Enables remote connection to wrds-cloud largely building on the ``Connection()`` class in the [WRDS-Py](https://pypi.org/project/wrds/) library. |
| `version.py`   | Module w/ package's version number.  |


## Installation
The latest release is **Release 0.1.0** as of April 2020 (see [documentation](https://famafrench.readthedocs.io/en/latest/changes/changes.html#release-0-1-0)).
### Python Package Index (`pip):

Releases are available via [PyPI](https://pypi.python.org/pypi/pyfinance/) and can be installed with `pip`.  
```bash
pip install famafrench
```
### Anaconda (`conda`):

Conda users will soon be able to install from my [Anaconda](https://anaconda.org/) channel. Stay tuned.


## Dependencies
`famafrench` relies on a suite of Python libraries, which include Python's scientific computing stack (e.g. [NumPy](https://numpy.org/) and [Pandas](https://pandas.pydata.org/)). Other dependencies include [Numba](http://numba.pydata.org/) and [SQLAlchemy](https://www.sqlalchemy.org/). 

Please see [``setup.py``](https://github.com/christianjauregui/famafrench/blob/master/setup.py) or [``requirements.txt``](https://github.com/christianjauregui/famafrench/blob/master/docs/requirements.txt) for specific version threshold requirements.



## Documentation
Released documentation is hosted on [Read The Docs](https://famafrench.readthedocs.io/en/latest/?badge=latest). Look out for updated documentation from my master branch hosted on Github.



## Contributing

I welcome recommendations, contributions and/or future collaborations. I am ambitious and plan to expand the module to include construction of additional factor-based datasets relevant for empirical asset pricing. These include the following:


- [AQR Capital Management's](https://www.aqr.com/library/data-sets):
    
    - `Betting Against Beta` (BAB)
    - `Quality Minus Junk` (QMJ)
    - `Modified Value - High Minus Low` (HMLD)


- [Lettau, Ludvigson, and Ma (2019)](https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12772) Capital Share Factor:
    
    - `Capital Share of Aggregate Income` (KS)


- [Pastor and Stambaugh (2003)](https://faculty.chicagobooth.edu/-/media/faculty/lubos-pastor/data/liq_data_1962_2019.txt) Liquidity Factors:
    
    - `Non-Traded Liquidity Factor`
    - `Traded Liquidity Factor`


- [Sadka (2006)](https://drive.google.com/file/d/1hTnBk7uasanA3x1gRFBNg6hFE1A0JJEO/view) Liquidity Factors:
    
    - `Fixed-Transitory Factor`
    - `Variable-Permanent Factor`


- [Stambaugh and Yuan (2017)](https://academic.oup.com/rfs/article/30/4/1270/2965095) *Clustered* Mispricing Factors:
    
    - `Management-related Factor` (MGMT)
    - `Performance-related Factor` (PERF)
    - `Mispricing (non-clustered) Factor` (UMO)
    

Performance and speed improvements are also appreciated. 

Please report any bugs or errors to [my github page](https://github.com/christianjauregui/famafrench) or please send me an email at chris.jauregui@berkeley.edu.  


## API

For in-depth call syntaxes, please see the source code doctrings. 