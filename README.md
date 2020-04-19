# `famafrench`

`famafrench` is a Python package designed to replicate and construct datasets from Ken French's 
[online data library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html) 
via remote access to the [wrds-cloud](https://wrds-www.wharton.upenn.edu/pages/support/getting-started/3-ways-use-wrds/#the-wrds-cloud)
by querying [CRSP](http://www.crsp.org/products/research-products/crsp-us-stock-databases) and 
[Compustat Fundamental Annuals](https://wrds-web.wharton.upenn.edu/wrds/support/Data/_001Manuals%20and%20Overviews/_001Compustat/_001North%20America%20-%20Global%20-%20Bank/_000dataguide/index.cfm0).

This module uses the [`WRDS-Py`](https://github.com/wharton/wrds) library package to extract data from CRPS and Compustat Fundamental Annuals via the cloud
for use with the [`Pandas-Py`](https://github.com/pandas-dev/pandas/issues/25571) package. 

`famafrench`'s efficient performance results from features such as the use of a [least recently used (LRU) cache](https://docs.python.org/3/library/functools.html)


## Contents
To best explore `famafrench`....

**Installation**

`famafrench` is available via [PyPI](https://pypi.python.org/pypi/pyfinance/).  The latest version is 0.1.0 as of March 2020.  Install with pip:

```
$ pip install `famafrench`
```

