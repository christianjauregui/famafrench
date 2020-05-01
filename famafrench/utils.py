"""
This file is part of famafrench.
Copyright (c) 2020, Christian Jauregui <chris.jauregui@berkeley.edu>
See file LICENSE.txt for license information.

Filename
_________
`famafrench/utils.py`

Descriptions
____________
lru_cached_method
    Wrapper for methodtools.lru_cache(maxsize) that allows for sphinx documentation
    recognition of decorated instance methods.
get_kfpriorfactors_directly
    Directly download zipped datafiles from Ken French's online data library without the
    use of the 'pandas-datareader' package. This method is used for a select few
    number of datafiles for which 'pandas-datareader' returns an error.
timing
    Wrapper for class methods that are to be timed for speed and performance measurement.
any_in
    Provide a boolean variable that is =True if elements in a given set intersect with
    elements in another set, =False, otherwise.
priormonthToDay
    Using Fama and French's methodology, map the prior (j-k) monthly return strategy into
    a daily strategy (see online documentation provided on Ken French's website).
grouped_vwAvg
     Calculate weighted (net) portfolio return for a given portfolio with weights within a
     group or set of groups. This function is FASTER THAN groupby(...).apply(...) because
     it avoids non-optimized aggregation.
portRetAvg
    Compute a simple average across different columns.
get_statsTable
    Construct tables with formatted summary statistics.
"""

__author__ = 'Christian Jauregui <chris.jauregui@berkeley.edu'
__all__ = [
    "lru_cached_method",
    "get_kfpriorfactors_directly",
    "timing",
    "any_in",
    "priormonthToDay",
    "grouped_vwAvg",
    "portRetAvg",
    "get_statsTable",
]

# Standard Imports
import weakref
import pandas as pd
import numpy as np
from functools import wraps
from methodtools import lru_cache  # see documentation: https://pypi.org/project/methodtools/
from time import time

# Function: lru_cached_method(.,.):
def lru_cached_method(*lru_args, **lru_kwargs):
    """
    Wrapper for :func:`methodtools.lru_cache` enabling recognition of `decorated`
    class instance methods by `Sphinx <https://www.sphinx-doc.org/en/master/>`_.

    Parameters
    __________
    *lru_args : arbitrary
        Variable number of arguments to :func:`methodtools.lru_cache`

    **lru_kwargs : arbitrary
        Keyworded, variable-length argument list for :func:`methodtools.lru_cache`

    Returns
    _______
    decorator : arbitrary `wrapped` object
        Wrapped function.
    """
    def decorator(wrapped_fn):
        @wraps(wrapped_fn)
        def wrapped(self, *args, **kwargs):
            # Use a weak reference to self. This prevents a self-reference cycle that fools the garbage collector
            # into thinking the instance shouldn't be dropped when all external references are dropped.
            weak_ref_to_self = weakref.ref(self)
            @wraps(wrapped_fn)
            @lru_cache(*lru_args, **lru_kwargs)
            def cached(*args, **kwargs):
                return wrapped_fn(weak_ref_to_self(), *args, **kwargs)
            setattr(self, wrapped_fn.__name__, cached)
            return cached(*args, **kwargs)
        return wrapped
    return decorator


