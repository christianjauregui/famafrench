.. _applications:

**************************
Applications and Examples
**************************

.. module:: famafrench
   :noindex:

.. currentmodule:: famafrench


Below are some examples of how the package can be used to construct datasets from `Ken French's online library <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>`_ as well as many other similar datasets. Throughout, the constructed datasets are compared to those provided by `Ken French <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html>`_.

Let's start by importing this package as well as other required Python libraries:

.. code-block:: ipython
   
   In [1]: import datetime as dt
   In [2]: import famafrench.famafrench as ff


Let's create all our datasets from 1950 to the present, or the most recent date for which there is stock returns data. We set :attr:`runQuery` to ``True`` and query all datafiles directly from `wrds-cloud`. 

.. code-block:: ipython

   In [3]: startDate = dt.date(1950, 1, 1)
   In [4]: endDate = dt.date.today()
   In [5]: runQuery = True



Fama-French 3 Factors
######################


Fama-French 3 Factors : Daily
*****************************

.. code-block:: ipython
   
   In [6]: ffFreq = 'D'
   In [7]: ffsortCharac = ['ME', 'BM']
   In [8]: ffFactors = ['MKT-RF', 'SMB', 'HML']
   In [9]: ff3_D = ff.FamaFrench(runQuery=runQuery, freqType=ffFreq, sortCharacsId=ffsortCharac, factorsId=ffFactors) 
   
   In [10]: # Summary statistics
	    ff3_D.getFamaFrenchStats(dataType='Factors', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate)
   
   CRSP (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [02:45<00:00, 82.68s/it]
   Historical risk-free interest rate (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: D ************************
                     mkt      mkt-rf         smb         hml
   startdate  1970-01-02  1970-01-02  1970-01-02  1970-01-02
   enddate    2020-02-28  2020-02-28  2020-02-28  2020-02-28
   count           12653       12653       12653       12653
   mean            0.04%       0.03%        0.0%       0.02%
   std             1.02%       1.02%       0.55%       0.55%
   min           -17.45%     -17.47%     -11.64%      -4.39%
   1%             -2.77%      -2.78%       -1.4%       -1.5%
   10%            -1.05%      -1.07%       -0.6%      -0.52%
   25%            -0.41%      -0.43%      -0.29%      -0.24%
   50%             0.07%       0.05%       0.02%       0.01%
   75%             0.54%       0.53%        0.3%       0.26%
   90%              1.1%       1.08%        0.6%       0.56%
   99%             2.75%       2.72%        1.4%       1.64%
   max            11.36%      11.36%       6.27%       4.91%
   skew           -0.53%      -0.52%      -0.97%       0.32%
   kurt           14.53%      14.53%      21.77%       9.86%
   mad             0.69%        0.7%       0.39%       0.36%

   [17 rows x 6 columns] 
   
   In [11]: # Compare daily Fama-French 3 factors constructed here to those provided in Ken French's online library 	   
            _, _, _, = ff3_D.comparePortfolios('Factors', ffFreq, startDate, endDate)

   CRSP (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [03:30<00:00, 105.19s/it]
   Historical risk-free interest rate (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [03:03<00:00, 91.90s/it]
   *********************************** Factor Returns: 1970-01-02 to 2020-02-28 ***********************************
       
      *********************** Observation frequency: D ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    smb    hml
   corr:  1.0     1.0  0.976  0.963 
   
   Fama-French factors: Average matrix:
                          mkt        mkt-rf         smb           hml
   [wrds, kflib]:  [0.04, 0.04]  [0.03, 0.03]  [0.0, 0.0]  [0.02, 0.02] 
   
   Fama-French factors: Std Deviation matrix:
                             mkt        mkt-rf           smb           hml
   [wrds, kflib]:  [1.02, 1.02]  [1.02, 1.02]  [0.55, 0.54]  [0.55, 0.52] 
   
   Elapsed time:  169.73  seconds.



Fama-French 3 Factors : Annual
******************************

.. code-block:: ipython
   
   In [6]: ffFreq = 'A'
   In [7]: ffsortCharac = ['ME', 'BM']
   In [8]: ffFactors = ['MKT-RF', 'SMB', 'HML']
   In [9]: ff3_A = ff.FamaFrench(runQuery=runQuery, freqType=ffFreq, sortCharacsId=ffsortCharac, factorsId=ffFactors) 

   In [10]: # Summary statistics
	    ff3_A.getFamaFrenchStats(dataType='Factors', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [00:04<00:00,  2.38s/it]
   Historical risk-free interest rate (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   **************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: A ************************
                     mkt      mkt-rf         smb         hml
   startdate  1970-12-31  1970-12-31  1970-12-31  1970-12-31
   enddate    2020-12-31  2020-12-31  2020-12-31  2020-12-31
   count              51          51          50          50
   mean           11.67%       7.07%       1.49%       4.76%
   std            17.63%       17.8%      11.33%      14.48%
   min           -36.65%     -38.24%     -25.74%     -30.85%
   1%            -32.19%     -36.99%      -24.2%     -28.01%
   10%           -11.24%      -17.6%     -10.61%     -11.57%
   25%             0.04%       -5.1%      -7.31%      -4.62%
   50%            15.41%      10.73%       0.42%       6.44%
   75%            24.58%       20.3%       8.84%      14.79%
   90%            32.58%       28.3%      15.29%      21.41%
   99%            37.51%      33.82%      24.86%      36.02%
   max            38.23%      35.22%      26.79%      47.04%
   skew           -0.65%      -0.65%      -0.02%       0.04%
   kurt             0.0%      -0.07%      -0.22%       0.59%
   mad            14.26%      14.44%        9.3%       11.5% 

   In [11]: # Compare annual Fama-French 3 factors constructed here to those provided in Ken French's online library 	   
            _, _, _, = ff3_A.comparePortfolios(kfType='Factors', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate)

   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [00:05<00:00,  2.79s/it]
   *********************************** Factor Returns: 1970-12-31 to 2019-12-31 ***********************************
       
      *********************** Observation frequency: A ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    smb    hml
   corr:  1.0     1.0  0.995  0.977 
   
   Fama-French factors: Average matrix:
                               mkt        mkt-rf           smb           hml
   [wrds, kflib]:  [12.07, 12.07]  [7.37, 7.37]  [1.49, 1.59]  [4.76, 4.28] 

   Fama-French factors: Std Deviation matrix:
                              mkt          mkt-rf            smb             hml
   [wrds, kflib]:  [17.59, 17.6]  [17.84, 17.86]  [11.33, 11.5]  [14.48, 14.36] 

   Elapsed time:  7.354  seconds.


Fama-French 5 Factors
######################

Fama-French 5 Factors : Daily
*****************************

.. code-block:: ipython
   
   In [6]: ffFreq = 'D'
   In [7]: ffsortCharac = ['ME', 'BM']
   In [8]: ffFactors = ['MKT-RF', 'SMB', 'HML', 'RMW', 'CMA']
   In [9]: ffportCharac = ['ME', 'BM', 'OP', 'INV']
   In [10]: ff5_D = ff.FamaFrench(runQuery=runQuery, freqType=ffFreq, sortCharacsId=ffsortCharac, factorsId=ffFactors, mainCharacsId=ffportCharac) 

   In [11]: # Summary statistics
	    ff5_D.getFamaFrenchStats(dataType='Factors', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate)

   CRSP (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [08:02<00:00, 96.59s/it] 
   Historical risk-free interest rate (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: D ************************
                     mkt      mkt-rf  ...         rmw         hml
   startdate  1970-01-02  1970-01-02  ...  1970-01-02  1970-01-02
   enddate    2020-02-28  2020-02-28  ...  2020-02-28  2020-02-28
   count           12653       12653  ...       12653       12653
   mean            0.04%       0.03%  ...       0.01%       0.02%
   std             1.02%       1.02%  ...       0.43%       0.55%
   min           -17.45%     -17.47%  ...      -7.67%      -4.39%
   1%             -2.77%      -2.78%  ...      -1.17%       -1.5%
   10%            -1.05%      -1.07%  ...      -0.37%      -0.52%
   25%            -0.41%      -0.43%  ...      -0.17%      -0.24%
   50%             0.07%       0.05%  ...       0.01%       0.01%
   75%             0.54%       0.53%  ...       0.19%       0.26%
   90%              1.1%       1.08%  ...       0.41%       0.56%
   99%             2.75%       2.72%  ...       1.25%       1.64%
   max            11.36%      11.36%  ...       6.01%       4.91%
   skew           -0.53%      -0.52%  ...       -0.0%       0.32%
   kurt           14.53%      14.53%  ...      22.14%       9.86%
   mad             0.69%        0.7%  ...       0.27%       0.36%
   
   [17 rows x 6 columns] 
   
   In [12]: # Compare daily Fama-French 5 factors constructed here to those provided in Ken French's online library 	   
            _, _, _, = ff5_D.comparePortfolios(kfType='Factors', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate)

   CRSP (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [08:00<00:00, 96.11s/it]
   Historical risk-free interest rate (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [08:34<00:00, 102.94s/it]
   *********************************** Factor Returns: 1970-01-02 to 2020-02-28 ***********************************
       *********************** Observation frequency: D ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    smb    cma    rmw    hml
   corr:  1.0     1.0  0.976  0.917  0.902  0.963 

   Fama-French factors: Average matrix:
                             mkt        mkt-rf  ...           rmw           hml
   [wrds, kflib]:  [0.04, 0.04]  [0.03, 0.03]  ...  [0.01, 0.01]  [0.02, 0.02]
   [1 rows x 6 columns] 

   Fama-French factors: Std Deviation matrix:
                             mkt        mkt-rf  ...           rmw           hml
   [wrds, kflib]:  [1.02, 1.02]  [1.02, 1.02]  ...  [0.43, 0.38]  [0.55, 0.52]
   [1 rows x 6 columns] 

   Elapsed time:  518.612  seconds.


Fama-French 5 Factors : Monthly
*******************************

.. code-block:: ipython
   
   In [6]: ffFreq = 'M'
   In [7]: ffsortCharac = ['ME', 'BM']
   In [8]: ffFactors = ['MKT-RF', 'SMB', 'HML', 'RMW', 'CMA']
   In [9]: ffportCharac = ['ME', 'BM', 'OP', 'INV']
   In [10]: ff5_M = ff.FamaFrench(runQuery=runQuery, freqType=ffFreq, sortCharacsId=ffsortCharac, factorsId=ffFactors, mainCharacsId=ffportCharac) 

   In [11]: # Summary statistics
	    ff5_M.getFamaFrenchStats(dataType='Factors', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [00:14<00:00,  2.88s/it]
   Historical risk-free interest rate (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: M ************************
                     mkt      mkt-rf  ...         hml         cma
   startdate  1970-01-31  1970-01-31  ...  1970-01-31  1970-01-31
   enddate    2020-02-29  2020-02-29  ...  2020-02-29  2020-02-29
   count             602         602  ...         602         602
   mean            0.93%       0.55%  ...       0.31%       0.28%
   std              4.5%       4.51%  ...       3.01%       1.93%
   min           -22.66%     -23.26%  ...      -11.9%      -7.08%
   1%            -10.96%     -11.76%  ...      -8.43%      -4.38%
   10%            -4.53%      -4.94%  ...      -2.87%      -1.89%
   25%            -1.71%       -2.0%  ...      -1.45%      -0.93%
   50%             1.28%       0.94%  ...       0.24%       0.17%
   75%              3.9%        3.5%  ...       1.79%       1.43%
   90%             6.06%       5.57%  ...       3.95%       2.67%
   99%            11.35%      11.14%  ...       8.33%       5.72%
   max             16.6%      16.09%  ...      12.43%       8.55%
   skew           -0.54%      -0.56%  ...       0.06%       0.33%
   kurt            1.92%       1.91%  ...       2.13%       1.43%
   mad             3.41%       3.43%  ...        2.2%       1.47%

   [17 rows x 6 columns] 
   
   In [12]: # Compare monthly Fama-French 5 factors constructed here to those provided in Ken French's online library 	   
            _, _, _, = ff5_M.comparePortfolios(kfType='Factors', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate)

   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [00:14<00:00,  2.84s/it]
   *********************************** Factor Returns: 1970-01-31 to 2020-02-29 ***********************************
   
       *********************** Observation frequency: M ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    smb    rmw    hml    cma
   corr:  1.0     1.0  0.984  0.975  0.977  0.957 

   Fama-French factors: Average matrix:
                             mkt        mkt-rf  ...          hml           cma
   [wrds, kflib]:  [0.93, 0.93]  [0.55, 0.55]  ...  [0.31, 0.3]  [0.28, 0.31]

   [1 rows x 6 columns] 

   Fama-French factors: Std Deviation matrix:
                           mkt        mkt-rf  ...           hml           cma
   [wrds, kflib]:  [4.5, 4.5]  [4.51, 4.51]  ...  [3.01, 2.92]  [1.93, 1.99]

   [1 rows x 6 columns] 

   Elapsed time:  15.183  seconds.


Fama-French 5 Factors : Annual
*******************************

.. code-block:: ipython
   
   In [6]: ffFreq = 'A'
   In [7]: ffsortCharac = ['ME', 'BM']
   In [8]: ffFactors = ['MKT-RF', 'SMB', 'HML', 'RMW', 'CMA']
   In [9]: ffportCharac = ['ME', 'BM', 'OP', 'INV']
   In [10]: ff5_A = ff.FamaFrench(runQuery=runQuery, freqType=ffFreq, sortCharacsId=ffsortCharac, factorsId=ffFactors, mainCharacsId=ffportCharac) 

   In [11]: # Summary statistics
	    ff5_A.getFamaFrenchStats(dataType='Factors', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [00:14<00:00,  2.92s/it]
   Historical risk-free interest rate (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: A ************************
                     mkt      mkt-rf  ...         rmw         cma
   startdate  1970-12-31  1970-12-31  ...  1970-12-31  1970-12-31
   enddate    2020-12-31  2020-12-31  ...  2020-12-31  2020-12-31
   count              51          51  ...          50          50
   mean           11.67%       7.07%  ...       3.51%       3.74%
   std            17.63%       17.8%  ...       9.34%       8.82%
   min           -36.65%     -38.24%  ...     -25.27%     -14.95%
   1%            -32.19%     -36.99%  ...     -23.54%     -13.26%
   10%           -11.24%      -17.6%  ...      -6.06%      -7.29%
   25%             0.04%       -5.1%  ...      -0.87%      -1.99%
   50%            15.41%      10.73%  ...       3.35%       3.15%
   75%            24.58%       20.3%  ...       8.66%       8.97%
   90%            32.58%       28.3%  ...      14.68%      14.68%
   99%            37.51%      33.82%  ...      22.08%      25.39%
   max            38.23%      35.22%  ...       22.2%       26.0%
   skew           -0.65%      -0.65%  ...       -0.6%       0.34%
   kurt             0.0%      -0.07%  ...       1.56%        0.2%
   mad            14.26%      14.44%  ...       6.88%       6.88%

   [17 rows x 6 columns] 
   
   In [12]: # Compare annual Fama-French 5 factors constructed here to those provided in Ken French's online library 	   
            _, _, _, = ff5_A.comparePortfolios(kfType='Factors', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [00:16<00:00,  3.32s/it]
   Historical risk-free interest rate (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [00:17<00:00,  3.56s/it]
   *********************************** Factor Returns: 1970-12-31 to 2019-12-31 ***********************************
   
       *********************** Observation frequency: A ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    smb    hml    rmw    cma
   corr:  1.0     1.0  0.996  0.978  0.986  0.977 

   Fama-French factors: Average matrix:
                               mkt        mkt-rf  ...           rmw           cma
   [wrds, kflib]:  [12.07, 12.07]  [7.37, 7.37]  ...  [3.42, 3.64]  [3.88, 3.98]

   [1 rows x 6 columns] 

   Fama-French factors: Std Deviation matrix:
                              mkt          mkt-rf  ...           rmw           cma
   [wrds, kflib]:  [17.59, 17.6]  [17.84, 17.86]  ...  [9.43, 9.54]  [9.21, 9.76]

   [1 rows x 6 columns] 

   Elapsed time:  18.957  seconds.


Momentum, Short-Term Reversal, and Long-Term Reversal Factor
#############################################################

``MOM, ``ST_Rev``, and ``LT_Rev`` : Daily
******************************************

.. code-block:: ipython
   


``MOM, ``ST_Rev``, and ``LT_Rev`` : Monthly
********************************************

.. code-block:: ipython
   


Portfolios Sorted on `Size` ``ME``
##################################


Portfolios Sorted on `Size` ``ME`` : Daily
********************************************

**(3 x 1) Sorts**:


**(5 x 1) Quintile Sorts**:


**(10 x 1) Decile Sorts**:



Portfolios Sorted on `Size` ``ME`` : Monthly
**********************************************

**(3 x 1) Sorts**:


**(5 x 1) Quintile Sorts**:


**(10 x 1) Decile Sorts**:




Portfolios Sorted on `Size` ``ME`` : Annual
**********************************************

**(3 x 1) Sorts**:


**(5 x 1) Quintile Sorts**:


**(10 x 1) Decile Sorts**:



Portfolios Sorted on `Book-to-Market` ``BM``
#############################################




Portfolios Sorted on `Operating Profitability` ``OP``
######################################################




Portfolios Sorted on `Investment` ``INV``
##########################################


    
