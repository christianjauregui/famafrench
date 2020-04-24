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

``MOM``, ``ST_Rev``, and ``LT_Rev`` : Daily
********************************************

.. code-block:: ipython
   
   In [6]: ffFreq = 'D'
   In [7]: ffsortCharac = ['ME', 'PRIOR_2_12']
   In [8]: ffFactors = ['MKT-RF', 'MOM', 'ST_Rev', 'LT_Rev']
   In [9]: ffportCharac = ['ME', 'PRIOR_2_12', 'PRIOR_1_1', 'PRIOR_13_60']
   In [10]: ffprior_D = ff.FamaFrench(runQuery=runQuery, freqType=ffFreq, sortCharacsId=ffsortCharac, factorsId=ffFactors, mainCharacsId=ffportCharac) 

   
   In [11]: # Summary statistics
	    ffprior_D.getFamaFrenchStats(dataType='Factors', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate)

   CRSP (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (daily) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 4/4 [24:44<00:00, 371.14s/it]
   Historical risk-free interest rate (daily) dataset currently NOT saved locally. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: D ************************
                     mkt      mkt-rf      st_rev      lt_rev         mom
   startdate  1950-01-03  1950-01-03  1951-07-02  1951-07-02  1951-07-02
   enddate    2020-02-28  2020-02-28  2020-02-28  2020-02-28  2020-02-28
   count           17653       17653       17279       17279       17279
   mean            0.05%       0.03%        0.1%        0.0%       0.03%
   std             0.93%       0.93%       0.66%       0.43%       0.67%
   min           -17.45%     -17.47%      -6.86%      -4.28%      -7.79%
   1%             -2.55%      -2.56%       -1.6%      -1.11%      -2.01%
   10%            -0.95%      -0.96%      -0.47%      -0.46%      -0.61%
   25%            -0.36%      -0.38%      -0.17%      -0.22%      -0.23%
   50%             0.07%       0.06%       0.08%       -0.0%       0.06%
   75%             0.49%       0.47%       0.34%       0.22%       0.33%
   90%             0.97%       0.95%       0.68%       0.48%       0.66%
   99%             2.44%       2.42%       2.13%        1.2%       1.83%
   max            11.36%      11.36%       10.2%       4.41%        6.9%
   skew           -0.57%      -0.57%       1.71%      -0.12%      -0.88%
   kurt           16.24%      16.24%      26.23%       7.39%      14.15%
   mad             0.62%       0.62%        0.4%        0.3%       0.43%    
   
   In [12]: # Compare daily Fama-French factors based on prior returns constructed here to those provided in Ken French's online library
	    _, _, _, = ffprior_D.comparePortfolios(dataType='Factors', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate)


``MOM``, ``ST_Rev``, and ``LT_Rev`` : Monthly
**********************************************

.. code-block:: ipython

   In [6]: ffFreq = 'M'
   In [7]: ffsortCharac = ['ME', 'PRIOR_2_12']
   In [8]: ffFactors = ['MKT-RF', 'MOM', 'ST_Rev', 'LT_Rev']
   In [9]: ffportCharac = ['ME', 'PRIOR_2_12', 'PRIOR_1_1', 'PRIOR_13_60']
   In [10]: ffprior_M = ff.FamaFrench(runQuery=runQuery, freqType=ffFreq, sortCharacsId=ffsortCharac, factorsId=ffFactors, mainCharacsId=ffportCharac) 

   
   In [11]: # Summary statistics
	    ffprior_M.getFamaFrenchStats(dataType='Factors', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 4/4 [00:25<00:00,  6.44s/it]
   Historical risk-free interest rate (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: M ************************
                     mkt      mkt-rf         mom      st_rev      lt_rev
   startdate  1950-01-31  1950-01-31  1951-07-31  1951-07-31  1951-07-31
   enddate    2020-02-29  2020-02-29  2020-02-29  2020-02-29  2020-02-29
   count             842         842         824         824         824
   mean            0.97%       0.64%       0.69%       0.55%       0.11%
   std             4.22%       4.24%       3.91%       2.89%       2.47%
   min           -22.66%     -23.26%     -33.02%     -14.26%     -14.31%
   1%            -10.17%     -10.52%      -9.54%      -7.17%      -5.36%
   10%            -4.26%      -4.76%      -3.42%      -2.22%      -2.62%
   25%            -1.58%      -1.89%      -0.96%      -0.96%      -1.34%
   50%             1.33%       1.05%       0.78%       0.42%      -0.04%
   75%             3.71%       3.42%       2.72%       1.87%       1.51%
   90%             5.68%       5.25%       4.54%       3.42%        3.0%
   99%            11.09%      10.59%       9.68%      10.23%       6.75%
   max             16.6%      16.09%       18.3%      16.74%      15.64%
   skew           -0.53%      -0.55%       -1.3%       0.43%       0.47%
   kurt            1.92%       1.91%      10.51%       5.81%       4.11%
   mad             3.22%       3.23%       2.66%       1.98%       1.83% 


   In [12]: # Compare monthly Fama-French factors based on prior returns constructed here to those provided in Ken French's online library
	    _, _, _, = ffprior_M.comparePortfolios(dataType='Factors', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate)
	    
   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 4/4 [00:26<00:00,  6.71s/it]
   Historical risk-free interest rate (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 4/4 [00:25<00:00,  6.25s/it]
   *********************************** Factor Returns: 1950-01-31 to 2020-02-29 ***********************************
    
       *********************** Observation frequency: M ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    mom  st_rev  lt_rev
   corr:  1.0     1.0  0.986   0.977    0.95 

   Fama-French factors: Average matrix:
                             mkt        mkt-rf  ...        st_rev        lt_rev
   [wrds, kflib]:  [0.97, 0.96]  [0.64, 0.62]  ...  [0.55, 0.52]  [0.12, 0.12]

   [1 rows x 5 columns] 

   Fama-French factors: Std Deviation matrix:
                             mkt        mkt-rf  ...        st_rev        lt_rev

   [wrds, kflib]:  [4.22, 4.25]  [4.24, 4.27]  ...  [2.89, 2.89]  [2.48, 2.42]
    
   [1 rows x 5 columns] 

   Elapsed time:  26.804  seconds.



``MOM``, ``ST_Rev``, and ``LT_Rev`` : Annual
**********************************************

.. code-block:: ipython

   In [6]: ffFreq = 'A'
   In [7]: ffsortCharac = ['ME', 'PRIOR_2_12']
   In [8]: ffFactors = ['MKT-RF', 'MOM', 'ST_Rev', 'LT_Rev']
   In [9]: ffportCharac = ['ME', 'PRIOR_2_12', 'PRIOR_1_1', 'PRIOR_13_60']
   In [10]: ffprior_A = ff.FamaFrench(runQuery=runQuery, freqType=ffFreq, sortCharacsId=ffsortCharac, factorsId=ffFactors, mainCharacsId=ffportCharac) 

   
   In [11]: # Summary statistics
	    ffprior_A.getFamaFrenchStats(dataType='Factors', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 4/4 [00:31<00:00,  7.88s/it]
   Historical risk-free interest rate (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: A ************************
                     mkt      mkt-rf         mom      st_rev      lt_rev
   startdate  1950-12-31  1950-12-31  1953-12-31  1953-12-31  1953-12-31
   enddate    2020-12-31  2020-12-31  2020-12-31  2020-12-31  2020-12-31
   count              72          72          67          67          67
   mean           12.17%       8.11%       8.16%       7.17%       1.47%
   std            17.56%      17.92%       17.1%      11.36%       12.5%
   min           -36.65%     -38.24%     -79.66%     -17.67%     -25.26%
   1%            -30.32%     -36.47%     -43.82%     -16.09%     -21.91%
   10%           -10.17%     -14.96%      -8.28%      -5.06%     -13.29%
   25%             0.05%      -4.63%       1.57%       0.33%      -8.02%
   50%            14.23%      10.71%      10.35%        5.8%       1.57%
   75%            24.95%      20.74%      17.52%      13.37%       8.86%
   90%             32.5%      28.74%      24.17%      18.27%      16.98%
   99%            46.52%      45.18%      37.27%      42.81%      29.01%
   max            50.21%      49.35%      38.24%      44.99%      31.03%
   skew           -0.38%      -0.35%      -2.12%       0.87%       0.27%
   kurt           -0.11%      -0.05%       9.61%       2.15%      -0.26%
   mad            14.17%      14.36%      11.49%        8.3%      10.08% 

   In [12]: # Compare monthly Fama-French factors based on prior returns constructed here to those provided in Ken French's online library
	    _, _, _, = ffprior_A.comparePortfolios(dataType='Factors', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate)
	    
   Constructing Fama-French return factor(s): 100%|██████████| 4/4 [00:30<00:00,  7.54s/it]
   *********************************** Factor Returns: 1950-12-31 to 2019-12-31 ***********************************
    
	*********************** Observation frequency: A ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    mom  st_rev  lt_rev
   corr:  1.0     1.0  0.989   0.969   0.978 

   Fama-French factors: Average matrix:
                               mkt        mkt-rf  ...        st_rev        lt_rev
   [wrds, kflib]:  [12.75, 12.75]  [8.57, 8.57]  ...  [7.17, 7.07]  [1.47, 1.59]

   [1 rows x 5 columns] 

   Fama-French factors: Std Deviation matrix:
                               mkt          mkt-rf  ...          st_rev         lt_rev
   [wrds, kflib]:  [17.46, 17.48]  [17.96, 17.97]  ...  [11.36, 10.82]  [12.5, 12.04]

   [1 rows x 5 columns] 

   Elapsed time:  32.233  seconds.



Portfolios Sorted on `Size` ``ME``
##################################

.. code-block:: ipython

   In [6]: ffFactors, ffsortCharac, ffportCharac = [], ['ME'], ['ME']


Portfolios Sorted on `Size` ``ME`` : Daily
********************************************

.. code-block:: ipython

   In [7]: ffFreq = 'D'
   In [8]: ff_D = ff.FamaFrench(runQuery=runQuery, freqType=ffFreq, sortCharacsId=ffsortCharac, factorsId=ffFactors, mainCharacsId=ffportCharac)

**(3 x 1) Sorts**:

.. code-block:: ipython

   In [9]: sortingDim = [3]    
   In [10]: # Summary statistics
	      ff_D.getFamaFrenchStats(dataType='Returns', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType='vw')
	      ff_D.getFamaFrenchStats(dataType='NumFirms', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
              ff_D.getFamaFrenchStats(dataType='Characs', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
        
   In [11]: # daily portfolios 
            _, _, _, = ff_D.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType='vw')


**(5 x 1) Quintile Sorts**:

.. code-block:: ipython

   In [9]: sortingDim = [5]      
   In [10]: # Summary statistics
	    ff_D.getFamaFrenchStats(dataType='Returns', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType='vw')
	    ff_D.getFamaFrenchStats(dataType='NumFirms', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
            ff_D.getFamaFrenchStats(dataType='Characs', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
        
   In [11]: # daily portfolios 
            _, _, _, = ff_D.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType='vw')


**(10 x 1) Decile Sorts**:

.. code-block:: ipython

   In [9]: sortingDim = [10]      
   In [10]: # Summary statistics
	    ff_D.getFamaFrenchStats(dataType='Returns', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType='vw')
	    ff_D.getFamaFrenchStats(dataType='NumFirms', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
            ff_D.getFamaFrenchStats(dataType='Characs', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
   
   In [11]: # daily portfolios 
            _, _, _, = ff_D.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType='vw')



Portfolios Sorted on `Size` ``ME`` : Monthly
**********************************************

.. code-block:: ipython
   
   In [7]: ffFreq = 'M'
   In [8]: ff_M = ff.FamaFrench(runQuery=runQuery, freqType=ffFreq, sortCharacsId=ffsortCharac, factorsId=ffFactors, mainCharacsId=ffportCharac)

**(3 x 1) Sorts**:

.. code-block:: ipython

   In [9]: sortingDim = [3]      
   In [10]: # Summary statistics
	    ff_M.getFamaFrenchStats(dataType='Returns', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType='vw')
	    ff_M.getFamaFrenchStats(dataType='NumFirms', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
            ff_M.getFamaFrenchStats(dataType='Characs', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** ME (3) ************************************

       *********************** Observation frequency: M ************************
                  me0-30     me30-70    me70-100
   startdate  1951-07-31  1951-07-31  1951-07-31
   enddate    2020-02-29  2020-02-29  2020-02-29
   count             824         824         824
   mean            0.01%       0.01%       0.01%
   std             0.06%       0.05%       0.04%
   min             -0.3%      -0.27%      -0.21%
   1%             -0.14%      -0.12%       -0.1%
   10%            -0.06%      -0.05%      -0.04%
   25%            -0.02%      -0.02%      -0.01%
   50%             0.02%       0.02%       0.01%
   75%             0.05%       0.04%       0.04%
   90%             0.08%       0.07%       0.06%
   99%             0.14%       0.12%       0.11%
   max             0.28%       0.23%       0.18%
   skew           -0.33%      -0.54%      -0.41%
   kurt            2.59%       2.53%       1.74%
   mad             0.04%       0.04%       0.03% 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** ME (3) ************************************
 
      *********************** Observation frequency: M ************************
                  me0-30     me30-70    me70-100
   startdate  1951-07-31  1951-07-31  1951-07-31
   enddate    2020-02-29  2020-02-29  2020-02-29
   count             824         824         824
   mean             2172         723         396
   std              1393         329         150
   min                31          29          20
   1%                102         132          99
   10%               143         191         138
   25%               847         428         293
   50%              2430         838         440
   75%              3305         920         500
   90%              3876        1116         541
   99%              4655        1334         676
   max              4956        1428         718
   skew               -0          -0          -1
   kurt               -1          -1          -0
   mad              1188         279         122 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** ME (3) ************************************
 
     ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: M ************************
   me_port        me0-30     me30-70    me70-100
   startdate  1951-07-31  1951-07-31  1951-07-31
   enddate    2020-02-29  2020-02-29  2020-02-29
   count             824         824         824
   mean            98.04      850.42     10312.5
   std            120.72     1003.63     12782.8
   min             10.83       44.78      445.17
   1%              10.83       44.78      445.17
   10%             14.72      107.55       955.6
   25%             22.32      145.12      1422.6
   50%             37.26       393.6     3246.79
   75%            126.37     1209.45     18281.1
   90%            277.16     2506.54     28415.1
   99%            604.29     4017.67       48861
   max            611.05     4468.11     61026.1
   skew             1.93        1.56        1.55
   kurt             3.75        1.76        2.08
   mad             91.54      787.58     10412.7 

   In [11]: # monthly portfolios 
            _, _, _, = ff_M.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType='vw')
	    _, _, _, = ff_M.comparePortfolios(kfType='NumFirms', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim)
	    _, _, _, = ff_M.comparePortfolios(kfType='Characs', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim)

   *********************************** ME (3) ************************************
       *********************** Observation frequency: M ************************
       ************************* Returns: 1951-07-31 to 2020-02-29 **************************

   Correlation matrix:
           me0-30  me70-100  me30-70
   corr:   0.994     0.997    0.995 

   Average matrix:
                            me0-30        me70-100         me30-70
   [wrds, kflib]:  [1.18%, 1.12%]  [0.95%, 0.94%]  [1.11%, 1.09%] 

   Std Deviation matrix:
                            me0-30        me70-100         me30-70
   [wrds, kflib]:  [5.85%, 5.81%]  [4.12%, 4.13%]  [4.96%, 5.07%] 

   Elapsed time:  6.309  seconds.

   *********************************** ME (3) ************************************
       *********************** Observation frequency: M ************************
       ************************* NumFirms: 1951-07-31 to 2020-02-29 **************************

   Correlation matrix:
           me0-30  me70-100  me30-70
   corr:   0.978     0.911    0.953 

   Average matrix:
                          me0-30    me70-100     me30-70
   [wrds, kflib]:  [2172, 2469]  [396, 448]  [723, 804] 

   Std Deviation matrix:
                          me0-30   me70-100     me30-70
   [wrds, kflib]:  [1393, 1479]  [150, 96]  [329, 266] 

   Elapsed time:  6.268  seconds.

   *********************************** ME (3) ************************************
       *********************** Observation frequency: M ************************
       ************************* (Characteristic: ME): 1951-07-31 to 2020-02-29 ***************************

   Correlation matrix:
           me0-30  me70-100  me30-70
   corr:   0.955     0.989    0.979 
   
   Average matrix:
                            me0-30              me70-100           me30-70
   [wrds, kflib]:  [98.04, 91.55]  [10312.47, 10189.21]  [850.42, 817.22] 

   Std Deviation matrix:
                              me0-30              me70-100            me30-70
   [wrds, kflib]:  [120.72, 109.95]  [12782.78, 12893.69]  [1003.63, 978.37] 

   Elapsed time:  5.401  seconds.


**(5 x 1) Quintile Sorts**:

.. code-block:: ipython

   In [9]: sortingDim = [5]   
   In [10]: # Summary statistics
	    ff_M.getFamaFrenchStats(dataType='Returns', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType='vw')
	    ff_M.getFamaFrenchStats(dataType='NumFirms', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
            ff_M.getFamaFrenchStats(dataType='Characs', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)

   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** ME (5) ************************************

       *********************** Observation frequency: M ************************
                  me0-20     me20-40     me40-60     me60-80    me80-100
   startdate  1951-07-31  1951-07-31  1951-07-31  1951-07-31  1951-07-31
   enddate    2020-02-29  2020-02-29  2020-02-29  2020-02-29  2020-02-29
   count             824         824         824         824         824
   mean            0.01%       0.01%       0.01%       0.01%       0.01%
   std             0.06%       0.06%       0.05%       0.05%       0.04%
   min             -0.3%       -0.3%      -0.27%      -0.25%       -0.2%
   1%             -0.15%      -0.15%      -0.12%      -0.11%       -0.1%
   10%            -0.06%      -0.06%      -0.05%      -0.05%      -0.04%
   25%            -0.02%      -0.02%      -0.02%      -0.02%      -0.01%
   50%             0.02%       0.02%       0.02%       0.01%       0.01%
   75%             0.05%       0.05%       0.04%       0.04%       0.04%
   90%             0.08%       0.08%       0.07%       0.07%       0.06%
   99%             0.15%       0.13%       0.13%       0.12%       0.11%
   max             0.29%       0.26%       0.23%       0.19%       0.18%
   skew           -0.21%      -0.49%      -0.53%      -0.49%      -0.38%
   kurt            2.77%        2.4%       2.41%       2.26%        1.7%
   mad             0.04%       0.04%       0.04%       0.04%       0.03% 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** ME (5) ************************************

       *********************** Observation frequency: M ************************
                  me0-20     me20-40     me40-60     me60-80    me80-100
   startdate  1951-07-31  1951-07-31  1951-07-31  1951-07-31  1951-07-31
   enddate    2020-02-29  2020-02-29  2020-02-29  2020-02-29  2020-02-29
   count             824         824         824         824         824
   mean             1892         505         350         287         256
   std              1239         271         158         116          95
   min                25          15          15          11          14
   1%                 73          59          68          63          70
   10%                99          92          94          92          96
   25%               724         238         216         198         192
   50%              2120         580         402         324         286
   75%              2920         666         438         356         323
   90%              3420         872         530         414         343
   99%              4118         989         669         511         438
   max              4391        1029         711         543         465
   skew               -0          -0          -0          -1          -1
   kurt               -1          -1          -1          -1          -0
   mad              1066         228         132          96          77 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** ME (5) ************************************

      ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: M ************************
   me_port        me0-20     me20-40     me40-60     me60-80    me80-100
   startdate  1951-07-31  1951-07-31  1951-07-31  1951-07-31  1951-07-31
   enddate    2020-02-29  2020-02-29  2020-02-29  2020-02-29  2020-02-29
   count             824         824         824         824         824
   mean            67.55      351.45      834.63     2038.13     14480.3
   std              81.4      416.87     1001.71     2412.76     17836.3
   min              8.61       19.24        39.1       98.06       578.4
   1%               8.61       19.24        39.1       98.06       578.4
   10%             11.36       43.38       99.13      230.85     1260.94
   25%             16.15       58.79      135.22       331.8     1933.43
   50%             26.48      167.59      389.03       921.5     4381.07
   75%             86.78      526.02     1198.73      2971.8     26896.4
   90%            197.77      1021.4      2381.6     5734.64     40281.7
   99%            406.77     1782.62     3921.44     9833.41     69033.1
   max            413.35     1787.57     4971.89       11719     80726.9
   skew              1.9        1.48        1.68        1.66        1.46
   kurt             3.63        1.31        2.62        2.56         1.6
   mad             61.97      331.69      776.58     1876.38     14703.3 


   In [11]: # monthly portfolios 
            _, _, _, = ff_M.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType='vw')
	    _, _, _, = ff_M.comparePortfolios(kfType='NumFirms', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim)
	    _, _, _, = ff_M.comparePortfolios(kfType='Characs', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim)
   
   *********************************** ME (5) ************************************
       *********************** Observation frequency: M ************************
       ************************* Returns: 1951-07-31 to 2020-02-29 **************************

   Correlation matrix:
           me20-40  me80-100  me0-20  me40-60  me60-80
   corr:    0.991     0.997   0.991    0.995    0.993 

   Average matrix:
                           me20-40        me80-100  ...        me40-60        me60-80
   [wrds, kflib]:  [1.15%, 1.12%]  [0.94%, 0.93%]  ...  [1.11%, 1.1%]  [1.1%, 1.07%]

   [1 rows x 5 columns] 

   Std Deviation matrix:
                           me20-40       me80-100  ...         me40-60         me60-80
   [wrds, kflib]:  [5.53%, 5.58%]  [4.1%, 4.09%]  ...  [5.01%, 5.12%]  [4.68%, 4.82%]
   
   [1 rows x 5 columns] 

   Elapsed time:  6.725  seconds.

   *********************************** ME (5) ************************************
       *********************** Observation frequency: M ************************
       ************************* NumFirms: 1951-07-31 to 2020-02-29 **************************

   Correlation matrix:
           me20-40  me80-100  me0-20  me40-60  me60-80
   corr:    0.973     0.899   0.977    0.948    0.926 

   Average matrix:
                       me20-40    me80-100        me0-20     me40-60     me60-80
   [wrds, kflib]:  [505, 558]  [256, 291]  [1892, 2160]  [350, 390]  [287, 324] 

   Std Deviation matrix:
                       me20-40  me80-100        me0-20     me40-60    me60-80
   [wrds, kflib]:  [271, 245]  [95, 59]  [1239, 1340]  [158, 127]  [116, 81] 

   Elapsed time:  5.478  seconds.

   *********************************** ME (5) ************************************
       *********************** Observation frequency: M ************************
       ************************* (Characteristic: ME): 1951-07-31 to 2020-02-29 ***************************

   Correlation matrix:
           me20-40  me80-100  me0-20  me40-60  me60-80
   corr:    0.978     0.991   0.943    0.968    0.978 

   Average matrix:
                             me20-40  ...             me60-80

   [wrds, kflib]:  [351.45, 338.05]  ...  [2038.13, 1970.45]
   
   [1 rows x 5 columns] 

   Std Deviation matrix:
                             me20-40  ...            me60-80
   [wrds, kflib]:  [416.87, 405.33]  ...  [2412.76, 2347.4]


   [1 rows x 5 columns] 

   Elapsed time:  5.629  seconds.

**(10 x 1) Decile Sorts**:

.. code-block:: ipython

   In [9]: sortingDim = [10]   
   In [10]: # Summary statistics
	    ff_M.getFamaFrenchStats(dataType='Returns', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType='vw')
	    ff_M.getFamaFrenchStats(dataType='NumFirms', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
            ff_M.getFamaFrenchStats(dataType='Characs', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)

   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** ME (10) ************************************
   
    *********************** Observation frequency: M ************************
                  me0-10     me10-20  ...     me80-90    me90-100
   startdate  1951-07-31  1951-07-31  ...  1951-07-31  1951-07-31
   enddate    2020-02-29  2020-02-29  ...  2020-02-29  2020-02-29
   count             824         824  ...         824         824
   mean            0.01%       0.01%  ...       0.01%       0.01%
   std             0.06%       0.06%  ...       0.04%       0.04%
   min             -0.3%      -0.31%  ...      -0.22%       -0.2%
   1%             -0.16%      -0.14%  ...       -0.1%       -0.1%
   10%            -0.06%      -0.06%  ...      -0.04%      -0.04%
   25%            -0.02%      -0.02%  ...      -0.02%      -0.01%
   50%             0.01%       0.01%  ...       0.01%       0.01%
   75%             0.05%       0.05%  ...       0.04%       0.03%
   90%             0.08%       0.08%  ...       0.06%       0.05%
   99%             0.17%       0.16%  ...       0.11%       0.11%
   max             0.31%        0.3%  ...       0.18%       0.18%
   skew           -0.14%      -0.21%  ...      -0.42%      -0.36%
   kurt            2.94%       2.56%  ...       2.08%        1.6%
   mad             0.04%       0.05%  ...       0.03%       0.03%

   [17 rows x 10 columns] 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** ME (10) ************************************
    
   *********************** Observation frequency: M ************************
                  me0-10     me10-20  ...     me80-90    me90-100
   startdate  1951-07-31  1951-07-31  ...  1951-07-31  1951-07-31
   enddate    2020-02-29  2020-02-29  ...  2020-02-29  2020-02-29
   count             824         824  ...         824         824
   mean             1485         407  ...         130         126
   std               989         265  ...          49          45
   min                19           6  ...           9           5
   1%                 33          40  ...          36          34
   10%                49          48  ...          48          48
   25%               563         162  ...          95          97
   50%              1654         413  ...         144         141
   75%              2312         567  ...         164         156
   90%              2749         778  ...         179         168
   99%              3173        1024  ...         225         213
   max              3368        1052  ...         241         224
   skew               -0           0  ...          -1          -1
   kurt               -1          -1  ...          -0          -0

   mad               863         214  ...          40          37

   [17 rows x 10 columns] 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** ME (10) ************************************
   
   ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: M ************************
   me_port        me0-10     me10-20  ...     me80-90    me90-100
   startdate  1951-07-31  1951-07-31  ...  1951-07-31  1951-07-31
   enddate    2020-02-29  2020-02-29  ...  2020-02-29  2020-02-29
   count             824         824  ...         824         824
   mean            40.39      154.28  ...      5062.7     24674.1
   std             47.09      183.16  ...     6212.28     31341.9
   min              5.59       11.11  ...      215.91       962.2
   1%               5.59       11.11  ...      215.91       962.2
   10%              8.17       20.29  ...      459.37     2122.34
   25%             10.83       29.03  ...       684.2     3160.34
   50%             17.47       69.27  ...     2044.56     6704.41
   75%             48.52      228.78  ...     8061.98     46122.2
   90%            114.21      464.07  ...     14395.2     66496.7
   99%             213.2      834.97  ...     22621.6      113340
   max            224.47      838.48  ...     32120.8      168218
   skew             1.87        1.58  ...        1.68        1.72
   kurt             3.22         1.8  ...        2.89        3.41
   mad             35.78      144.44  ...     4894.66     25470.4

   [17 rows x 10 columns] 
   
   In [11]: # monthly portfolios 
            _, _, _, = ff_M.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType='vw')
	    _, _, _, = ff_M.comparePortfolios(kfType='NumFirms', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim)
	    _, _, _, = ff_M.comparePortfolios(kfType='Characs', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim)

   *********************************** ME (10) ************************************
       *********************** Observation frequency: M ************************
       ************************* Returns: 1951-07-31 to 2020-02-29 **************************

   Correlation matrix:
           me30-40  me0-10  me90-100  me20-30  ...  me80-90  me40-50  me60-70  me70-80
   corr:    0.986   0.984     0.996    0.989  ...    0.992    0.988    0.988    0.987

   [1 rows x 10 columns] 
   
   Average matrix:
                          me30-40        me0-10  ...        me60-70        me70-80
   [wrds, kflib]:  [1.14%, 1.1%]  [1.2%, 1.1%]  ...  [1.1%, 1.08%]  [1.1%, 1.06%]

   [1 rows x 10 columns] 

   Std Deviation matrix:
                           me30-40          me0-10  ...         me60-70         me70-80
   [wrds, kflib]:  [5.46%, 5.51%]  [6.06%, 5.98%]  ...  [4.84%, 4.93%]  [4.65%, 4.78%]

   [1 rows x 10 columns] 

   Elapsed time:  5.44  seconds.

   *********************************** ME (10) ************************************
       *********************** Observation frequency: M ************************
       ************************* NumFirms: 1951-07-31 to 2020-02-29 **************************

   Correlation matrix:
           me30-40  me0-10  me90-100  me20-30  ...  me80-90  me40-50  me60-70  me70-80
   corr:    0.963   0.976     0.891    0.976  ...    0.903    0.951    0.923    0.925

   [1 rows x 10 columns] 

   Average matrix:
                       me30-40        me0-10  ...     me60-70     me70-80
   [wrds, kflib]:  [226, 248]  [1485, 1706]  ...  [147, 166]  [140, 158]
  
   [1 rows x 10 columns] 

   Std Deviation matrix:
                      me30-40       me0-10  me90-100  ...   me40-50   me60-70   me70-80
   [wrds, kflib]:  [113, 98]  [989, 1101]  [45, 27]  ...  [89, 73]  [61, 44]  [56, 38]

   [1 rows x 10 columns] 

   Elapsed time:  5.427  seconds.

   *********************************** ME (10) ************************************
       *********************** Observation frequency: M ************************
       ************************* (Characteristic: ME): 1951-07-31 to 2020-02-29 ***************************

   Correlation matrix:
           me30-40  me0-10  me90-100  me20-30  ...  me80-90  me40-50  me60-70  me70-80
   corr:    0.982   0.923     0.983    0.977  ...    0.978     0.97    0.982    0.979

   [1 rows x 10 columns] 

   Average matrix:
                             me30-40  ...             me70-80
   [wrds, kflib]:  [440.84, 425.56]  ...  [2568.75, 2498.92]

   [1 rows x 10 columns] 

   Std Deviation matrix:
                             me30-40  ...             me70-80
   [wrds, kflib]:  [519.11, 511.26]  ...  [3058.66, 3004.56]

   [1 rows x 10 columns] 

   Elapsed time:  5.276  seconds.


Portfolios Sorted on `Size` ``ME`` : Annual
**********************************************

.. code-block:: ipython

   In [7]: ffFreq = 'A'
   In [8]: ff_A = ff.FamaFrench(runQuery=runQuery, freqType=ffFreq, sortCharacsId=ffsortCharac, factorsId=ffFactors, mainCharacsId=ffportCharac)

**(3 x 1) Sorts**:

.. code-block:: ipython

   In [9]: sortingDim = [3]      
   In [10]: # Summary statistics
	    ff_A.getFamaFrenchStats(dataType='Returns', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType='vw')
	    ff_A.getFamaFrenchStats(dataType='NumFirms', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
            ff_A.getFamaFrenchStats(dataType='Characs', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...

   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** ME (3) ************************************

       *********************** Observation frequency: A ************************
                  me0-30     me30-70    me70-100
   startdate  1953-12-31  1953-12-31  1953-12-31
   enddate    2019-12-31  2019-12-31  2019-12-31
   count              67          67          67
   mean            0.16%       0.14%       0.12%
   std             0.26%        0.2%       0.17%
   min            -0.37%      -0.35%      -0.37%
   1%             -0.36%      -0.31%      -0.31%
   10%            -0.13%       -0.1%      -0.09%
   25%            -0.05%       0.01%       0.02%
   50%             0.19%       0.17%       0.13%
   75%             0.33%       0.27%       0.23%
   90%             0.47%       0.42%       0.33%
   99%             0.77%       0.54%       0.44%
   max             0.92%       0.55%       0.49%
   skew            0.29%      -0.18%      -0.44%
   kurt            0.12%       -0.1%       0.15%
   mad             0.21%       0.16%       0.14% 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** ME (3) ************************************
       *********************** Observation frequency: A ************************
                  me0-30     me30-70    me70-100
   startdate  1953-12-31  1953-12-31  1953-12-31
   enddate    2019-12-31  2019-12-31  2019-12-31
   count              67          67          67
   mean             2221         738         405
   std              1372         317         142
   min               115         181         138
   1%                122         182         138
   10%               149         197         147
   25%               892         464         317
   50%              2454         841         439
   75%              3330         915         499
   90%              3786        1088         539
   99%              4557        1259         646
   max              4577        1273         669
   skew               -0          -0          -1
   kurt               -1          -1          -0
   mad              1158         265         114 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** ME (3) ************************************
   
      ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: A ************************
   me_port        me0-30     me30-70    me70-100
   startdate  1953-12-31  1953-12-31  1953-12-31
   enddate    2019-12-31  2019-12-31  2019-12-31
   count              67          67          67
   mean            99.41      878.26     10677.4
   std             118.8     1003.61     12937.8
   min             11.65       50.16      438.23
   1%              11.73        62.5      522.79
   10%             17.23      111.49     1092.48
   25%             22.74      154.07     1422.71
   50%             37.13      476.24     4182.93
   75%            126.43      1214.5     18512.6
   90%            282.15     2519.86     28357.1
   99%            436.04     3760.24     50142.1
   max            591.43     3937.65       54121
   skew             1.85        1.42        1.46
   kurt             3.56        1.08        1.58
   mad             91.04      797.02     10585.3 
   
   In [11]: # annual portfolios 
            _, _, _, = ff_A.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType='vw')
	    _, _, _, = ff_A.comparePortfolios(kfType='Characs', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim)

   *********************************** ME (3) ************************************
       *********************** Observation frequency: A ************************
       ************************* Returns: 1953-12-31 to 2019-12-31 **************************

   Correlation matrix:
           me0-30  me70-100  me30-70
   corr:   0.995     0.998    0.995 

   Average matrix:
                             me0-30          me70-100           me30-70
   [wrds, kflib]:  [16.25%, 15.6%]  [12.29%, 12.53%]  [14.46%, 14.69%] 

   Std Deviation matrix:
                              me0-30          me70-100           me30-70
   [wrds, kflib]:  [26.13%, 25.87%]  [17.07%, 16.99%]  [19.88%, 20.65%] 

   Elapsed time:  5.846  seconds.

   *********************************** ME (3) ************************************
       *********************** Observation frequency: A ************************
      ************************** (Characteristic: ME) ***************************
      ******************************* NOT AVAILABLE *****************************

   Elapsed time:  5.53  seconds.


**(5 x 1) Quintile Sorts**:

.. code-block:: ipython

   In [9]: sortingDim = [5]   
   In [10]: # Summary statistics
	    ff_A.getFamaFrenchStats(dataType='Returns', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType='vw')
	    ff_A.getFamaFrenchStats(dataType='NumFirms', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
            ff_A.getFamaFrenchStats(dataType='Characs', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)

   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** ME (5) ************************************
       
      *********************** Observation frequency: A ************************
                  me0-20     me20-40     me40-60     me60-80    me80-100
   startdate  1953-12-31  1953-12-31  1953-12-31  1953-12-31  1953-12-31
   enddate    2019-12-31  2019-12-31  2019-12-31  2019-12-31  2019-12-31
   count              67          67          67          67          67
   mean            0.16%       0.15%       0.15%       0.14%       0.12%
   std             0.28%       0.22%        0.2%       0.18%       0.17%
   min            -0.39%      -0.34%      -0.32%       -0.4%      -0.36%
   1%             -0.38%      -0.32%      -0.29%      -0.32%      -0.31%
   10%            -0.14%      -0.12%      -0.11%      -0.07%      -0.09%
   25%            -0.06%      -0.02%        0.0%       0.02%       0.02%
   50%             0.18%       0.17%       0.17%       0.16%       0.13%
   75%             0.32%       0.28%       0.29%       0.27%       0.23%
   90%              0.5%       0.43%       0.43%       0.37%       0.33%
   99%             0.85%       0.62%       0.54%        0.5%       0.44%
   max             1.01%       0.63%        0.6%        0.5%       0.49%
   skew            0.37%       0.02%      -0.11%       -0.4%      -0.42%
   kurt            0.32%      -0.29%      -0.22%       0.34%       0.12%
   mad             0.22%       0.18%       0.16%       0.14%       0.14% 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** ME (5) ************************************
       
   *********************** Observation frequency: A ************************
                  me0-20     me20-40     me40-60     me60-80    me80-100
   startdate  1953-12-31  1953-12-31  1953-12-31  1953-12-31  1953-12-31
   enddate    2019-12-31  2019-12-31  2019-12-31  2019-12-31  2019-12-31
   count              67          67          67          67          67
   mean             1936         515         358         294         262
   std              1222         264         152         110          90
   min                76          80          90          91          92
   1%                 81          83          90          92          92
   10%               100          96         101          98          99
   25%               758         261         233         214         207
   50%              2186         589         402         323         285
   75%              2992         658         436         355         323
   90%              3370         869         531         405         343
   99%              4010         957         623         482         416
   max              4015         962         627         502         430
   skew               -0          -0          -0          -1          -1
   kurt               -1          -1          -1          -1          -0
   mad              1041         219         125          89          72 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** ME (5) ************************************
      
      ************************** (Characteristic: ME) ***************************
    *********************** Observation frequency: A ************************
   me_port        me0-20     me20-40     me40-60     me60-80    me80-100
   startdate  1953-12-31  1953-12-31  1953-12-31  1953-12-31  1953-12-31
   enddate    2019-12-31  2019-12-31  2019-12-31  2019-12-31  2019-12-31
   count              67          67          67          67          67
   mean             68.4         358      850.01     2089.37     15007.1
   std             79.87      409.31      964.15     2361.61       18082
   min              8.66       21.12       44.38      106.44      598.48
   1%               8.93       26.26       56.77      129.62      705.69
   10%             12.98       47.99       103.7      245.61      1480.2
   25%             16.28       64.64      144.69      340.59     1944.19
   50%             26.31      170.06      464.82     1153.87     5693.19
   75%             89.11      530.76     1204.12     2987.83     26924.5
   90%            199.37     1011.88     2418.42      5756.8     40020.4
   99%            290.35     1427.32      3438.1     8960.67     69321.9
   max             396.9     1745.95     3838.29     9542.63     72980.1
   skew              1.8        1.39        1.36        1.41        1.39
   kurt             3.35        1.08        0.86        1.19        1.25
   mad             61.55      329.41      770.75     1877.98     14960.5 
   
   In [11]: # annual portfolios 
            _, _, _, = ff_A.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType='vw')
	    _, _, _, = ff_A.comparePortfolios(kfType='Characs', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim)

   *********************************** ME (5) ************************************
       *********************** Observation frequency: A ************************
       ************************* Returns: 1953-12-31 to 2019-12-31 **************************
   
   Correlation matrix:
           me20-40  me80-100  me0-20  me40-60  me60-80
   corr:    0.993     0.998   0.994    0.994    0.991 

   Average matrix:
                             me20-40  ...          me60-80
   [wrds, kflib]:  [15.29%, 15.21%]  ...  [14.17%, 14.3%]

   [1 rows x 5 columns] 

   Std Deviation matrix:
                             me20-40  ...          me60-80
   [wrds, kflib]:  [22.39%, 22.89%]  ...  [18.4%, 19.14%]

   [1 rows x 5 columns] 

   Elapsed time:  5.436  seconds.

   *********************************** ME (5) ************************************
       *********************** Observation frequency: A ************************
      ************************** (Characteristic: ME) ***************************
      ******************************* NOT AVAILABLE *****************************

   Elapsed time:  5.454  seconds.


**(10 x 1) Decile Sorts**:

.. code-block:: ipython

   In [9]: sortingDim = [10]   
   In [10]: # Summary statistics
	   ff_A.getFamaFrenchStats(dataType='Returns', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType='vw')
	   ff_A.getFamaFrenchStats(dataType='NumFirms', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
           ff_A.getFamaFrenchStats(dataType='Characs', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
   
   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** ME (10) ************************************
       
      *********************** Observation frequency: A ************************
                  me0-10     me10-20  ...     me80-90    me90-100
   startdate  1953-12-31  1953-12-31  ...  1953-12-31  1953-12-31
   enddate    2019-12-31  2019-12-31  ...  2019-12-31  2019-12-31
   count              67          67  ...          67          67
   mean            0.18%       0.15%  ...       0.13%       0.12%
   std             0.31%       0.26%  ...       0.18%       0.17%
   min            -0.44%      -0.36%  ...      -0.42%      -0.35%
   1%              -0.4%      -0.36%  ...      -0.31%       -0.3%
   10%            -0.15%      -0.15%  ...       -0.1%       -0.1%
   25%            -0.06%      -0.04%  ...       0.02%       0.02%
   50%             0.19%       0.16%  ...       0.15%       0.13%
   75%             0.34%       0.32%  ...       0.21%       0.23%
   90%             0.52%       0.49%  ...       0.36%       0.33%
   99%             0.99%       0.74%  ...       0.47%       0.43%
   max             1.14%       0.85%  ...        0.5%       0.49%
   skew             0.5%       0.24%  ...      -0.44%      -0.39%
   kurt            0.53%      -0.13%  ...       0.58%       0.01%
   mad             0.24%        0.2%  ...       0.13%       0.14%

   [17 rows x 10 columns] 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** ME (10) ************************************
 
      *********************** Observation frequency: A ************************
                  me0-10     me10-20  ...     me80-90    me90-100
   startdate  1953-12-31  1953-12-31  ...  1953-12-31  1953-12-31
   enddate    2019-12-31  2019-12-31  ...  2019-12-31  2019-12-31
   count              67          67  ...          67          67
   mean             1521         416  ...         133         128
   std               975         261  ...          47          43
   min                37          39  ...          46          42
   1%                 40          41  ...          46          43
   10%                49          51  ...          50          49
   25%               584         177  ...         104         103
   50%              1723         418  ...         144         142
   75%              2366         562  ...         166         157
   90%              2743         789  ...         180         166
   99%              3085         954  ...         216         200
   max              3129         959  ...         222         208
   skew               -0           0  ...          -1          -1
   kurt               -1          -1  ...          -0          -0
   mad               842         208  ...          37          35

   [17 rows x 10 columns] 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** ME (10) ************************************
      
      ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: A ************************
   me_port        me0-10     me10-20  ...     me80-90    me90-100
   startdate  1953-12-31  1953-12-31  ...  1953-12-31  1953-12-31
   enddate    2019-12-31  2019-12-31  ...  2019-12-31  2019-12-31
   count              67          67  ...          67          67
   mean               40      157.27  ...     5267.35     25637.9
   std             43.78      180.57  ...     6302.84     31790.4
   min              6.03       11.16  ...      225.93        1042
   1%               6.51        12.8  ...      264.12     1171.39
   10%              8.49       22.92  ...      520.41     2430.96
   25%              11.2       31.11  ...      715.65     3211.85
   50%             17.21       73.12  ...     2592.55     8974.88
   75%             50.27      231.63  ...     8063.43     47211.8
   90%            109.03      442.67  ...     14509.7     66863.5
   99%            163.79      646.97  ...     24173.2      123100
   max            203.33      812.66  ...     28221.9      147577
   skew             1.63        1.52  ...        1.55        1.58
   kurt             2.13        1.69  ...        2.06        2.46
   mad             34.27      143.62  ...     5000.12     25984.8

   [17 rows x 10 columns] 
   
   In [11]: # annual portfolios 
           _, _, _, = ff_A.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType='vw')
	   _, _, _, = ff_A.comparePortfolios(kfType='Characs', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim)

   *********************************** ME (10) ************************************
       *********************** Observation frequency: A ************************
       ************************* Returns: 1953-12-31 to 2019-12-31 **************************
   Correlation matrix:
           me30-40  me0-10  me90-100  me20-30  ...  me80-90  me40-50  me60-70  me70-80
   corr:    0.987   0.968     0.998    0.989  ...    0.994     0.99    0.988    0.979

   [1 rows x 10 columns] 

   Average matrix:
                             me30-40  ...          me70-80
   [wrds, kflib]:  [14.76%, 14.91%]  ...  [14.07%, 14.1%]
   [1 rows x 10 columns] 

   Std Deviation matrix:
                            me30-40  ...           me70-80
   [wrds, kflib]:  [21.83%, 22.8%]  ...  [18.14%, 18.61%]
   [1 rows x 10 columns] 

   Elapsed time:  5.5  seconds.

   *********************************** ME (10) ************************************
       *********************** Observation frequency: A ************************
      ************************** (Characteristic: ME) ***************************
      ******************************* NOT AVAILABLE *****************************

   Elapsed time:  5.396  seconds


Portfolios Sorted on `Book-to-Market` ``BM``
#############################################

.. code-block:: ipython

   In [6]: ffFactors, ffsortCharac, ffportCharac = [], ['BM'], ['ME', 'BM']


Portfolios Sorted on `Book-to-Market` ``BM`` : Daily
*****************************************************

.. code-block:: ipython

   In [7]: ffFreq = 'D'
   In [8]: ff_D = ff.FamaFrench(runQuery=runQuery, freqType=ffFreq, sortCharacsId=ffsortCharac, factorsId=ffFactors, mainCharacsId=ffportCharac)


**(3 x 1) Sorts**:

.. code-block:: ipython

   In [9]: sortingDim = [3]    
   In [10]: # Summary statistics
	      ff_D.getFamaFrenchStats(dataType='Returns', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType='vw')
	      ff_D.getFamaFrenchStats(dataType='NumFirms', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
              ff_D.getFamaFrenchStats(dataType='Characs', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
        
   In [11]: # daily portfolios 
            _, _, _, = ff_D.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType='vw')



**(5 x 1) Sorts**:

.. code-block:: ipython

   In [9]: sortingDim = [5]    
   In [10]: # Summary statistics
	      ff_D.getFamaFrenchStats(dataType='Returns', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType='vw')
	      ff_D.getFamaFrenchStats(dataType='NumFirms', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
              ff_D.getFamaFrenchStats(dataType='Characs', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
        
   In [11]: # daily portfolios 
            _, _, _, = ff_D.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType='vw')



**(10 x 1) Sorts**:

.. code-block:: ipython

   In [9]: sortingDim = [10]    
   In [10]: # Summary statistics
	      ff_D.getFamaFrenchStats(dataType='Returns', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType='vw')
	      ff_D.getFamaFrenchStats(dataType='NumFirms', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
              ff_D.getFamaFrenchStats(dataType='Characs', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
        
   In [11]: # daily portfolios 
            _, _, _, = ff_D.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType='vw')



Portfolios Sorted on `Book-to-Market` ``BM`` : Monthly
*******************************************************


.. code-block:: ipython
   
   In [7]: ffFreq = 'M'
   In [8]: ff_M = ff.FamaFrench(runQuery=runQuery, freqType=ffFreq, sortCharacsId=ffsortCharac, factorsId=ffFactors, mainCharacsId=ffportCharac)

**(3 x 1) Sorts**:

.. code-block:: ipython

   In [9]: sortingDim = [3]      
   In [10]: # Summary statistics
	    ff_M.getFamaFrenchStats(dataType='Returns', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType='vw')
	    ff_M.getFamaFrenchStats(dataType='NumFirms', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
            ff_M.getFamaFrenchStats(dataType='Characs', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** BM (3) ************************************

       *********************** Observation frequency: M ************************
                  bm0-30     bm30-70    bm70-100
   startdate  1953-07-31  1953-07-31  1953-07-31
   enddate    2020-02-29  2020-02-29  2020-02-29
   count             800         800         800
   mean            0.01%       0.01%       0.01%
   std             0.05%       0.04%       0.05%
   min            -0.24%      -0.21%      -0.21%
   1%             -0.11%       -0.1%      -0.13%
   10%            -0.05%      -0.04%      -0.04%
   25%            -0.02%      -0.01%      -0.01%
   50%             0.01%       0.01%       0.02%
   75%             0.04%       0.03%       0.04%
   90%             0.06%       0.06%       0.06%
   99%             0.11%       0.11%       0.12%
   max             0.21%       0.18%       0.23%
   skew           -0.42%      -0.43%       -0.4%
   kurt            1.86%       2.39%       2.49%
   mad             0.03%       0.03%       0.04% 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** BM (3) ************************************

       *********************** Observation frequency: M ************************
                  bm0-30     bm30-70    bm70-100
   startdate  1953-07-31  1953-07-31  1953-07-31
   enddate    2020-02-29  2020-02-29  2020-02-29
   count             800         800         800
   mean             1088        1062        1045
   std               634         543         603
   min                29          24          24
   1%                 95         125          94
   10%               104         136         103
   25%               593         602         478
   50%              1070        1198        1153
   75%              1640        1446        1368
   90%              1909        1645        1926
   99%              2132        2040        2243
   max              2187        2165        2332
   skew               -0          -0          -0
   kurt               -1          -1          -1
   mad               530         454         486 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** BM (3) ************************************

      ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: M ************************
   bm_port        bm0-30     bm30-70    bm70-100
   startdate  1953-07-31  1953-07-31  1953-07-31
   enddate    2020-02-29  2020-02-29  2020-02-29
   count             800         800         800
   mean          3061.84     1744.29      687.78
   std           4372.63     2729.59     1026.88
   min            232.23       139.9       35.29
   1%             239.84      142.07       35.75
   10%            332.29      251.35       67.04
   25%            481.72      331.11      113.76
   50%            838.72      592.78      309.89
   75%           5436.18     1822.69      561.97
   90%           8036.61     4850.32     2080.76
   99%           18618.6     8482.18     5635.78
   max           27233.1     20797.4     5871.15
   skew             2.66        3.96         2.7
   kurt             9.49       22.15        8.22
   mad           3222.53     1727.27      697.83 

      ************************** (Characteristic: BM) ***************************
       *********************** Observation frequency: M ************************
   bm_port        bm0-30     bm30-70    bm70-100
   startdate  1953-07-31  1953-07-31  1953-07-31
   enddate    2020-02-29  2020-02-29  2020-02-29
   count             800         800         800
   mean              0.3         0.7        1.35
   std              0.12        0.27        0.52
   min              0.07        0.31        0.73
   1%               0.13        0.39        0.74
   10%              0.16        0.44        0.83
   25%              0.21        0.51        0.97
   50%              0.25        0.65        1.26
   75%              0.38        0.82        1.54
   90%              0.49        1.08        1.88
   99%               0.7         1.8        3.61
   max              0.72         1.8        3.66
   skew             0.92         1.4        1.97
   kurt             0.46        2.68        5.83
   mad               0.1        0.21        0.37 
	
   In [11]: # monthly portfolios 
            _, _, _, = ff_M.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType='vw')
	    _, _, _, = ff_M.comparePortfolios(kfType='NumFirms', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim)
	    _, _, _, = ff_M.comparePortfolios(kfType='Characs', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim)

   *********************************** BM (3) ************************************
       *********************** Observation frequency: M ************************
       ************************* Returns: 1953-07-31 to 2020-02-29 **************************
   
   Correlation matrix:
           bm0-30  bm30-70  bm70-100
   corr:   0.997    0.992     0.989 

   Average matrix:
                            bm0-30         bm30-70        bm70-100
   [wrds, kflib]:  [0.95%, 0.94%]  [1.01%, 0.99%]  [1.18%, 1.18%] 

   Std Deviation matrix:
                            bm0-30         bm30-70        bm70-100
   [wrds, kflib]:  [4.53%, 4.46%]  [4.15%, 4.14%]  [4.82%, 4.86%] 

   Elapsed time:  4.789  seconds.

   *********************************** BM (3) ************************************
       *********************** Observation frequency: M ************************
       ************************* NumFirms: 1953-07-31 to 2020-02-29 **************************

   Correlation matrix:
           bm0-30  bm30-70  bm70-100
   corr:   0.986    0.973     0.984 

   Average matrix:
                          bm0-30       bm30-70      bm70-100
   [wrds, kflib]:  [1088, 1100]  [1062, 1087]  [1045, 1026] 

   Std Deviation matrix:
                        bm0-30     bm30-70    bm70-100
   [wrds, kflib]:  [634, 588]  [543, 473]  [603, 531] 

   Elapsed time:  4.502  seconds.

   *********************************** BM (3) ************************************
       *********************** Observation frequency: M ************************
       ************************* (Characteristic: ME): 1953-07-31 to 2020-02-29 ***************************

   Correlation matrix:
           bm0-30  bm30-70  bm70-100
   corr:   0.973    0.852     0.961 

   Average matrix:
                                bm0-30             bm30-70          bm70-100
   [wrds, kflib]:  [3061.84, 2812.73]  [1744.29, 1520.57]  [687.78, 711.19] 

   Std Deviation matrix:
                                bm0-30             bm30-70            bm70-100
   [wrds, kflib]:  [4372.63, 3968.86]  [2729.59, 2041.68]  [1026.88, 1036.67] 

   *********************************** BM (3) ************************************
       *********************** Observation frequency: M ************************
      ************************** (Characteristic: BM) ***************************
      ******************************* NOT AVAILABLE *****************************

   Elapsed time:  4.481  seconds.


**(5 x 1) Sorts**:


.. code-block:: ipython

   In [9]: sortingDim = [5]      
   In [10]: # Summary statistics
	    ff_M.getFamaFrenchStats(dataType='Returns', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType='vw')
	    ff_M.getFamaFrenchStats(dataType='NumFirms', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
            ff_M.getFamaFrenchStats(dataType='Characs', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)

   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** BM (5) ************************************

       *********************** Observation frequency: M ************************
                  bm0-20     bm20-40     bm40-60     bm60-80    bm80-100
   startdate  1953-07-31  1953-07-31  1953-07-31  1953-07-31  1953-07-31
   enddate    2020-02-29  2020-02-29  2020-02-29  2020-02-29  2020-02-29
   count             800         800         800         800         800
   mean            0.01%       0.01%       0.01%       0.01%       0.01%
   std             0.05%       0.04%       0.04%       0.04%       0.05%
   min            -0.24%      -0.25%      -0.22%      -0.24%      -0.21%
   1%             -0.11%      -0.11%       -0.1%      -0.12%      -0.13%
   10%            -0.05%      -0.04%      -0.04%      -0.04%      -0.05%
   25%            -0.02%      -0.02%      -0.01%      -0.01%      -0.02%
   50%             0.01%       0.01%       0.01%       0.01%       0.02%
   75%             0.04%       0.04%       0.04%       0.04%       0.04%
   90%             0.06%       0.06%       0.06%       0.06%       0.07%
   99%             0.11%       0.11%       0.11%       0.11%       0.13%
   max             0.22%       0.16%       0.17%       0.22%       0.26%
   skew           -0.37%      -0.48%      -0.44%      -0.53%      -0.23%
   kurt            1.67%       2.16%       2.29%       3.48%       2.04%
   mad             0.04%       0.03%       0.03%       0.03%       0.04% 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** BM (5) ************************************
   
       *********************** Observation frequency: M ************************
                  bm0-20     bm20-40     bm40-60     bm60-80    bm80-100
   startdate  1953-07-31  1953-07-31  1953-07-31  1953-07-31  1953-07-31
   enddate    2020-02-29  2020-02-29  2020-02-29  2020-02-29  2020-02-29
   count             800         800         800         800         800
   mean              804         553         525         560         752
   std               491         284         270         301         445
   min                19          15          14          13          16
   1%                 65          63          63          63          64
   10%                69          69          68          68          69
   25%               405         343         290         281         325
   50%               784         627         589         627         836
   75%              1246         767         723         715        1007
   90%              1464         844         798         934        1399
   99%              1656        1078        1044        1178        1655
   max              1692        1155        1133        1235        1746
   skew               -0          -0          -0          -0          -0
   kurt               -1          -1          -1          -1          -1
   mad               414         238         224         243         362 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** BM (5) ************************************

      ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: M ************************
   bm_port        bm0-20     bm20-40     bm40-60     bm60-80    bm80-100
   startdate  1953-07-31  1953-07-31  1953-07-31  1953-07-31  1953-07-31
   enddate    2020-02-29  2020-02-29  2020-02-29  2020-02-29  2020-02-29
   count             800         800         800         800         800
   mean           3295.4     2528.11     1600.91     1099.05      538.89
   std           5150.17     4072.37     2048.53     1453.59      782.87
   min            209.09      177.45       151.3       69.07       26.42
   1%             217.28      181.17      152.36       70.26       26.69
   10%             350.7      263.06         217      128.15       48.26
   25%            542.22         366      306.52      212.81       91.58
   50%            839.15      733.43      600.21      530.33      208.56
   75%           5751.78     2940.28      1918.5     1065.85      447.98
   90%           7621.09     7368.07     4642.98     3358.62     1841.48
   99%           20946.8     12469.8      7983.8     8305.23     3417.73
   max           37614.7     30047.6     8086.98     8495.83     3588.63
   skew              3.7        3.69        1.78        2.56        2.11
   kurt            19.18       19.37        2.18        8.12        3.68
   mad           3484.21     2633.91     1535.61     1017.34      559.67 

      ************************** (Characteristic: BM) ***************************
       *********************** Observation frequency: M ************************
   bm_port        bm0-20     bm20-40     bm40-60     bm60-80    bm80-100
   startdate  1953-07-31  1953-07-31  1953-07-31  1953-07-31  1953-07-31
   enddate    2020-02-29  2020-02-29  2020-02-29  2020-02-29  2020-02-29
   count             800         800         800         800         800
   mean             0.25        0.51        0.71        0.96         1.6
   std              0.11         0.2        0.27        0.35        0.67
   min              0.06        0.26        0.35        0.54        0.82
   1%               0.11        0.26         0.4        0.54        0.83
   10%              0.13        0.31        0.45        0.62        0.96
   25%              0.18        0.36        0.52         0.7        1.17
   50%              0.21        0.48        0.67        0.89         1.5
   75%              0.31        0.61        0.83        1.11        1.81
   90%              0.42         0.8        1.08        1.46        2.19
   99%              0.54        1.32        1.83         2.5        4.45
   max              0.55        1.32        1.83         2.5        5.31
   skew              0.8        1.41        1.45        1.63        2.49
   kurt            -0.17        2.71        2.99        3.81        9.12
   mad              0.09        0.15         0.2        0.26        0.45 
 
   In [11]: # monthly portfolios 
            _, _, _, = ff_M.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType='vw')
	    _, _, _, = ff_M.comparePortfolios(kfType='NumFirms', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim)
	    _, _, _, = ff_M.comparePortfolios(kfType='Characs', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim)

   *********************************** BM (5) ************************************
       *********************** Observation frequency: M ************************
       ************************* Returns: 1953-07-31 to 2020-02-29 **************************

   Correlation matrix:
           bm80-100  bm20-40  bm0-20  bm40-60  bm60-80
   corr:     0.979    0.989   0.996    0.982     0.97 

   Average matrix:
                         bm80-100         bm20-40  ...         bm40-60         bm60-80
   [wrds, kflib]:  [1.3%, 1.21%]  [0.96%, 0.96%]  ...  [1.03%, 1.06%]  [1.01%, 1.04%]

   [1 rows x 5 columns] 

   Std Deviation matrix:
                          bm80-100         bm20-40  ...         bm40-60         bm60-80
   [wrds, kflib]:  [5.12%, 5.22%]  [4.39%, 4.28%]  ...  [4.19%, 4.15%]  [4.47%, 4.47%]

   [1 rows x 5 columns] 

   Elapsed time:  4.899  seconds.

   *********************************** BM (5) ************************************
       *********************** Observation frequency: M ************************
       ************************* NumFirms: 1953-07-31 to 2020-02-29 **************************

   Correlation matrix:
           bm80-100  bm20-40  bm0-20  bm40-60  bm60-80
   corr:     0.988    0.973   0.989    0.976    0.969 

   Average matrix:
                      bm80-100     bm20-40      bm0-20     bm40-60     bm60-80
   [wrds, kflib]:  [752, 733]  [553, 567]  [804, 807]  [525, 537]  [560, 569] 

   Std Deviation matrix:
                      bm80-100     bm20-40      bm0-20     bm40-60     bm60-80
   [wrds, kflib]:  [445, 397]  [284, 251]  [491, 459]  [270, 235]  [301, 262] 

   Elapsed time:  4.74  seconds.

   *********************************** BM (5) ************************************
       *********************** Observation frequency: M ************************
       ************************* (Characteristic: ME): 1953-07-31 to 2020-02-29 ***************************

   Correlation matrix:
           bm80-100  bm20-40  bm0-20  bm40-60  bm60-80
   corr:     0.966     0.89   0.941    0.974    0.924 

   Average matrix:
                            bm80-100  ...             bm60-80
   [wrds, kflib]:  [538.89, 559.61]  ...  [1099.05, 1145.39]

   [1 rows x 5 columns] 

   Std Deviation matrix:
                            bm80-100  ...             bm60-80
   [wrds, kflib]:  [782.87, 823.04]  ...  [1453.59, 1593.26]

   [1 rows x 5 columns] 

   *********************************** BM (5) ************************************
       *********************** Observation frequency: M ************************
      ************************** (Characteristic: BM) ***************************
      ******************************* NOT AVAILABLE *****************************

   Elapsed time:  4.758  seconds.

**(10 x 1) Sorts**:

.. code-block:: ipython

   In [9]: sortingDim = [10]      
   In [10]: # Summary statistics
	    ff_M.getFamaFrenchStats(dataType='Returns', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType='vw')
	    ff_M.getFamaFrenchStats(dataType='NumFirms', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)
            ff_M.getFamaFrenchStats(dataType='Characs', dataFreq=ffFreq, dt_start=startDate, dt_end=endDate, pDim=sortingDim)

   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** BM (10) ************************************

       *********************** Observation frequency: M ************************
                  bm0-10     bm10-20  ...     bm80-90    bm90-100
   startdate  1953-07-31  1953-07-31  ...  1953-07-31  1953-07-31
   enddate    2020-02-29  2020-02-29  ...  2020-02-29  2020-02-29
   count             800         800  ...         800         800
   mean            0.01%       0.01%  ...       0.01%       0.01%
   std             0.05%       0.05%  ...       0.05%       0.06%
   min            -0.23%      -0.25%  ...       -0.2%      -0.23%
   1%             -0.12%      -0.11%  ...      -0.13%      -0.16%
   10%            -0.05%      -0.05%  ...      -0.05%      -0.06%
   25%            -0.02%      -0.02%  ...      -0.02%      -0.02%
   50%             0.01%       0.01%  ...       0.02%       0.02%
   75%             0.04%       0.04%  ...       0.04%       0.05%
   90%             0.07%       0.06%  ...       0.07%       0.07%
   99%             0.12%       0.11%  ...       0.13%       0.16%
   max             0.23%       0.19%  ...       0.22%       0.31%
   skew           -0.28%      -0.44%  ...       -0.2%      -0.24%
   kurt            1.42%       1.73%  ...       1.66%        2.9%
   mad             0.04%       0.04%  ...       0.04%       0.04%

   [17 rows x 10 columns] 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** BM (10) ************************************
   
       *********************** Observation frequency: M ************************
                  bm0-10     bm10-20  ...     bm80-90    bm90-100
   startdate  1953-07-31  1953-07-31  ...  1953-07-31  1953-07-31
   enddate    2020-02-29  2020-02-29  ...  2020-02-29  2020-02-29
   count             800         800  ...         800         800
   mean              483         321  ...         338         415
   std               331         173  ...         202         253
   min                 5          14  ...           8           8
   1%                 32          32  ...          32          32
   10%                34          35  ...          34          35
   25%               209         194  ...         138         182
   50%               422         359  ...         370         451
   75%               799         459  ...         443         579
   90%               963         537  ...         631         682
   99%              1139         599  ...         807         989
   max              1207         620  ...         894        1026
   skew                0          -0  ...           0           0
   kurt               -1          -1  ...          -1          -1
   mad               282         143  ...         163         206

   [17 rows x 10 columns] 
   
   *********************************** Summary Statistics: Firm Characteristics ***********************************
            *********************************** BM (10) ************************************
 
        ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: M ************************
   bm_port        bm0-10     bm10-20  ...     bm80-90    bm90-100
   startdate  1953-07-31  1953-07-31  ...  1953-07-31  1953-07-31
   enddate    2020-02-29  2020-02-29  ...  2020-02-29  2020-02-29
   count             800         800  ...         800         800
   mean          3577.64     3098.58  ...      710.14       391.7
   std           6269.73     4712.12  ...      986.12      611.44
   min            147.22      205.62  ...       34.08       18.17
   1%              153.7      205.62  ...       34.45       18.17
   10%            358.77      336.39  ...       61.72       29.48
   25%            554.07      468.85  ...       101.7       71.46
   50%           1077.72      793.22  ...      307.38      129.21
   75%           5465.65     5255.08  ...      676.31       261.6
   90%           8527.31     7991.98  ...     2391.08     1501.81
   99%           22960.3     18812.6  ...     4506.64     2410.72
   max           51165.5     32775.2  ...     4664.76     2498.37
   skew             4.89        3.26  ...        2.08        2.08
   kurt            31.93        15.1  ...        3.73        3.07
   mad           3762.89      3298.7  ...      695.71      432.34

   [17 rows x 10 columns] 

      ************************** (Characteristic: BM) ***************************
       *********************** Observation frequency: M ************************
   bm_port        bm0-10     bm10-20  ...     bm80-90    bm90-100
   startdate  1953-07-31  1953-07-31  ...  1953-07-31  1953-07-31
   enddate    2020-02-29  2020-02-29  ...  2020-02-29  2020-02-29
   count             800         800  ...         800         800
   mean             0.19        0.34  ...        1.29        2.05
   std              0.09        0.13  ...        0.47        0.92
   min              0.01        0.09  ...        0.71           1
   1%               0.07        0.16  ...        0.72        1.01
   10%              0.09         0.2  ...        0.82        1.21
   25%              0.13        0.24  ...        0.95        1.42
   50%              0.16         0.3  ...        1.22        1.87
   75%              0.24        0.41  ...        1.43        2.31
   90%              0.33        0.54  ...        1.85        2.81
   99%              0.39         0.8  ...        3.56        5.67
   max              0.39         0.8  ...        3.57        7.55
   skew             0.72        0.96  ...        1.97        2.91
   kurt            -0.29        0.71  ...        6.53       12.49
   mad              0.07        0.11  ...        0.34         0.6

   [17 rows x 10 columns] 
   
   In [11]: # monthly portfolios 
            _, _, _, = ff_M.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType='vw')
	    _, _, _, = ff_M.comparePortfolios(kfType='NumFirms', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim)
	    _, _, _, = ff_M.comparePortfolios(kfType='Characs', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim)

   *********************************** BM (10) ************************************
       *********************** Observation frequency: M ************************
       ************************* Returns: 1953-07-31 to 2020-02-29 **************************

   Correlation matrix:
           bm0-10  bm20-30  bm10-20  bm80-90  ...  bm60-70  bm70-80  bm90-100  bm50-60
   corr:   0.991    0.974    0.982     0.96  ...    0.943    0.954     0.973    0.955

   [1 rows x 10 columns] 

   Average matrix:
                            bm0-10         bm20-30  ...       bm90-100         bm50-60
   [wrds, kflib]:  [0.91%, 0.92%]  [0.98%, 0.98%]  ...  [1.3%, 1.21%]  [1.07%, 1.08%]

   [1 rows x 10 columns] 
   Std Deviation matrix:
                            bm0-10         bm20-30  ...        bm90-100         bm50-60
   [wrds, kflib]:  [4.92%, 4.86%]  [4.47%, 4.36%]  ...  [5.76%, 6.06%]  [4.37%, 4.22%]

   [1 rows x 10 columns] 

   Elapsed time:  4.8  seconds.

   *********************************** BM (10) ************************************
       *********************** Observation frequency: M ************************
       ************************* NumFirms: 1953-07-31 to 2020-02-29 **************************

   Correlation matrix:
           bm0-10  bm20-30  bm10-20  bm80-90  ...  bm60-70  bm70-80  bm90-100  bm50-60
   corr:   0.993    0.972    0.976    0.983  ...    0.962    0.967     0.988    0.972
   [1 rows x 10 columns] 

   Average matrix:
                        bm0-10     bm20-30  ...    bm90-100     bm50-60
   [wrds, kflib]:  [483, 482]  [284, 293]  ...  [415, 400]  [263, 269]

   [1 rows x 10 columns] 

   Std Deviation matrix:
                        bm0-10     bm20-30  ...    bm90-100     bm50-60
   [wrds, kflib]:  [331, 311]  [149, 134]  ...  [253, 228]  [136, 118]

   [1 rows x 10 columns] 

   Elapsed time:  4.741  seconds.
   *********************************** BM (10) ************************************
       *********************** Observation frequency: M ************************
       ************************* (Characteristic: ME): 1953-07-31 to 2020-02-29 ***************************

   Correlation matrix:
           bm0-10  bm20-30  bm10-20  bm80-90  ...  bm60-70  bm70-80  bm90-100  bm50-60
   corr:   0.918    0.965    0.925    0.965  ...    0.887    0.946     0.965     0.97
  
    [1 rows x 10 columns] 

   Average matrix:
                                bm0-10  ...             bm50-60
   [wrds, kflib]:  [3577.64, 3031.17]  ...  [1502.36, 1360.03]

   [1 rows x 10 columns] 

   Std Deviation matrix:
                                bm0-10  ...             bm50-60
   [wrds, kflib]:  [6269.73, 4359.65]  ...  [1925.28, 1776.52]

   [1 rows x 10 columns] 

   *********************************** BM (10) ************************************
       *********************** Observation frequency: M ************************
      ************************** (Characteristic: BM) ***************************
      ******************************* NOT AVAILABLE *****************************

   Elapsed time:  4.746  seconds.

Portfolios Sorted on `Book-to-Market` ``BM`` : Annual
*******************************************************


**(3 x 1) Sorts**:

TODO


**(5 x 1) Sorts**:

TODO


**(10 x 1) Sorts**:

TODO


Portfolios Sorted on `Operating Profitability` ``OP``
######################################################


Portfolios Sorted on `Operating Profitability` ``OP`` : Monthly
***************************************************************


**(3 x 1) Sorts**:

TODO


**(5 x 1) Sorts**:

TODO


**(10 x 1) Sorts**:

TODO


Portfolios Sorted on `Operating Profitability` ``OP`` : Annual
***************************************************************


**(3 x 1) Sorts**:

TODO


**(5 x 1) Sorts**:

TODO


**(10 x 1) Sorts**:

TODO




Portfolios Sorted on `Investment` ``INV``
##########################################



Portfolios Sorted on `Investment` ``INV`` : Monthly
****************************************************


**(3 x 1) Sorts**:

TODO


**(5 x 1) Sorts**:

TODO


**(10 x 1) Sorts**:

TODO


Portfolios Sorted on `Investment` ``INV`` : Annual
***************************************************


**(3 x 1) Sorts**:

TODO


**(5 x 1) Sorts**:

TODO


**(10 x 1) Sorts**:

TODO


Portfolios Sorted on `Size` ``ME`` & `Book-to-Market` ``BM``
############################################################

TODO


Portfolios Sorted on `Size` ``ME`` & `Operating Profitability` ``OP``
######################################################################

TODO


Portfolios Sorted on `Size` ``ME`` & `Investment` ``INV``
######################################################################

TODO


Portfolios Sorted on `Book-to-Market` ``BM`` & `Operating Profitability` ``OP``
################################################################################

TODO


Portfolios Sorted on `Book-to-Market` ``BM`` & `Investment` ``INV``
################################################################################

TODO


Portfolios Sorted on `Operating Profitability` ``OP`` & `Investment` ``INV``
################################################################################

TODO



    