# Function: get_kfpriorfactors_directly(.,.):
def get_kfpriorfactors_directly(kflib_name, kflib_freq, kf_factor):
    """
    Directly download (from Ken French's online library) zipped monthly or annual datafiles
    for the `Short-Term Reversal` or `Long-Term Reversal` Fama-French-style factors.
    This is required since the :meth:`pandas_datareader.web` method is broken for such datafiles.

    Parameters
    ___________
    kflib_name : str
        Name of zipped datafile.
    kflib_freq : str
        Observation frequency of factor portfolios. Possible choices are:

            * ``M``: monthly
            * ``A``: annual
    kf_factor : str
        The name or "label" of the Fama-French-style factor. Possible choices are:

            * ``ST_Rev`` : Short-Term Reversal - based on Prior (1-1) returns
            * ``LT_Rev`` : Long-Term Reversal - based on Prior (13-60) returns

    Returns
    ________
    kflib_data : pandas.DataFrame
        Dataset with time-series of the Fama-French-style factor.
    """
    from io import BytesIO
    from zipfile import ZipFile
    from urllib.request import urlopen

    urllink = "http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/"+kflib_name+"_CSV.zip"
    url = urlopen(urllink)

    # Download Zipfile and create pandas.DataFrame
    zipfile = ZipFile(BytesIO(url.read()))
    kflib_data = pd.read_csv(zipfile.open(kflib_name+".CSV"), header=0, skiprows=13)
    kflib_data.rename(columns={'Unnamed: 0': 'Date'}, inplace=True)
    kflib_data.columns = list(map(str.rstrip, kflib_data.columns))

    if kf_factor not in ['ST_Rev', 'LT_Rev']:
        kf_factor = kf_factor.title()

    # Get first row number that has all values set to "nan" coinciding with the start of annual data
    rows_with_all_nan = kflib_data.index[kflib_data[kf_factor].isna()]
    diffrows_with_all_nan = [j-i for i, j in zip(rows_with_all_nan[:-1], rows_with_all_nan[1:])]
    first_nan = rows_with_all_nan[0]
    second_nan = rows_with_all_nan[diffrows_with_all_nan.index(max(diffrows_with_all_nan))+1]

    if kflib_freq == 'M':
        kflib_data = kflib_data[:first_nan]
        kflib_data.loc[:, 'Date'] = pd.to_datetime(kflib_data['Date'], format='%Y%m').dt.to_period('M')
    elif kflib_freq == 'A':
        kflib_data = kflib_data[first_nan+4:second_nan]
        kflib_data.loc[:, 'Date'] = pd.to_datetime(kflib_data['Date'], format='%Y').dt.to_period('Y')
    kflib_data = kflib_data[['Date', kf_factor]]
    kflib_data[kf_factor] = kflib_data[kf_factor].replace(-99.99, np.nan).astype(float)
    if kf_factor not in ['ST_Rev', 'LT_Rev']:
        kflib_data = kflib_data.rename(columns={kf_factor: kf_factor.title().upper()})
    kflib_data.set_index('Date', inplace=True)
    return kflib_data


