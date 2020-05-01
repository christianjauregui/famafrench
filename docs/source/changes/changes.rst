.. _changes:

*************
Change Log
*************

.. module:: famafrench
   :noindex:
.. currentmodule:: famafrench

Version 0 (Beta)
################

Release 0.1.1
=============
Initial release as of April 25, 2020. 

Release 0.1.2
=============
Current release as of May 1, 2020.

   * Resolved ``FutureWarning`` for deprecated ``pandas.np`` module used to fill missing values (i.e. ``nan`` or ``None``): replaced the use of ``value=pd.np.nan`` w/ ``value=np.nan`` in :obj:`pandas.DataFrame.fillna`.
   * Fixed a bug that used the wrong instance method on a :class:`pandas.DatetimeIndex`. To check if a :class:`pandas.DatetimeIndex` value landed on a Saturday or Sunday, incorrect use of ``pandas.DatetimeIndex.weekday_name`` is replaced w/ :meth:`pandas.DatetimeIndex.day_name()`. The aforementioned is required when comparing datasets constructed at a weekly frequency to those from Ken French's online library (e.g. `Weekly Fama-French 3 Factors <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html>`_).
   * Fixed a bug that **did not** exclude data for an `incomplete` final calendar year in the construction of annual datasets. For example, annual datasets constructed from a given start date to the present should end in 2019, not 2020. 
   * Added options to construct portfolios based on sorts not included in Ken French's online data library. A single anomaly characteristic or multiple anomaly characteristics can now be split into 4 (i.e. quartiles), 6, 8, 20, 25, or 100 (i.e. percentiles) buckets. 
   


   