# Function: timing(.)
def timing(func):
    """
    Wrapper for class instance methods enabling the timing of execution.
    Important for measuring speed and performance measurement.

    Parameters
    ___________
    func : func
        Function to be wrapped and timed following execution.

    Returns
    ________
    wrapper : arbitrary `wrapped` object
        The wrapped result(s) for the function `func`.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        t0 = time()
        result = func(*args, **kwargs)
        print("Elapsed time: ", round(time() - t0, 3), " seconds.\n")
        return result
    return wrapper


# Function: any_in(.,.)
def any_in(a_set, b_set):
    """
    Boolean variable that is ``True`` if elements in a given set `a_set` intersect
    with elements in another set `b_set`. Otherwise, the boolean is ``False``.

    Parameters
    ___________
    a_set : list
        First set of elements.
    b_set : list
        Second set of elements.

    Returns
    ________
    not set(a_set).isdisjoint(b_set) : bool
        Boolean that is ``True`` if there is a non-empty intersection between both sets.
        Otherwise, the boolean is ``False``.
    """
    return not set(a_set).isdisjoint(b_set)


# Function: priormonthToDay(.,.,.)
def priormonthToDay(freq, j_mth, k_mth):
    """
    Consistent w/ Fama and French (2008, 2016), map the prior `(j-k)` monthly return strategy into a daily strategy
    (see `Ken French's online documentation  <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>`_).

    Parameters
    ___________
    freq : str
        Frequency used to calculate prior `(j-k)` return strategy. Possible choices are:

            * ``D`` : daily
            * ``'M`` : monthly
    j_mth : str
        Lagged month (or day) we start measuring stock performance.
    k_mth : str
        How many months (or days) are used in measuring stock performance.

    Returns
    ________
    j_per, k_per : tuple, str
        ``j_per = j_mth`` and ``k_per = k_mth`` if ``freq = M``.
        Otherwise, monthly figures mapped to daily periods using the description found on Ken French's online documentation:

            * `Daily Momentum <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_mom_factor_daily.html>`_.
            * `Daily Short-Term Reversal <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_st_rev_factor_daily.html>`_.
            * `Daily Long-Term Reversal <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_lt_rev_factor_daily.html>`_.

    Note
    ____
    Monthly ``M`` (daily ``D``) strategies involve portfolios formed every month `t-1` (or day `t-1`)
    for month `t` (or day `t`).

    Note
    ____
    The Fama and French (2008, 2016) momentum strategy definition differs from that of Jegadeesh and Titman (1993).
    Jegadeesh and Titman (1993) consider **J/K** strategies, which include portfolios formed on stock performance over the previous
    **J** months (excluding the last week or month prior to portfolio formation, to remove the
    large short-horizon reversals associated with bid-ask bounce) and hold portfolios for **K** months, where **J**, **K** :math:`\in` {3,6,9,12}.
    Future updates to this module will extend this package to include these additional momentum strategies.


    References
    ___________
    *   Fama, Eugene F., and Kenneth R. French. (2008). `Dissecting Anomalies`,
        Journal of Finance, 48(4), pp.1653-1678

    *   Fama, Eugene F., and Kenneth R. French. (2016). `Dissecting Anomalies with a Five-Factor Model`,
        Journal of Finance, 48(4), pp.1653-1678
    """
    # Per Fama and French, map prior (2-12), (1-1), and (13-60) returns
    # at the monthly frequency to the daily frequency
    if freq in ['D', 'W']:
        if (j_mth == '2') and (k_mth == '12'):
            j_per, k_per = '21', '250'
            return j_per, k_per
        elif (j_mth == '1') and (k_mth == '1'):
            j_per, k_per = '1', '20'
            return j_per, k_per
        elif (j_mth == '13') and (k_mth == '60'):
            j_per, k_per = '251', '1250'
            return j_per, k_per
        else:
            raise ValueError('\'prior (j-k)\' return strategy not of the standard Fama and French type.')
    elif freq in ['M', 'Q', 'A']:
        j_per, k_per = j_mth, k_mth
        return j_per, k_per
    else:
        raise ValueError('Please specify one of the following frequencies: \'D\' or \'M\'')


# Function: grouped_vwAvg(.,.,.,.,.)
def grouped_vwAvg(df0, col_values, col_weights, *groupby_args, **groupby_kwargs):
    """
    Calculate (net) weighted portfolio return for portfolio with weights ``col_weights`` within a group or groups.

    Parameters
    ___________
    df0 : pandas.DataFrame
        Dataset containing firm-level stock returns and portfolio weights, both indexed by dates and firm identifiers when required.
    col_values : list, str
        Column(s) to average over.
    col_weights : str
        Column containing the portfolio weights.
    group_args : list, str, [optional]
        args to pass into `groupby` (ie the level to group on).
    group_kwargs : list, str, [optional]
        kwargs to pass into `groupby`.

    Returns
    ________
    df1 : pandas.Series, or pandas.DataFrame
        Original dataset augmented w/ value-weighted returns.

    Note
    ____
    Function is **FASTER** than :func:`pandas.core.groupby.GroupBy.apply` since it avoids non-optimized aggregation.
    """
    if isinstance(col_values, str):
        col_values = [col_values]

    ss = []
    for value in col_values:
        df1 = df0.copy()
        value_x_weight = 'product_{v}_{w}'.format(v=value, w=col_weights)
        weights = 'weights_{w}'.format(w=col_weights)

        df1[value_x_weight] = df1[value] * df1[col_weights]
        df1[weights] = df1[col_weights].where(~df1[value_x_weight].isnull())
        df1 = df1.groupby(*groupby_args, **groupby_kwargs).sum()
        s = df1[value_x_weight] / df1[weights]

        s.name = value
        ss.append(s)
    df1 = pd.concat(ss, axis=1) if len(ss) > 1 else ss[0]
    return df1


# Function: portRetAvg(.)
def portRetAvg(df):
    """
    Compute a simple average across different columns.

    Parameters
    ___________
    df : pandas.DataFrame
        Dataset with columns to average over.

    Returns
    ________
    dfavg : pandas.DataFrame
        Dataset with the averaged columns.
    """
    dfavg = df.sum(axis=1, min_count=len(df.columns)) / len(df.columns)
    return dfavg


# Function: get_statsTable(.,.,.,.)
def get_statsTable(dType, dFreq, df, dates_as_index=True, ptiles=None):
    """
    Construct detailed tables with summary statistics.

    Parameters
    ___________
    dType : str
        Dataset type of the portfolios. Possible choices are:

            * ``Returns``
            * ``Factors``
            * ``NumFirms``
            * ``Characs``
    dFreq : str
        Observation frequency of the portfolios. Possible choices are:

            * ``D`` : daily
            * ``W`` : weekly
            * ``M`` : monthly
            * ``Q`` : quarterly (3-months)
            * ``A`` : annual
    df : pandas.DataFrame
        Dataset w/ portfolio returns (which may include factor returns), number of firms in each portfolio,
        or `average` anomaly portfolio characteristics for a given portfolio sorting strategy.
    dates_as_index : bool
        Flag determining whether ``df`` has a :class:`pandas.DatetimeIndex` index (``dates_as_index = True``).
        Otherwise, ``dates_as_index = False``.
    ptiles : list, float, default None
        List of percentiles (in decimal format) included as part of output results.
        If ``None``, then ``ptiles = [0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]``.


    Returns
    ________
    statsTable : pandas.DataFrame
        Summary statistics of the dataset including the following:

            * number of observations :meth:`pandas.DataFrame.count`
            * sample mean :meth:`pandas.DataFrame.mean`
            * sample standard deviation :meth:`pandas.DataFrame.std`
            * sample min :meth:`pandas.DataFrame.min`
            * sample max :meth:`pandas.DataFrame.max`
            * sample skewness :meth:`pandas.DataFrame.skew`
            * sample kurtosis :meth:`pandas.DataFrame.kurtosis`
            * sample mean absolute deviation :meth:`pandas.DataFrame.mad`
            * sample percentiles :meth:`numpy.percentile`

        If ``dates_as_index = True``, then the table also includes the starting and ending date for each observation type.
    """
    if ptiles is None:
        ptiles = [0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99]
    statsTable = df.describe(percentiles=ptiles).round(2)
    statsTable = statsTable.append(df.reindex(statsTable.columns, axis=1).agg(['skew', 'kurt', 'mad'])).round(2)

    # Find starting and ending date of each observation type
    if dates_as_index:
        statsTable0 = pd.DataFrame(index=['startdate', 'enddate'], columns=df.columns)
        for col in df.columns:
            sdate = df[col].first_valid_index()
            edate = df[col].index.max()
            statsTable0.loc['startdate', col] = sdate
            statsTable0.loc['enddate', col] = edate
        statsTable = statsTable0.append(statsTable)

    if dType in ['Factors', 'Returns']:
        if dates_as_index:
            statsTable.iloc[3:, :] = statsTable.iloc[3:, :].astype(str) + '%'
        else:
            statsTable.iloc[1:, :] = statsTable.iloc[1:, :].astype(str) + '%'
        statsTable.loc['count', :] = statsTable.loc['count', :].apply('{:.0f}'.format)
    elif dType == 'NumFirms':
        for c in statsTable.columns:
            if dates_as_index:
                statsTable.loc[2:, c] = statsTable.loc[:, c].apply('{:.0f}'.format)
            else:
                statsTable.loc[:, c] = statsTable.loc[:, c].apply('{:.0f}'.format)
    else:
        statsTable.loc['count', :] = statsTable.loc['count', :].apply('{:.0f}'.format)
    print('    *********************** Observation frequency: '+dFreq+' ************************')
    print(statsTable, '\n')
    return statsTable