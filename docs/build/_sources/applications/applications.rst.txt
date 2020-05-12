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
   
   In [1]: import os
   In [2]: import datetime as dt
   In [3]: import famafrench.famafrench as ff

A required attribute is the absolute path directory where pickled datafiles will be saved. Starting from the current working directory, we will create a folder ``pickled_db`` and save all pickled files there. To do that, let's define the string variable ``pickled_dir`` as follows:

.. code-block:: ipython
   
   In [4]: pickled_dir = os.getcwd() + '/pickled_db/'


Let's create all our datasets from 1960 to the present, or the most recent date for which there is stock returns data in CRSP and fundamentals data in Compustat. We set :attr:`runQuery` to ``True`` and query all datafiles directly from `wrds-cloud`. 

.. code-block:: ipython

   In [5]: startDate = dt.date(1960, 1, 1)
   In [6]: endDate = dt.date.today()
   In [7]: runQuery = True



Fama-French 3 Factors
######################


Fama-French 3 Factors : Daily
*****************************

.. code-block:: ipython
   
   In [8]: ffFreq = 'D'
   In [9]: ffsortCharac = ['ME', 'BM']
   In [10]: ffFactors = ['MKT-RF', 'SMB', 'HML']
   In [11]: ff3_D = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors) 
   
   In [12]: # Summary statistics
	    ff3_D.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)
   
   CRSP (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [02:45<00:00, 82.68s/it]
   Historical risk-free interest rate (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: D ************************
                     mkt      mkt-rf         smb         hml
   startdate  1960-01-04  1960-01-04  1960-01-04  1960-01-04
   enddate    2020-03-31  2020-03-31  2020-03-31  2020-03-31
   count           15164       15164       15164       15164
   mean            0.04%       0.02%        0.0%       0.01%
   std             0.99%       0.99%       0.52%       0.52%
   min           -17.45%     -17.47%     -11.66%      -6.05%
   1%             -2.67%      -2.68%      -1.38%      -1.41%
   10%            -0.99%      -1.01%      -0.57%      -0.49%
   25%            -0.39%      -0.41%      -0.26%      -0.23%
   50%             0.07%       0.05%       0.02%       0.01%
   75%              0.5%       0.49%       0.28%       0.24%
   90%             1.03%       1.01%       0.56%       0.53%
   99%             2.66%       2.64%       1.29%       1.55%
   max            11.36%      11.36%       6.84%       4.91%
   skew           -0.59%      -0.58%      -0.94%       0.11%
   kurt            17.5%      17.49%      24.92%      12.26%
   mad             0.66%       0.66%       0.37%       0.34% 

   [17 rows x 4 columns] 
   
   In [13]: # Compare daily Fama-French 3 factors constructed here to those provided in Ken French's online library 	   
            _, _, _, = ff3_D.comparePortfolios('Factors', ffFreq, startDate, endDate)

   CRSP (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [03:30<00:00, 105.19s/it]
   Historical risk-free interest rate (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [03:03<00:00, 91.90s/it]
   *********************************** Factor Returns: 1960-01-04 to 2020-03-31 ***********************************

       *********************** Observation frequency: D ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    smb    hml
   corr:  1.0     1.0  0.967  0.947 

   Fama-French factors: Average matrix:
                             mkt        mkt-rf         smb           hml
   [wrds, kflib]:  [0.04, 0.04]  [0.02, 0.02]  [0.0, 0.0]  [0.01, 0.01] 

   Fama-French factors: Std Deviation matrix:
                             mkt        mkt-rf           smb           hml
   [wrds, kflib]:  [0.99, 0.99]  [0.99, 0.99]  [0.52, 0.52]  [0.52, 0.52] 

   Elapsed time:  179.776  seconds.



Fama-French 3 Factors : Weekly
*******************************

.. code-block:: ipython

   In [8]: ffFreq = 'W'
   In [9]: ffsortCharac = ['ME', 'BM']
   In [10]: ffFactors = ['MKT-RF', 'SMB', 'HML']
   In [11]: ff3_W = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors) 


   In [12]: # Summary statistics
	    ff3_W.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)

   CRSP (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (daily) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [03:10<00:00, 95.45s/it]
   Historical risk-free interest rate (weekly) dataset currently NOT saved locally. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: W ************************
                     mkt      mkt-rf         smb         hml
   startdate  1960-01-08  1960-01-08  1960-01-08  1960-01-08
   enddate    2020-03-31  2020-03-31  2020-03-31  2020-03-31
   count            3144        3144        3144        3144
   mean             0.2%       0.12%       0.02%       0.06%
   std             2.18%       2.18%        1.2%       1.23%
   min           -17.97%     -17.99%      -9.95%      -9.12%
   1%             -6.28%      -6.39%      -3.09%      -3.18%
   10%            -2.25%      -2.32%      -1.32%      -1.27%
   25%            -0.94%      -1.04%      -0.65%      -0.58%
   50%             0.36%       0.28%       0.04%       0.03%
   75%             1.43%       1.36%       0.72%       0.67%
   90%             2.47%       2.38%       1.37%       1.37%
   99%             5.63%       5.62%       2.87%       3.52%
   max            13.58%      13.47%       6.97%      10.26%
   skew           -0.58%      -0.58%      -0.33%       0.38%
   kurt             5.9%       5.86%        5.4%       7.11%
   mad             1.56%       1.56%       0.87%       0.86% 

   [17 rows x 4 columns] 

   In [13]: # Compare weekly Fama-French 3 factors constructed here to those provided in Ken French's online library 	   
            _, _, _, = ff3_W.comparePortfolios('Factors', ffFreq, startDate, endDate)

   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [03:03<00:00, 91.92s/it]
   *********************************** Factor Returns: 1960-01-08 to 2020-03-27 ***********************************

       *********************** Observation frequency: W ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    smb    hml
   corr:  1.0     1.0  0.975  0.964 

   Fama-French factors: Average matrix:
                           mkt        mkt-rf           smb           hml
   [wrds, kflib]:  [0.2, 0.2]  [0.12, 0.12]  [0.03, 0.03]  [0.06, 0.06] 

   Fama-French factors: Std Deviation matrix:
                             mkt        mkt-rf         smb           hml
   [wrds, kflib]:  [2.18, 2.18]  [2.18, 2.18]  [1.2, 1.2]  [1.23, 1.23] 

   Elapsed time:  154.54  seconds.



Fama-French 3 Factors : Monthly
********************************

.. code-block:: ipython
   
   In [8]: ffFreq = 'M'
   In [9]: ffsortCharac = ['ME', 'BM']
   In [10]: ffFactors = ['MKT-RF', 'SMB', 'HML']
   In [11]: ff3_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors) 

   In [12]: # Summary statistics
	    ff3_M.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [00:03<00:00,  1.88s/it]
   Historical risk-free interest rate (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: M ************************
                     mkt      mkt-rf         smb         hml
   startdate  1960-01-31  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31  2020-03-31
   count             723         723         723         723
   mean            0.87%       0.51%       0.15%       0.28%
   std             4.39%       4.41%       3.01%       2.87%
   min           -22.66%     -23.26%     -17.42%     -11.31%
   1%            -10.86%      -11.6%       -6.5%      -8.42%
   10%            -4.54%      -5.01%      -3.26%      -2.79%
   25%            -1.68%      -1.97%      -1.55%      -1.43%
   50%             1.25%       0.92%       0.07%       0.28%
   75%             3.66%       3.35%       1.84%       1.63%
   90%             5.74%       5.29%       3.41%       3.62%
   99%            11.17%      10.85%       8.04%       7.84%
   max             16.6%      16.09%      21.12%      12.54%
   skew           -0.53%      -0.55%        0.2%       0.01%
   kurt            1.87%       1.86%       6.19%        2.0%
   mad             3.33%       3.35%       2.16%        2.1% 

   [17 rows x 4 columns] 

   In [13]: # Compare monthly Fama-French 3 factors constructed here to those provided in Ken French's online library 	   
            _, _, _, = ff3_M.comparePortfolios('Factors', ffFreq, startDate, endDate)

   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [00:05<00:00,  2.79s/it]
   *********************************** Factor Returns: 1960-01-31 to 2020-03-31 ***********************************
 
      *********************** Observation frequency: M ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    smb    hml
   corr:  1.0     1.0  0.978  0.976 

   Fama-French factors: Average matrix:
                             mkt        mkt-rf           smb           hml
   [wrds, kflib]:  [0.87, 0.87]  [0.51, 0.51]  [0.15, 0.15]  [0.28, 0.28] 

   Fama-French factors: Std Deviation matrix:
                             mkt        mkt-rf           smb           hml
   [wrds, kflib]:  [4.39, 4.39]  [4.41, 4.41]  [3.01, 3.01]  [2.87, 2.87] 

   Elapsed time:  5.372  seconds.



Fama-French 3 Factors : Annual
******************************

.. code-block:: ipython
   
   In [8]: ffFreq = 'A'
   In [9]: ffsortCharac = ['ME', 'BM']
   In [10]: ffFactors = ['MKT-RF', 'SMB', 'HML']
   In [11]: ff3_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors) 

   In [12]: # Summary statistics
	    ff3_A.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [00:04<00:00,  2.08s/it]
   Historical risk-free interest rate (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: A ************************
                     mkt      mkt-rf         smb         hml
   startdate  1960-12-31  1960-12-31  1960-12-31  1960-12-31
   enddate    2019-12-31  2019-12-31  2019-12-31  2019-12-31
   count              60          60          60          60
   mean            11.6%       7.04%       2.35%       4.62%
   std            17.13%      17.41%      12.63%      13.58%
   min           -36.65%     -38.24%     -25.74%     -30.85%
   1%            -31.39%     -36.77%     -23.89%     -27.43%
   10%            -11.0%     -17.55%     -10.61%     -10.81%
   25%             0.05%      -4.63%      -7.29%      -4.66%
   50%            14.93%      10.71%       0.42%       6.44%
   75%            24.45%      20.22%       9.16%      13.44%
   90%            31.84%      28.21%      17.03%      20.83%
   99%            37.38%      33.57%      34.03%      33.77%
   max            38.23%      35.22%      44.45%      47.04%
   skew           -0.63%      -0.63%       0.61%       0.06%
   kurt           -0.04%      -0.16%        1.1%       0.85%
   mad            13.91%       14.2%       9.88%      10.71% 

   [17 rows x 4 columns] 

   In [13]: # Compare annual Fama-French 3 factors constructed here to those provided in Ken French's online library 	   
            _, _, _, = ff3_A.comparePortfolios('Factors', ffFreq, startDate, endDate)

   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [00:03<00:00,  1.95s/it]
   *********************************** Factor Returns: 1960-12-31 to 2019-12-31 ***********************************

       *********************** Observation frequency: A ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    smb    hml
   corr:  1.0     1.0  0.993  0.971 
   
   Fama-French factors: Average matrix:
                             mkt        mkt-rf           smb           hml
   [wrds, kflib]:  [11.6, 11.6]  [7.04, 7.04]  [2.29, 2.29]  [4.77, 4.77] 

   Fama-French factors: Std Deviation matrix:
                            mkt          mkt-rf             smb             hml
   [wrds, kflib]:  [17.13, 17.13]  [17.41, 17.41]  [12.66, 12.66]  [13.53, 13.53] 

   Elapsed time:  5.833  seconds.


Fama-French 5 Factors
######################


Fama-French 5 Factors : Daily
*******************************

.. code-block:: ipython
   
   In [8]: ffFreq = 'D'
   In [9]: ffsortCharac = ['ME', 'BM']
   In [10]: ffFactors = ['MKT-RF', 'SMB', 'HML', 'RMW', 'CMA']
   In [11]: ffportCharac = ['ME', 'BM', 'OP', 'INV']
   In [12]: ff5_D = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac) 

   In [13]: # Summary statistics
	    ff5_D.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)

   CRSP (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (daily) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [08:46<00:00, 105.24s/it]
   Historical risk-free interest rate (daily) dataset currently NOT saved locally. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: D ************************
                     mkt      mkt-rf  ...         rmw         cma
   startdate  1960-01-04  1960-01-04  ...  1960-01-04  1960-01-04
   enddate    2020-03-31  2020-03-31  ...  2020-03-31  2020-03-31
   count           15164       15164  ...       15164       15164
   mean            0.04%       0.02%  ...       0.01%       0.01%
   std             0.99%       0.99%  ...       0.42%       0.35%
   min           -17.45%     -17.47%  ...      -8.31%      -5.07%
   1%             -2.67%      -2.68%  ...      -1.13%      -0.94%
   10%            -0.99%      -1.01%  ...      -0.36%      -0.35%
   25%            -0.39%      -0.41%  ...      -0.17%      -0.17%
   50%             0.07%       0.05%  ...       0.01%       0.01%
   75%              0.5%       0.49%  ...       0.19%       0.18%
   90%             1.03%       1.01%  ...        0.4%       0.38%
   99%             2.66%       2.64%  ...       1.17%       0.95%
   max            11.36%      11.36%  ...       7.97%       3.69%
   skew           -0.59%      -0.58%  ...      -0.02%      -0.62%
   kurt            17.5%      17.49%  ...      35.09%       13.1%
   mad             0.66%       0.66%  ...       0.26%       0.24%

   [17 rows x 6 columns] 
   
   In [14]: # Compare daily Fama-French 5 factors constructed here to those provided in Ken French's online library 	   
            _, _, _, = ff5_D.comparePortfolios('Factors', ffFreq, startDate, endDate)

   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [00:14<00:00,  2.84s/it]
   *********************************** Factor Returns: 1963-07-01 to 2020-03-31 ***********************************
 
      *********************** Observation frequency: D ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    smb    hml    rmw    cma
   corr:  1.0     1.0  0.965  0.954  0.876  0.921 

   Fama-French factors: Average matrix:
                             mkt        mkt-rf  ...           rmw           cma
   [wrds, kflib]:  [0.04, 0.04]  [0.02, 0.02]  ...  [0.01, 0.01]  [0.01, 0.01]

   [1 rows x 6 columns] 

   Fama-French factors: Std Deviation matrix:
                             mkt        mkt-rf  ...           rmw           cma
   [wrds, kflib]:  [1.01, 1.01]  [1.01, 1.01]  ...  [0.43, 0.43]  [0.35, 0.35]

   [1 rows x 6 columns] 

   Elapsed time:  600.35  seconds.


Fama-French 5 Factors : Weekly
*******************************

.. code-block:: ipython
   
   In [8]: ffFreq = 'W'
   In [9]: ffsortCharac = ['ME', 'BM']
   In [10]: ffFactors = ['MKT-RF', 'SMB', 'HML', 'RMW', 'CMA']
   In [11]: ffportCharac = ['ME', 'BM', 'OP', 'INV']
   In [12]: ff5_W = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac) 

   In [13]: # Summary statistics
	    ff5_W.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)

   CRSP (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [08:11<00:00, 98.29s/it]
   Historical risk-free interest rate (weekly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: W ************************
                     mkt      mkt-rf  ...         rmw         cma
   startdate  1960-01-08  1960-01-08  ...  1960-01-08  1960-01-08
   enddate    2020-03-31  2020-03-31  ...  2020-03-31  2020-03-31
   count            3144        3144  ...        3144        3144
   mean             0.2%       0.12%  ...       0.05%       0.04%
   std             2.18%       2.18%  ...        1.0%       0.87%
   min           -17.97%     -17.99%  ...     -13.09%      -6.27%
   1%             -6.28%      -6.39%  ...      -2.68%      -2.39%
   10%            -2.25%      -2.32%  ...      -0.88%       -0.9%
   25%            -0.94%      -1.04%  ...       -0.4%      -0.43%
   50%             0.36%       0.28%  ...       0.05%       0.03%
   75%             1.43%       1.36%  ...        0.5%       0.48%
   90%             2.47%       2.38%  ...       0.98%       1.01%
   99%             5.63%       5.62%  ...       2.83%       2.52%
   max            13.58%      13.47%  ...       9.24%       5.77%
   skew           -0.58%      -0.58%  ...      -0.56%       0.06%
   kurt             5.9%       5.86%  ...      22.07%       4.68%
   mad             1.56%       1.56%  ...       0.64%       0.62%
   
   [17 rows x 6 columns] 


Fama-French 5 Factors : Monthly
*******************************

.. code-block:: ipython
   
   In [8]: ffFreq = 'M'
   In [9]: ffsortCharac = ['ME', 'BM']
   In [10]: ffFactors = ['MKT-RF', 'SMB', 'HML', 'RMW', 'CMA']
   In [11]: ffportCharac = ['ME', 'BM', 'OP', 'INV']
   In [12]: ff5_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac) 

   In [13]: # Summary statistics
	    ff5_M.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [00:14<00:00,  2.88s/it]
   Historical risk-free interest rate (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: M ************************
                     mkt      mkt-rf  ...         rmw         cma
   startdate  1960-01-31  1960-01-31  ...  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  ...  2020-03-31  2020-03-31
   count             723         723  ...         723         723
   mean            0.87%       0.51%  ...       0.22%       0.18%
   std             4.39%       4.41%  ...        2.3%        1.8%
   min           -22.66%     -23.26%  ...     -19.17%     -12.38%
   1%            -10.86%      -11.6%  ...      -6.04%      -4.07%
   10%            -4.54%      -5.01%  ...       -2.0%       -1.9%
   25%            -1.68%      -1.97%  ...      -0.84%      -0.94%
   50%             1.25%       0.92%  ...        0.2%       0.08%
   75%             3.66%       3.35%  ...       1.32%       1.35%
   90%             5.74%       5.29%  ...       2.44%       2.32%
   99%            11.17%      10.85%  ...       6.41%       4.92%
   max             16.6%      16.09%  ...      13.14%       8.03%
   skew           -0.53%      -0.55%  ...      -0.78%      -0.16%
   kurt            1.87%       1.86%  ...      12.73%       3.79%
   mad             3.33%       3.35%  ...       1.53%       1.37%

   [17 rows x 6 columns] 
   
   In [14]: # Compare monthly Fama-French 5 factors constructed here to those provided in Ken French's online library 	   
            _, _, _, = ff5_M.comparePortfolios('Factors', ffFreq, startDate, endDate)

   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [00:14<00:00,  2.84s/it]
   *********************************** Factor Returns: 1963-07-31 to 2020-03-31 ***********************************
  
     *********************** Observation frequency: M ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    smb   hml    rmw    cma
   corr:  1.0     1.0  0.974  0.98  0.948  0.927 

   Fama-French factors: Average matrix:
                             mkt        mkt-rf  ...           rmw           cma
   [wrds, kflib]:  [0.88, 0.88]  [0.51, 0.51]  ...  [0.23, 0.23]  [0.19, 0.19]

   [1 rows x 6 columns] 

   Fama-French factors: Std Deviation matrix:
                             mkt        mkt-rf  ...           rmw           cma
   [wrds, kflib]:  [4.41, 4.41]  [4.42, 4.42]  ...  [2.33, 2.33]  [1.83, 1.83]

   [1 rows x 6 columns] 

   Elapsed time:  17.519  seconds.


Fama-French 5 Factors : Annual
*******************************

.. code-block:: ipython
   
   In [8]: ffFreq = 'A'
   In [9]: ffsortCharac = ['ME', 'BM']
   In [10]: ffFactors = ['MKT-RF', 'SMB', 'HML', 'RMW', 'CMA']
   In [11]: ffportCharac = ['ME', 'BM', 'OP', 'INV']
   In [12]: ff5_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac) 

   In [13]: # Summary statistics
	    ff5_A.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [00:14<00:00,  2.92s/it]
   Historical risk-free interest rate (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: A ************************
                     mkt      mkt-rf  ...         rmw         hml
   startdate  1960-12-31  1960-12-31  ...  1960-12-31  1960-12-31
   enddate    2019-12-31  2019-12-31  ...  2019-12-31  2019-12-31
   count              60          60  ...          60          60
   mean            11.6%       7.04%  ...       3.19%       2.86%
   std            17.13%      17.41%  ...       8.99%       8.81%
   min           -36.65%     -38.24%  ...      -24.9%     -15.01%
   1%            -31.39%     -36.77%  ...     -23.01%     -14.98%
   10%            -11.0%     -17.55%  ...      -5.68%      -7.29%
   25%             0.05%      -4.63%  ...       -1.1%      -3.07%
   50%            14.93%      10.71%  ...       3.04%       2.12%
   75%            24.45%      20.22%  ...       8.76%        8.5%
   90%            31.84%      28.21%  ...      14.13%      13.71%
   99%            37.38%      33.57%  ...      22.08%      25.27%
   max            38.23%      35.22%  ...      22.32%       26.0%
   skew           -0.63%      -0.63%  ...      -0.52%       0.37%
   kurt           -0.04%      -0.16%  ...       1.39%       0.22%
   mad            13.91%       14.2%  ...       6.72%       6.88%
  
   [17 rows x 6 columns] 
   
   In [14]: # Compare annual Fama-French 5 factors constructed here to those provided in Ken French's online library 	   
            _, _, _, = ff5_A.comparePortfolios('Factors', ffFreq, startDate, endDate)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [00:16<00:00,  3.32s/it]
   Historical risk-free interest rate (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 5/5 [00:17<00:00,  3.56s/it]
   *********************************** Factor Returns: 1964-12-31 to 2019-12-31 ***********************************

       *********************** Observation frequency: A ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    smb    hml    rmw    cma
   corr:  1.0     1.0  0.997  0.977  0.989  0.984 

   Fama-French factors: Average matrix:
                            mkt        mkt-rf  ...           rmw           cma
   [wrds, kflib]:  [11.73, 11.73]  [7.04, 7.04]  ...  [3.19, 3.19]  [3.15, 3.15]
   
   [1 rows x 6 columns] 

   Fama-French factors: Std Deviation matrix:
                               mkt          mkt-rf  ...           rmw           cma
   [wrds, kflib]:  [17.28, 17.28]  [17.57, 17.57]  ...  [9.25, 9.25]  [8.97, 8.97]

   [1 rows x 6 columns] 

   Elapsed time:  17.418  seconds.



Momentum, Short-Term Reversal, and Long-Term Reversal Factor
#############################################################


``MOM``, ``ST_Rev``, and ``LT_Rev`` : Daily
*******************************************

.. code-block:: ipython

   In [8]: ffFreq = 'D'
   In [9]: ffsortCharac = ['ME', 'PRIOR_2_12']
   In [10]: ffFactors = ['MKT-RF', 'MOM', 'ST_Rev', 'LT_Rev']
   In [11]: ffportCharac = ['ME', 'PRIOR_2_12', 'PRIOR_1_1', 'PRIOR_13_60']
   In [12]: ffprior_D = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac) 
   
   In [13]: # Summary statistics
	    ffprior_D.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)

   CRSP (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (daily) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 4/4 [22:01<00:00, 330.45s/it]
   Historical risk-free interest rate (daily) dataset currently NOT saved locally. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: D ************************
                     mkt      mkt-rf         mom      st_rev      lt_rev
   startdate  1960-01-04  1960-01-04  1960-01-04  1960-01-04  1960-01-04
   enddate    2020-03-31  2020-03-31  2020-03-31  2020-03-31  2020-03-31
   count           15164       15164       15164       15164       15164
   mean            0.04%       0.02%       0.03%        0.1%       0.01%
   std             0.99%       0.99%        0.7%       0.72%       0.46%
   min           -17.45%     -17.47%      -7.79%     -10.53%      -7.28%
   1%             -2.67%      -2.68%       -2.1%      -1.69%      -1.17%
   10%            -0.99%      -1.01%      -0.65%       -0.5%      -0.46%
   25%            -0.39%      -0.41%      -0.24%      -0.18%      -0.22%
   50%             0.07%       0.05%       0.06%       0.08%       -0.0%
   75%              0.5%       0.49%       0.34%       0.35%       0.23%
   90%             1.03%       1.01%       0.68%        0.7%       0.49%
   99%             2.66%       2.64%       1.93%       2.22%       1.23%
   max            11.36%      11.36%        6.9%      18.29%       6.66%
   skew           -0.59%      -0.58%      -0.79%       2.31%      -0.51%
   kurt            17.5%      17.49%      13.46%      56.39%      18.11%
   mad             0.66%       0.66%       0.45%       0.42%       0.31% 

   [17 rows x 5 columns] 

   In [14]: # Compare daily Fama-French factors based on prior returns constructed here to those provided in Ken French's online library
	    _, _, _, = ffprior_D.comparePortfolios('Factors', ffFreq, startDate, endDate)
	    
   CRSP (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (daily) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 4/4 [20:29<00:00, 307.45s/it]
   Historical risk-free interest rate (daily) dataset currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 4/4 [20:02<00:00, 300.70s/it]
   *********************************** Factor Returns: 1960-01-04 to 2020-03-31 ***********************************

       *********************** Observation frequency: D ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    mom  st_rev  lt_rev
   corr:  1.0     1.0  0.965    0.95     0.9 

   Fama-French factors: Average matrix:
                             mkt        mkt-rf  ...      st_rev        lt_rev
   [wrds, kflib]:  [0.04, 0.04]  [0.02, 0.02]  ...  [0.1, 0.1]  [0.01, 0.01]

   [1 rows x 5 columns] 

   Fama-French factors: Std Deviation matrix:
                             mkt        mkt-rf  ...        st_rev        lt_rev
   [wrds, kflib]:  [0.99, 0.99]  [0.99, 0.99]  ...  [0.72, 0.72]  [0.46, 0.46]

   [1 rows x 5 columns] 

   Elapsed time:  1214.541  seconds.



``MOM``, ``ST_Rev``, and ``LT_Rev`` : Monthly
**********************************************

.. code-block:: ipython

   In [8]: ffFreq = 'M'
   In [9]: ffsortCharac = ['ME', 'PRIOR_2_12']
   In [10]: ffFactors = ['MKT-RF', 'MOM', 'ST_Rev', 'LT_Rev']
   In [11]: ffportCharac = ['ME', 'PRIOR_2_12', 'PRIOR_1_1', 'PRIOR_13_60']
   In [12]: ffprior_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac) 

   
   In [13]: # Summary statistics
	    ffprior_M.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 4/4 [00:23<00:00,  5.82s/it]
   Historical risk-free interest rate (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: M ************************
                     mkt      mkt-rf         mom      st_rev      lt_rev
   startdate  1960-01-31  1960-01-31  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31  2020-03-31  2020-03-31
   count             723         723         723         723         723
   mean            0.87%       0.51%       0.67%       0.53%       0.18%
   std             4.39%       4.41%       4.21%       3.05%        2.6%
   min           -22.66%     -23.26%     -33.02%     -14.26%     -14.31%
   1%            -10.86%      -11.6%     -10.38%      -8.94%      -5.91%
   10%            -4.54%      -5.01%      -3.65%      -2.36%       -2.6%
   25%            -1.68%      -1.97%      -1.01%      -1.01%      -1.34%
   50%             1.25%       0.92%       0.71%       0.33%       0.06%
   75%             3.66%       3.35%       2.71%       1.88%       1.59%
   90%             5.74%       5.29%       4.87%        3.8%       3.23%
   99%            11.17%      10.85%      10.64%      10.33%       7.21%
   max             16.6%      16.09%      28.68%      16.74%      15.64%
   skew           -0.53%      -0.55%      -0.77%       0.35%        0.2%
   kurt            1.87%       1.86%      11.21%       5.39%       4.84%
   mad             3.33%       3.35%        2.8%       2.08%       1.89% 

   [17 rows x 5 columns] 

   In [14]: # Compare monthly Fama-French factors based on prior returns constructed here to those provided in Ken French's online library
	    _, _, _, = ffprior_M.comparePortfolios('Factors', ffFreq, startDate, endDate)
	    
   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 4/4 [00:21<00:00,  5.37s/it]
   Historical risk-free interest rate (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 4/4 [00:21<00:00,  5.26s/it]
   *********************************** Factor Returns: 1960-01-31 to 2020-03-31 ***********************************
    
       *********************** Observation frequency: M ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    mom  st_rev  lt_rev
   corr:  1.0     1.0  0.973   0.983   0.954 

   Fama-French factors: Average matrix:
                             mkt        mkt-rf  ...        st_rev      lt_rev
   [wrds, kflib]:  [0.87, 0.87]  [0.51, 0.51]  ...  [0.53, 0.53]  [0.2, 0.2]

   [1 rows x 5 columns] 

   Fama-French factors: Std Deviation matrix:
                             mkt        mkt-rf  ...        st_rev      lt_rev
   [wrds, kflib]:  [4.39, 4.39]  [4.41, 4.41]  ...  [3.05, 3.05]  [2.6, 2.6]

   [1 rows x 5 columns] 
   
   Elapsed time:  22.634  seconds.




``MOM``, ``ST_Rev``, and ``LT_Rev`` : Annual
**********************************************

.. code-block:: ipython

   In [8]: ffFreq = 'A'
   In [9]: ffsortCharac = ['ME', 'PRIOR_2_12']
   In [10]: ffFactors = ['MKT-RF', 'MOM', 'ST_Rev', 'LT_Rev']
   In [11]: ffportCharac = ['ME', 'PRIOR_2_12', 'PRIOR_1_1', 'PRIOR_13_60']
   In [12]: ffprior_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac) 

   
   In [13]: # Summary statistics
	    ffprior_A.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 4/4 [00:31<00:00,  7.88s/it]
   Historical risk-free interest rate (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** Summary Statistics: Fama-French Factors ***********************************
       *********************** Observation frequency: A ************************
                     mkt      mkt-rf         mom      st_rev      lt_rev
   startdate  1960-12-31  1960-12-31  1960-12-31  1960-12-31  1960-12-31
   enddate    2019-12-31  2019-12-31  2019-12-31  2019-12-31  2019-12-31
   count              60          60          60          60          60
   mean            11.6%       7.04%       7.56%       7.12%       2.63%
   std            17.13%      17.41%      17.78%      11.38%      12.14%
   min           -36.65%     -38.24%     -79.66%     -17.67%     -19.66%
   1%            -31.39%     -36.77%     -47.62%     -16.26%     -19.01%
   10%            -11.0%     -17.55%     -10.03%      -4.68%     -11.84%
   25%             0.05%      -4.63%       1.42%       0.86%       -7.6%
   50%            14.93%      10.71%       9.48%       5.86%       2.77%
   75%            24.45%      20.22%       16.5%      12.94%       8.95%
   90%            31.84%      28.21%      24.81%      18.13%      17.85%
   99%            37.38%      33.57%      37.37%      43.04%      29.23%
   max            38.23%      35.22%      38.24%      44.99%      31.03%
   skew           -0.63%      -0.63%      -2.03%       0.91%       0.34%
   kurt           -0.04%      -0.16%       8.87%       2.55%      -0.37%
   mad            13.91%       14.2%      11.86%       8.09%       9.76% 

   [17 rows x 5 columns] 

   In [14]: # Compare annual Fama-French factors based on prior returns constructed here to those provided in Ken French's online library
	    _, _, _, = ffprior_A.comparePortfolios('Factors', ffFreq, startDate, endDate)
	    
   Constructing Fama-French return factor(s): 100%|██████████| 4/4 [00:30<00:00,  7.54s/it]
   *********************************** Factor Returns: 1960-12-31 to 2019-12-31 ***********************************
 
      *********************** Observation frequency: A ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    mom  st_rev  lt_rev
   corr:  1.0     1.0  0.991   0.972   0.987 

   Fama-French factors: Average matrix:
                             mkt        mkt-rf  ...        st_rev        lt_rev
   [wrds, kflib]:  [11.6, 11.6]  [7.04, 7.04]  ...  [7.12, 7.12]  [2.63, 2.63]

   [1 rows x 5 columns] 

   Fama-French factors: Std Deviation matrix:
                               mkt          mkt-rf  ...          st_rev          lt_rev
   [wrds, kflib]:  [17.13, 17.13]  [17.41, 17.41]  ...  [11.38, 11.38]  [12.14, 12.14]

   [1 rows x 5 columns] 

   Elapsed time:  23.845  seconds.


Portfolios Sorted on `Size` ``ME``
##################################

.. code-block:: ipython

   In [8]: ffFactors, ffsortCharac, ffportCharac = [], ['ME'], ['ME']


Portfolios Sorted on `Size` ``ME`` : Daily
********************************************

.. code-block:: ipython

   In [9]: ffFreq = 'D'
   In [10]: ff_D = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

**(3 x 1) Sorts**:

.. code-block:: ipython

   In [11]: sortingDim = [3]    
   In [12]: # Summary statistics
	      ff_D.getFamaFrenchStats('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	      ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
              ff_D.getFamaFrenchStats('Characs', ffFreq, startDate, endDate, sortingDim)

   CRSP (daily) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (daily) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** ME (3) ************************************

       *********************** Observation frequency: D ************************
                  me0-30     me30-70    me70-100
   startdate  1960-01-04  1960-01-04  1960-01-04
   enddate    2020-03-31  2020-03-31  2020-03-31
   count           15164       15164       15164
   mean             0.0%        0.0%        0.0%
   std             0.01%       0.01%       0.01%
   min            -0.15%      -0.17%      -0.19%
   1%             -0.03%      -0.03%      -0.03%
   10%            -0.01%      -0.01%      -0.01%
   25%             -0.0%       -0.0%       -0.0%
   50%              0.0%        0.0%        0.0%
   75%             0.01%       0.01%       0.01%
   90%             0.01%       0.01%       0.01%
   99%             0.03%       0.03%       0.03%
   max             0.14%       0.14%       0.12%
   skew           -0.74%      -0.78%      -0.61%
   kurt           16.36%      18.26%      19.49%
   mad             0.01%       0.01%       0.01% 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** ME (3) ************************************
 
      *********************** Observation frequency: D ************************
                  me0-30     me30-70    me70-100
   startdate  1960-01-04  1960-01-04  1960-01-04
   enddate    2020-03-31  2020-03-31  2020-03-31
   count           15164       15164       15164
   mean             2471         802         434
   std              1252         277         122
   min                31          29          20
   1%                 31          29          20
   10%               491         343         240
   25%              1335         772         407
   50%              2540         852         453
   75%              3497         933         502
   90%              3971        1140         561
   99%              4741        1359         686
   max              5011        1439         726
   skew               -0          -1          -1
   kurt               -1           0           1
   mad              1018         204          88 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** ME (3) ************************************

      ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: D ************************
   me_port        me0-30     me30-70    me70-100
   startdate  1960-01-04  1960-01-04  1960-01-04
   enddate    2020-03-31  2020-03-31  2020-03-31
   count           15164       15164       15164
   mean           114.56      998.93     12145.2
   std            128.13     1057.04     13798.3
   min              8.81       74.04      846.91
   1%              11.73       96.69     1096.48
   10%             19.55      138.81     1360.57
   25%             27.26       177.1     1530.24
   50%             43.04      539.11     5487.16
   75%            189.09     1579.63     20402.3
   90%            307.47     2663.05     32653.4
   99%            569.59     4266.21     62493.6
   max             642.7      4841.5     75448.5
   skew             1.57        1.34         1.5
   kurt             1.96        0.97        2.16
   mad            101.81      846.66     11251.2 


        
   In [13]: # daily portfolios 
            _, _, _, = ff_D.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')

   *********************************** ME (3) ************************************
       *********************** Observation frequency: D ************************
       ************************* Returns: 1960-01-04 to 2020-03-31 **************************

   Correlation matrix:
           me0-30  me30-70  me70-100
   corr:   0.988    0.993     0.997 

   Average matrix:
                            me0-30         me30-70        me70-100
   [wrds, kflib]:  [0.05%, 0.05%]  [0.05%, 0.05%]  [0.04%, 0.04%] 

   Std Deviation matrix:
                            me0-30         me30-70        me70-100
   [wrds, kflib]:  [1.08%, 1.05%]  [1.05%, 1.04%]  [1.01%, 1.01%] 

   Elapsed time:  2818.093  seconds.


**(5 x 1) Quintile Sorts**:

.. code-block:: ipython

   In [11]: sortingDim = [5]      
   In [12]: # Summary statistics
	    ff_D.getFamaFrenchStats('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
            ff_D.getFamaFrenchStats('Characs', ffFreq, startDate, endDate, sortingDim)

   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** ME (5) ************************************

       *********************** Observation frequency: D ************************
                  me0-20     me20-40     me40-60     me60-80    me80-100
   startdate  1960-01-04  1960-01-04  1960-01-04  1960-01-04  1960-01-04
   enddate    2020-03-31  2020-03-31  2020-03-31  2020-03-31  2020-03-31
   count           15164       15164       15164       15164       15164
   mean             0.0%        0.0%        0.0%        0.0%        0.0%
   std             0.01%       0.01%       0.01%       0.01%       0.01%
   min            -0.15%      -0.17%      -0.18%      -0.16%      -0.19%
   1%             -0.03%      -0.03%      -0.03%      -0.03%      -0.03%
   10%            -0.01%      -0.01%      -0.01%      -0.01%      -0.01%
   25%             -0.0%       -0.0%       -0.0%       -0.0%       -0.0%
   50%              0.0%        0.0%        0.0%        0.0%        0.0%
   75%             0.01%       0.01%       0.01%       0.01%       0.01%
   90%             0.01%       0.01%       0.01%       0.01%       0.01%
   99%             0.03%       0.03%       0.03%       0.03%       0.03%
   max             0.13%       0.15%       0.14%       0.12%       0.12%
   skew           -0.78%      -0.58%      -0.77%      -0.63%       -0.6%
   kurt           17.15%      15.76%      17.76%      14.26%      19.82%
   mad             0.01%       0.01%       0.01%       0.01%       0.01% 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** ME (5) ************************************

       *********************** Observation frequency: D ************************
                  me0-20     me20-40     me40-60     me60-80    me80-100
   startdate  1960-01-04  1960-01-04  1960-01-04  1960-01-04  1960-01-04
   enddate    2020-03-31  2020-03-31  2020-03-31  2020-03-31  2020-03-31
   count           15164       15164       15164       15164       15164
   mean             2158         565         388         316         280
   std              1118         237         133          95          77
   min                25          15          15          11          14
   1%                 25          15          15          11          14
   10%               399         179         174         161         161
   25%              1077         484         375         304         262
   50%              2237         598         412         330         288
   75%              3074         701         450         362         326
   90%              3504         881         555         437         350
   99%              4194        1003         685         518         442
   max              4445        1033         719         550         468
   skew               -0          -0          -1          -1          -1
   kurt               -1          -0           0           1           1
   mad               920         182          96          68          55 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** ME (5) ************************************

      ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: D ************************
   me_port        me0-20     me20-40     me40-60     me60-80    me80-100
   startdate  1960-01-04  1960-01-04  1960-01-04  1960-01-04  1960-01-04
   enddate    2020-03-31  2020-03-31  2020-03-31  2020-03-31  2020-03-31
   count           15164       15164       15164       15164       15164
   mean            79.09      412.78       982.6     2416.53     17035.8
   std             86.27      439.67     1057.88      2615.9     19157.8
   min              6.73        27.9       68.08      178.31     1199.85
   1%               8.96       37.66       88.57      237.83     1497.93
   10%              14.4       56.07      128.23      318.88     1856.79
   25%             19.59       79.22      166.37      387.95      2090.8
   50%             31.07      191.49      535.47     1430.95     7525.56
   75%            131.47      690.13     1565.35     3665.02     29167.2
   90%            215.87      1130.5     2564.95     6323.36     45361.6
   99%            380.63     1694.92     4673.21     11725.9     82619.8
   max            430.04      1912.7     5427.69     15170.7     98985.6
   skew             1.53        1.24        1.45        1.62        1.39
   kurt             1.75        0.41        1.63        2.69        1.57
   mad             69.16      360.26      839.39      2029.8     15860.8 

        
   In [13]: # daily portfolios 
            _, _, _, = ff_D.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')

   *********************************** ME (5) ************************************
       *********************** Observation frequency: D ************************
       ************************* Returns: 1960-01-04 to 2020-03-31 **************************

   Correlation matrix:
           me0-20  me20-40  me40-60  me60-80  me80-100
   corr:   0.985    0.985    0.992    0.993     0.997 

   Average matrix:
                            me0-20         me20-40  ...         me60-80        me80-100
   [wrds, kflib]:  [0.05%, 0.04%]  [0.05%, 0.05%]  ...  [0.05%, 0.05%]  [0.04%, 0.04%]

   [1 rows x 5 columns] 

   Std Deviation matrix:
                            me0-20        me20-40  ...         me60-80        me80-100
   [wrds, kflib]:  [1.06%, 1.02%]  [1.12%, 1.1%]  ...  [1.01%, 1.02%]  [1.02%, 1.01%]

   [1 rows x 5 columns] 

   Elapsed time:  91.655  seconds.




**(10 x 1) Decile Sorts**:

.. code-block:: ipython

   In [11]: sortingDim = [10]      
   In [12]: # Summary statistics
	    ff_D.getFamaFrenchStats('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
            ff_D.getFamaFrenchStats('Characs', ffFreq, startDate, endDate, sortingDim)
   
   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** ME (10) ************************************
 
      *********************** Observation frequency: D ************************
                  me0-10     me10-20  ...     me80-90    me90-100
   startdate  1960-01-04  1960-01-04  ...  1960-01-04  1960-01-04
   enddate    2020-03-31  2020-03-31  ...  2020-03-31  2020-03-31
   count           15164       15164  ...       15164       15164
   mean             0.0%        0.0%  ...        0.0%        0.0%
   std             0.01%       0.01%  ...       0.01%       0.01%
   min            -0.17%      -0.16%  ...      -0.18%       -0.2%
   1%             -0.03%      -0.03%  ...      -0.03%      -0.03%
   10%            -0.01%      -0.01%  ...      -0.01%      -0.01%
   25%             -0.0%       -0.0%  ...       -0.0%       -0.0%
   50%              0.0%        0.0%  ...        0.0%        0.0%
   75%              0.0%       0.01%  ...       0.01%       0.01%
   90%             0.01%       0.01%  ...       0.01%       0.01%
   99%             0.02%       0.03%  ...       0.03%       0.03%
   max             0.14%       0.12%  ...       0.12%       0.12%
   skew           -1.12%      -0.48%  ...      -0.65%      -0.56%
   kurt           25.55%       13.5%  ...      18.86%      19.82%
   mad             0.01%       0.01%  ...       0.01%       0.01%

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** ME (10) ************************************

       *********************** Observation frequency: D ************************
                  me0-10     me10-20  ...     me80-90    me90-100
   startdate  1960-01-04  1960-01-04  ...  1960-01-04  1960-01-04
   enddate    2020-03-31  2020-03-31  ...  2020-03-31  2020-03-31
   count           15164       15164  ...       15164       15164
   mean             1698         460  ...         143         137
   std               891         245  ...          40          37
   min                19           6  ...           9           5
   1%                 19           6  ...           9           5
   10%               277         120  ...          82          79
   25%               768         336  ...         131         129
   50%              1838         437  ...         146         143
   75%              2422         589  ...         168         158
   90%              2804         814  ...         182         170
   99%              3242        1031  ...         225         217
   max              3405        1068  ...         243         225
   skew               -0           0  ...          -1          -1
   kurt               -1          -0  ...           1           2
   mad               747         193  ...          29          26

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** ME (10) ************************************

      ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: D ************************
   me_port        me0-10     me10-20  ...     me80-90    me90-100
   startdate  1960-01-04  1960-01-04  ...  1960-01-04  1960-01-04
   enddate    2020-03-31  2020-03-31  ...  2020-03-31  2020-03-31
   count           15164       15164  ...       15164       15164
   mean            47.56      181.07  ...      5954.2     29116.7
   std              50.4      192.23  ...     6609.56     34216.7
   min              4.93       14.73  ...      388.42     2031.14
   1%               6.52       20.06  ...      513.58      2466.8
   10%              9.79       27.66  ...       671.5     3050.29
   25%             13.27       41.11  ...      778.92     3440.26
   50%             20.22       80.72  ...      3240.1     11976.3
   75%             77.17      306.07  ...     9491.63       50586
   90%            126.97      509.56  ...     16009.9     76206.4
   99%            214.91      775.37  ...       32230      173378
   max            266.17      891.06  ...     36109.6      212162
   skew             1.53         1.3  ...        1.54        1.77
   kurt             1.72        0.66  ...        2.39        4.15
   mad             40.44      157.46  ...      5252.5     27607.3
   
   In [13]: # daily portfolios 
            _, _, _, = ff_D.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')

   *********************************** ME (10) ************************************
       *********************** Observation frequency: D ************************
       ************************* Returns: 1960-01-04 to 2020-03-31 **************************

   Correlation matrix:
           me0-10  me10-20  me20-30  me30-40  ...  me60-70  me70-80  me80-90  me90-100
   corr:   0.968    0.982    0.982    0.978  ...    0.985    0.988    0.992     0.996

   [1 rows x 10 columns] 

   Average matrix:
                            me0-10         me10-20  ...         me80-90        me90-100
   [wrds, kflib]:  [0.05%, 0.04%]  [0.05%, 0.05%]  ...  [0.04%, 0.04%]  [0.04%, 0.04%]

   [1 rows x 10 columns] 

   Std Deviation matrix:
                           me0-10         me10-20  ...        me80-90        me90-100
   [wrds, kflib]:  [0.99%, 0.92%]  [1.15%, 1.12%]  ...  [1.0%, 1.01%]  [1.03%, 1.02%]

   [1 rows x 10 columns] 
   
   Elapsed time:  93.507  seconds.



Portfolios Sorted on `Size` ``ME`` : Monthly
**********************************************

.. code-block:: ipython
   
   In [9]: ffFreq = 'M'
   In [10]: ff_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

**(3 x 1) Sorts**:

.. code-block:: ipython

   In [11]: sortingDim = [3]      
   In [12]: # Summary statistics
	    ff_M.getFamaFrenchStats('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
            ff_M.getFamaFrenchStats('Characs', ffFreq, startDate, endDate, sortingDim)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** ME (3) ************************************

       *********************** Observation frequency: M ************************
                  me0-30     me30-70    me70-100
   startdate  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31
   count             723         723         723
   mean            0.01%       0.01%       0.01%
   std             0.06%       0.05%       0.04%
   min            -0.34%       -0.3%      -0.21%
   1%             -0.17%      -0.14%       -0.1%
   10%            -0.06%      -0.05%      -0.04%
   25%            -0.02%      -0.02%      -0.02%
   50%             0.01%       0.01%       0.01%
   75%             0.05%       0.04%       0.03%
   90%             0.08%       0.07%       0.06%
   99%             0.15%       0.13%       0.11%
   max             0.28%       0.23%       0.18%
   skew           -0.52%      -0.74%       -0.4%
   kurt            3.25%        3.4%       1.74%
   mad             0.05%       0.04%       0.03% 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** ME (3) ************************************
 
      *********************** Observation frequency: M ************************
                  me0-30     me30-70    me70-100
   startdate  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31
   count             723         723         723
   mean             2456         799         433
   std              1245         276         121
   min                31          29          20
   1%                 31          29          20
   10%               491         343         240
   25%              1328         770         404
   50%              2534         850         453
   75%              3472         931         502
   90%              3949        1138         558
   99%              4693        1348         680
   max              4956        1428         718
   skew               -0          -1          -1
   kurt               -1           0           1
   mad              1013         204          88 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** ME (3) ************************************
 
     ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: M ************************
   me_port        me0-30     me30-70    me70-100
   startdate  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31
   count             723         723         723
   mean           115.54     1004.31     12182.6
   std            128.88     1060.45     13828.6
   min              9.06       74.98      864.46
   1%              11.88       98.22     1101.41
   10%             19.37      139.23     1363.76
   25%             27.38      177.75     1531.07
   50%             43.35       541.5     5477.92
   75%             189.7     1592.17       20489
   90%            306.94     2667.29     32628.8
   99%            568.47     4189.41     61689.2
   max             642.7      4691.3     69162.8
   skew             1.56        1.32        1.49
   kurt             1.88        0.89        2.07
   mad             102.6      851.04     11282.5 

   In [13]: # monthly portfolios 
            _, _, _, = ff_M.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    _, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
	    _, _, _, = ff_M.comparePortfolios('Characs', ffFreq, startDate, endDate, sortingDim)

   *********************************** ME (3) ************************************
       *********************** Observation frequency: M ************************
       ************************* Returns: 1960-01-31 to 2020-03-31 **************************
   
   Correlation matrix:
           me0-30  me30-70  me70-100
   corr:   0.993    0.995     0.997 

   Average matrix:
                            me0-30         me30-70        me70-100
   [wrds, kflib]:  [1.06%, 1.05%]  [1.01%, 1.02%]  [0.87%, 0.86%] 

   Std Deviation matrix:
                            me0-30       me30-70        me70-100
   [wrds, kflib]:  [6.25%, 6.09%]  [5.3%, 5.3%]  [4.22%, 4.25%] 

   Elapsed time:  100.566  seconds.

   *********************************** ME (3) ************************************
       *********************** Observation frequency: M ************************
    ************************* NumFirms: 1960-01-31 to 2020-03-31 **************************
   
   Correlation matrix:
           me0-30  me30-70  me70-100
   corr:   0.967    0.921     0.854 

   Average matrix:
                          me0-30     me30-70    me70-100
   [wrds, kflib]:  [2456, 2829]  [799, 870]  [433, 472] 

   Std Deviation matrix:
                          me0-30     me30-70   me70-100
   [wrds, kflib]:  [1245, 1281]  [276, 226]  [121, 82] 

   Elapsed time:  5.229  seconds.


   *********************************** ME (3) ************************************
       *********************** Observation frequency: M ************************
    ************************* (Characteristic: ME): 1960-01-31 to 2020-03-31 ***************************

   Correlation matrix:
           me0-30  me30-70  me70-100
   corr:   0.977    0.991     0.992 

   Average matrix:
                              me0-30            me30-70              me70-100
   [wrds, kflib]:  [115.54, 105.23]  [1004.31, 946.07]  [12182.59, 11808.07] 

   Std Deviation matrix:
                              me0-30            me30-70              me70-100
   [wrds, kflib]:  [128.88, 113.05]  [1060.45, 999.73]  [13828.64, 13245.28] 

   Elapsed time:  5.097  seconds.


**(5 x 1) Quintile Sorts**:

.. code-block:: ipython

   In [11]: sortingDim = [5]   
   In [12]: # Summary statistics
	    ff_M.getFamaFrenchStats('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
            ff_M.getFamaFrenchStats('Characs', ffFreq, startDate, endDate, sortingDim)

   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** ME (5) ************************************

       *********************** Observation frequency: M ************************
                  me0-20     me20-40     me40-60     me60-80    me80-100
   startdate  1960-01-31  1960-01-31  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31  2020-03-31  2020-03-31
   count             723         723         723         723         723
   mean            0.01%       0.01%       0.01%       0.01%       0.01%
   std             0.06%       0.06%       0.05%       0.05%       0.04%
   min            -0.36%      -0.37%      -0.28%      -0.25%       -0.2%
   1%             -0.17%      -0.16%      -0.14%      -0.13%       -0.1%
   10%            -0.07%      -0.06%      -0.05%      -0.05%      -0.04%
   25%            -0.02%      -0.02%      -0.02%      -0.02%      -0.02%
   50%             0.01%       0.02%       0.01%       0.01%       0.01%
   75%             0.05%       0.05%       0.05%       0.04%       0.03%
   90%             0.08%       0.08%       0.07%       0.07%       0.06%
   99%             0.16%       0.13%       0.13%       0.13%       0.11%
   max             0.29%       0.26%       0.23%       0.19%       0.18%
   skew           -0.41%      -0.77%      -0.69%       -0.5%      -0.38%
   kurt            3.43%       3.86%       3.02%       2.04%       1.72%
   mad             0.05%       0.04%       0.04%       0.04%       0.03% 
   
   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** ME (5) ************************************

       *********************** Observation frequency: M ************************
                  me0-20     me20-40     me40-60     me60-80    me80-100
   startdate  1960-01-31  1960-01-31  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31  2020-03-31  2020-03-31
   count             723         723         723         723         723
   mean             2143         563         387         315         279
   std              1111         237         132          95          76
   min                25          15          15          11          14
   1%                 25          15          15          11          14
   10%               399         179         174         161         161
   25%              1072         483         374         304         262
   50%              2230         596         411         330         288
   75%              3056         694         448         360         325
   90%              3480         879         547         433         348
   99%              4144         995         675         516         438
   max              4391        1029         711         543         465
   skew               -0          -0          -1          -1          -1
   kurt               -1          -0           0           1           1
   mad               915         182          96          68          55 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** ME (5) ************************************

      ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: M ************************
   me_port        me0-20     me20-40     me40-60     me60-80    me80-100
   startdate  1960-01-31  1960-01-31  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31  2020-03-31  2020-03-31
   count             723         723         723         723         723
   mean            79.77      415.45       988.3     2430.13     17081.2
   std             86.74      442.15     1061.08     2628.59     19199.7
   min              6.91       29.26       70.13      180.85     1225.56
   1%               9.11       38.89       90.45      237.84     1515.12
   10%             14.47       55.99      128.05      321.45      1872.1
   25%             19.81       79.64      166.96      389.72     2094.28
   50%             31.52      191.98      539.09     1434.43     7476.49
   75%            132.12       694.7      1562.8     3702.32     29182.1
   90%            217.95     1138.24      2580.5     6339.92     45295.8
   99%            378.94      1689.9     4528.82     11427.2     81277.5
   max            430.04     1908.78     5205.69     14078.5     90732.4
   skew             1.51        1.23        1.42         1.6        1.38
   kurt             1.67        0.38        1.48        2.56         1.5
   mad             69.68       362.5      844.08     2042.27     15897.7 
   
   In [13]: # monthly portfolios 
            _, _, _, = ff_M.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    _, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
	    _, _, _, = ff_M.comparePortfolios('Characs', ffFreq, startDate, endDate, sortingDim)
   
   *********************************** ME (5) ************************************
       *********************** Observation frequency: M ************************
    ************************* Returns: 1960-01-31 to 2020-03-31 **************************

   Correlation matrix:
           me0-20  me20-40  me40-60  me60-80  me80-100
   corr:    0.99    0.989    0.995    0.994     0.997 

   Average matrix:
                            me0-20         me20-40  ...        me60-80        me80-100
   [wrds, kflib]:  [1.07%, 1.03%]  [1.03%, 1.05%]  ...  [1.04%, 1.0%]  [0.86%, 0.84%]

   [1 rows x 5 columns] 

   Std Deviation matrix:
                            me0-20         me20-40  ...         me60-80        me80-100
   [wrds, kflib]:  [6.43%, 6.21%]  [5.96%, 5.85%]  ...  [4.91%, 5.03%]  [4.19%, 4.21%]

   [1 rows x 5 columns] 

   Elapsed time:  5.526  seconds.

   *********************************** ME (5) ************************************
       *********************** Observation frequency: M ************************
    ************************* NumFirms: 1960-01-31 to 2020-03-31 **************************

   Correlation matrix:
           me0-20  me20-40  me40-60  me60-80  me80-100
   corr:   0.966    0.958    0.916     0.88     0.834 

   Average matrix:
                          me0-20     me20-40     me40-60     me60-80    me80-100
   [wrds, kflib]:  [2143, 2485]  [563, 617]  [387, 421]  [315, 344]  [279, 305] 

   Std Deviation matrix:
                          me0-20     me20-40     me40-60   me60-80  me80-100
   [wrds, kflib]:  [1111, 1163]  [237, 213]  [132, 109]  [95, 70]  [76, 50] 

   Elapsed time:  5.515  seconds.

   *********************************** ME (5) ************************************
       *********************** Observation frequency: M ************************
    ************************* (Characteristic: ME): 1960-01-31 to 2020-03-31 ***************************

   Correlation matrix:
           me0-20  me20-40  me40-60  me60-80  me80-100
   corr:    0.97    0.992    0.983    0.982     0.994 

   Average matrix:
                            me0-20  ...              me80-100
   [wrds, kflib]:  [79.77, 72.27]  ...  [17081.19, 16670.08]

   [1 rows x 5 columns] 

   Std Deviation matrix:
                            me0-20  ...              me80-100
   [wrds, kflib]:  [86.74, 74.75]  ...  [19199.67, 18704.98]

   [1 rows x 5 columns] 

   Elapsed time:  5.268  seconds.


**(10 x 1) Decile Sorts**:

.. code-block:: ipython

   In [11]: sortingDim = [10]   
   In [12]: # Summary statistics
	    ff_M.getFamaFrenchStats('Returns', ffFreq, startDate, endDate, sortingDim, 'vw'
	    ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
            ff_M.getFamaFrenchStats('Characs', ffFreq, startDate, endDate, sortingDim)

   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** ME (10) ************************************
   
    *********************** Observation frequency: M ************************
                  me0-10     me10-20  ...     me80-90    me90-100
   startdate  1960-01-31  1960-01-31  ...  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  ...  2020-03-31  2020-03-31
   count             723         723  ...         723         723
   mean            0.01%       0.01%  ...       0.01%       0.01%
   std             0.07%       0.06%  ...       0.05%       0.04%
   min            -0.41%      -0.31%  ...      -0.22%       -0.2%
   1%             -0.19%      -0.17%  ...      -0.11%       -0.1%
   10%            -0.06%      -0.07%  ...      -0.05%      -0.04%
   25%            -0.02%      -0.03%  ...      -0.02%      -0.01%
   50%             0.01%       0.01%  ...       0.01%       0.01%
   75%             0.05%       0.05%  ...       0.04%       0.03%
   90%             0.08%       0.08%  ...       0.06%       0.05%
   99%             0.17%       0.16%  ...       0.12%       0.11%
   max             0.31%        0.3%  ...       0.18%       0.18%
   skew           -0.46%      -0.32%  ...      -0.44%      -0.36%
   kurt            4.38%       2.65%  ...       1.99%       1.65%
   mad             0.05%       0.05%  ...       0.03%       0.03%

   [17 rows x 10 columns] 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** ME (10) ************************************
    
   *********************** Observation frequency: M ************************
                  me0-10     me10-20  ...     me80-90    me90-100
   startdate  1960-01-31  1960-01-31  ...  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  ...  2020-03-31  2020-03-31
   count             723         723  ...         723         723
   mean             1686         457  ...         142         137
   std               886         244  ...          40          37
   min                19           6  ...           9           5
   1%                 19           6  ...           9           5
   10%               277         120  ...          82          79
   25%               766         336  ...         131         130
   50%              1829         435  ...         146         143
   75%              2400         586  ...         167         158
   90%              2788         803  ...         182         169
   99%              3206        1026  ...         225         213
   max              3368        1052  ...         241         224
   skew               -0           0  ...          -1          -1
   kurt               -1          -0  ...           1           2
   mad               743         192  ...          29          26
   
   [17 rows x 10 columns] 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** ME (10) ************************************
   
      ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: M ************************
   me_port        me0-10     me10-20  ...     me80-90    me90-100
   startdate  1960-01-31  1960-01-31  ...  1960-01-31  1960-01-31
   count             723         723  ...         723         723
   mean            48.03      182.37  ...     5976.78     29190.2
   std             50.67      193.25  ...     6615.78     34276.4
   min              5.04       15.22  ...      393.83     2080.73
   1%               6.61       20.88  ...       517.7     2512.42
   10%              9.92       27.74  ...      673.95     3057.81
   25%             13.29       41.36  ...      777.04     3452.13
   50%              20.4        80.7  ...     3208.76     12057.3
   75%             76.74      305.09  ...     9556.76     50541.4
   90%            128.01      513.19  ...     16083.4     76165.6
   99%            213.24      774.53  ...     30900.9      174582
   max            259.13      891.06  ...     33968.9      193829
   skew              1.5        1.29  ...        1.51        1.75
   kurt             1.58        0.61  ...        2.21        4.01
   mad             40.79      158.53  ...     5273.11     27671.3

   [17 rows x 10 columns] 
   
   In [13]: # monthly portfolios 
            _, _, _, = ff_M.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    _, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
	    _, _, _, = ff_M.comparePortfolios('Characs', ffFreq, startDate, endDate, sortingDim)

   *********************************** ME (10) ************************************
       *********************** Observation frequency: M ************************
    ************************* Returns: 1960-01-31 to 2020-03-31 **************************

   Correlation matrix:
           me0-10  me10-20  me20-30  me30-40  ...  me60-70  me70-80  me80-90  me90-100
   corr:   0.984     0.99    0.991    0.983  ...     0.99    0.988    0.994     0.996

   [1 rows x 10 columns] 

   Average matrix:
                            me0-10         me10-20  ...         me80-90        me90-100
   [wrds, kflib]:  [1.08%, 1.04%]  [1.07%, 1.02%]  ...  [0.91%, 0.94%]  [0.85%, 0.83%]

   [1 rows x 10 columns] 

   Std Deviation matrix:
                            me0-10         me10-20  ...         me80-90        me90-100
   [wrds, kflib]:  [6.51%, 6.23%]  [6.44%, 6.27%]  ...  [4.54%, 4.56%]  [4.18%, 4.19%]

   [1 rows x 10 columns] 

   Elapsed time:  5.62  seconds.

   *********************************** ME (10) ************************************
       *********************** Observation frequency: M ************************
    ************************* NumFirms: 1960-01-31 to 2020-03-31 **************************

   Correlation matrix:
           me0-10  me10-20  me20-30  me30-40  ...  me60-70  me70-80  me80-90  me90-100
   corr:   0.965    0.969    0.964     0.94  ...    0.875    0.881    0.847     0.817

   [1 rows x 10 columns] 

   Average matrix:
                          me0-10     me10-20  ...     me80-90    me90-100
   [wrds, kflib]:  [1686, 1973]  [457, 512]  ...  [142, 156]  [137, 149]

   [1 rows x 10 columns] 

   Std Deviation matrix:
                        me0-10     me10-20  ...   me80-90  me90-100
   [wrds, kflib]:  [886, 955]  [244, 234]  ...  [40, 28]  [37, 23]

   [1 rows x 10 columns] 

   Elapsed time:  5.308  seconds.

   *********************************** ME (10) ************************************
       *********************** Observation frequency: M ************************
    ************************* (Characteristic: ME): 1960-01-31 to 2020-03-31 ***************************

   Correlation matrix:
           me0-10  me10-20  me20-30  me30-40  ...  me60-70  me70-80  me80-90  me90-100
   corr:   0.952    0.985    0.992    0.993  ...    0.992     0.98    0.985     0.981

   [1 rows x 10 columns] 

   Average matrix:
                            me0-10  ...              me90-100
   [wrds, kflib]:  [48.03, 43.31]  ...  [29190.16, 28203.72]

   [1 rows x 10 columns] 

   Std Deviation matrix:
                            me0-10  ...              me90-100
   [wrds, kflib]:  [50.67, 43.18]  ...  [34276.36, 31739.34]

   [1 rows x 10 columns] 

   Elapsed time:  5.263  seconds.


Portfolios Sorted on `Size` ``ME`` : Annual
**********************************************

.. code-block:: ipython

   In [9]: ffFreq = 'A'
   In [10]: ff_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

**(3 x 1) Sorts**:

.. code-block:: ipython

   In [11]: sortingDim = [3]      
   In [12]: # Summary statistics
	    ff_A.getFamaFrenchStats('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
            ff_A.getFamaFrenchStats('Characs', ffFreq, startDate, endDate, sortingDim)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...

   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** ME (3) ************************************

       *********************** Observation frequency: A ************************
                  me0-30     me30-70    me70-100
   startdate  1960-12-31  1960-12-31  1960-12-31
   enddate    2019-12-31  2019-12-31  2019-12-31
   count              60          60          60
   mean            0.15%       0.14%       0.11%
   std             0.26%       0.19%       0.17%
   min            -0.37%      -0.35%      -0.37%
   1%             -0.36%      -0.31%      -0.31%
   10%            -0.14%      -0.11%       -0.1%
   25%            -0.06%       0.01%       0.02%
   50%             0.19%       0.17%       0.14%
   75%             0.33%       0.27%       0.23%
   90%             0.46%       0.38%       0.32%
   99%             0.77%       0.48%       0.37%
   max             0.92%       0.52%       0.38%
   skew            0.27%      -0.36%      -0.63%
   kurt            0.26%      -0.16%       0.13%
   mad             0.21%       0.16%       0.13% 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** ME (3) ************************************
       *********************** Observation frequency: A ************************
                  me0-30     me30-70    me70-100
   startdate  1960-12-31  1960-12-31  1960-12-31
   enddate    2019-12-31  2019-12-31  2019-12-31
   count              60          60          60
   mean             2465         802         436
   std              1236         269         115
   min               150         198         148
   1%                167         201         149
   10%               627         388         254
   25%              1665         770         413
   50%              2531         848         451
   75%              3484         925         501
   90%              3826        1115         550
   99%              4559        1260         648
   max              4577        1273         669
   skew               -0          -1          -1
   kurt               -1          -0           1
   mad              1003         199          85 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** ME (3) ************************************
   
      ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: A ************************
   me_port        me0-30     me30-70    me70-100
   startdate  1960-12-31  1960-12-31  1960-12-31
   enddate    2019-12-31  2019-12-31  2019-12-31
   count              60          60          60
   mean           108.53      972.74       11929
   std            122.78     1031.99     13392.2
   min             11.14       89.06     1063.89
   1%              12.24      102.95     1114.86
   10%             18.09      133.45     1345.73
   25%             25.45       170.1        1486
   50%             42.29      541.39     5630.78
   75%            173.37      1541.8     19383.4
   90%            295.95     2680.51     30816.7
   99%            450.68     3878.05     51804.7
   max            606.37     4026.68     54933.1
   skew             1.74        1.31        1.36
   kurt             3.35         0.8        1.31
   mad             96.17      825.58     11045.4 
   
   In [13]: # annual portfolios 
            _, _, _, = ff_A.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    _, _, _, = ff_A.comparePortfolios('Characs', ffFreq, startDate, endDate, sortingDim)

   *********************************** ME (3) ************************************
       *********************** Observation frequency: A ************************
    ************************* Returns: 1960-12-31 to 2019-12-31 **************************

   Correlation matrix:
           me0-30  me30-70  me70-100
   corr:   0.996    0.995     0.999 

   Average matrix:
                              me0-30           me30-70          me70-100
   [wrds, kflib]:  [15.24%, 14.61%]  [13.64%, 13.64%]  [11.38%, 11.35%] 

   Std Deviation matrix:
                              me0-30           me30-70          me70-100
   [wrds, kflib]:  [25.86%, 25.79%]  [19.42%, 20.24%]  [16.64%, 16.64%] 

   Elapsed time:  64.261  seconds.

   *********************************** ME (3) ************************************
       *********************** Observation frequency: A ************************
      ************************** (Characteristic: ME) ***************************
      ******************************* NOT AVAILABLE *****************************

   Elapsed time:  5.53  seconds.


**(5 x 1) Quintile Sorts**:

.. code-block:: ipython

   In [11]: sortingDim = [5]   
   In [12]: # Summary statistics
	    ff_A.getFamaFrenchStats('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
            ff_A.getFamaFrenchStats('Characs', ffFreq, startDate, endDate, sortingDim)

   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** ME (5) ************************************
       
      *********************** Observation frequency: A ************************
                  me0-20     me20-40     me40-60     me60-80    me80-100
   startdate  1960-12-31  1960-12-31  1960-12-31  1960-12-31  1960-12-31
   enddate    2019-12-31  2019-12-31  2019-12-31  2019-12-31  2019-12-31
   count              60          60          60          60          60
   mean            0.16%       0.14%       0.14%       0.13%       0.11%
   std             0.28%       0.22%        0.2%       0.18%       0.17%
   min            -0.39%      -0.34%      -0.32%       -0.4%      -0.36%
   1%             -0.38%      -0.32%       -0.3%      -0.33%      -0.31%
   10%            -0.15%      -0.16%      -0.12%      -0.08%      -0.11%
   25%            -0.07%      -0.03%        0.0%       0.02%       0.02%
   50%             0.18%       0.17%       0.16%       0.16%       0.14%
   75%             0.32%       0.27%       0.29%       0.27%       0.22%
   90%             0.48%       0.42%       0.37%       0.36%       0.32%
   99%             0.86%       0.59%        0.5%       0.45%       0.36%
   max             1.01%       0.63%       0.51%        0.5%       0.39%
   skew            0.38%      -0.12%       -0.3%      -0.56%       -0.6%
   kurt            0.49%      -0.34%      -0.32%       0.37%        0.1%
   mad             0.22%       0.17%       0.16%       0.14%       0.13% 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** ME (5) ************************************
       
   *********************** Observation frequency: A ************************
                  me0-20     me20-40     me40-60     me60-80    me80-100
   startdate  1960-12-31  1960-12-31  1960-12-31  1960-12-31  1960-12-31
   enddate    2019-12-31  2019-12-31  2019-12-31  2019-12-31  2019-12-31
   count              60          60          60          60          60
   mean             2151         564         389         317         282
   std              1104         233         129          91          72
   min               102          97         100          98          99
   1%                116         101         101          99         100
   10%               505         214         192         171         168
   25%              1432         466         377         309         265
   50%              2231         595         412         331         289
   75%              3079         675         448         361         325
   90%              3394         878         537         423         351
   99%              4011         958         623         484         417
   max              4015         962         627         502         430
   skew               -0          -0          -1          -1          -1
   kurt               -1          -1           0           0           1
   mad               907         179          94          65          53 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** ME (5) ************************************
      
      ************************** (Characteristic: ME) ***************************
    *********************** Observation frequency: A ************************
   me_port        me0-20     me20-40     me40-60     me60-80    me80-100
   startdate  1960-12-31  1960-12-31  1960-12-31  1960-12-31  1960-12-31
   enddate    2019-12-31  2019-12-31  2019-12-31  2019-12-31  2019-12-31
   count              60          60          60          60          60
   mean            74.52      394.62      942.41     2323.61     16773.3
   std             81.93      419.25      992.02     2434.72     18695.7
   min              8.56       35.89       83.82      217.01      1523.9
   1%               9.47       42.23       96.96      249.07     1550.61
   10%             13.59       55.05      121.25      306.41     1845.78
   25%              18.6       75.46       159.4      376.71     2046.98
   50%             29.81      185.38      533.89      1447.4     7786.82
   75%             117.5      642.98     1517.36     3524.15       28126
   90%            198.91     1071.54     2543.06     6175.21     42740.2
   99%            297.21     1455.73     3612.33     9322.32     71379.2
   max            403.81     1787.37      3930.2     9771.45     73873.9
   skew             1.69        1.28        1.25        1.32        1.28
   kurt             3.09        0.83         0.6        1.01        0.98
   mad              64.8       341.7      800.62      1940.2     15615.2 
   
   In [13]: # annual portfolios 
            _, _, _, = ff_A.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    _, _, _, = ff_A.comparePortfolios('Characs', ffFreq, startDate, endDate, sortingDim)

   *********************************** ME (5) ************************************
       *********************** Observation frequency: A ************************
    ************************* Returns: 1960-12-31 to 2019-12-31 **************************

   Correlation matrix:
           me0-20  me20-40  me40-60  me60-80  me80-100
   corr:   0.996    0.995    0.996    0.995       1.0 

   Average matrix:
                              me0-20  ...         me80-100
   [wrds, kflib]:  [15.53%, 14.53%]  ...  [11.21%, 11.2%]

   [1 rows x 5 columns] 

   Std Deviation matrix:
                              me0-20  ...          me80-100
   [wrds, kflib]:  [27.84%, 27.64%]  ...  [16.69%, 16.67%]

   [1 rows x 5 columns] 

   Elapsed time:  5.455  seconds.

   *********************************** ME (5) ************************************
       *********************** Observation frequency: A ************************
      ************************** (Characteristic: ME) ***************************
      ******************************* NOT AVAILABLE *****************************

   Elapsed time:  5.454  seconds.


**(10 x 1) Decile Sorts**:

.. code-block:: ipython

   In [11]: sortingDim = [10]   
   In [12]: # Summary statistics
	   ff_A.getFamaFrenchStats('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	   ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
           ff_A.getFamaFrenchStats('Characs', ffFreq, startDate, endDate, sortingDim)
   
   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** ME (10) ************************************
       
      *********************** Observation frequency: A ************************
                  me0-10     me10-20  ...     me80-90    me90-100
   startdate  1960-12-31  1960-12-31  ...  1960-12-31  1960-12-31
   enddate    2019-12-31  2019-12-31  ...  2019-12-31  2019-12-31
   count              60          60  ...          60          60
   mean            0.17%       0.15%  ...       0.12%       0.11%
   std             0.31%       0.26%  ...       0.17%       0.17%
   min            -0.44%      -0.36%  ...      -0.42%      -0.35%
   1%              -0.4%      -0.36%  ...      -0.32%      -0.31%
   10%            -0.16%      -0.15%  ...      -0.11%      -0.12%
   25%            -0.07%      -0.05%  ...        0.0%       0.02%
   50%             0.18%       0.16%  ...       0.15%       0.13%
   75%             0.33%       0.31%  ...       0.21%       0.23%
   90%             0.49%       0.46%  ...       0.36%       0.33%
   99%             1.01%       0.73%  ...       0.39%       0.37%
   max             1.14%       0.85%  ...        0.4%        0.4%
   skew            0.56%       0.21%  ...      -0.66%      -0.54%
   kurt            0.83%      -0.09%  ...       0.55%        0.0%
   mad             0.24%       0.21%  ...       0.13%       0.14%

   [17 rows x 10 columns] 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** ME (10) ************************************
 
      *********************** Observation frequency: A ************************
                  me0-10     me10-20  ...     me80-90    me90-100
   startdate  1960-12-31  1960-12-31  ...  1960-12-31  1960-12-31
   enddate    2019-12-31  2019-12-31  ...  2019-12-31  2019-12-31
   count              60          60  ...          60          60
   mean             1693         459  ...         143         138
   std               880         241  ...          38          34
   min                50          52  ...          50          49
   1%                 61          55  ...          50          49
   10%               342         127  ...          85          84
   25%              1120         334  ...         134         131
   50%              1824         434  ...         146         143
   75%              2423         584  ...         167         158
   90%              2814         798  ...         182         167
   99%              3090         955  ...         217         200
   max              3129         959  ...         222         208
   skew               -0           0  ...          -1          -1
   kurt               -1          -0  ...           0           1
   mad               736         189  ...          28          25

   [17 rows x 10 columns] 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** ME (10) ************************************
      
      ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: A ************************
   me_port        me0-10     me10-20  ...     me80-90    me90-100
   startdate  1960-12-31  1960-12-31  ...  1960-12-31  1960-12-31
   enddate    2019-12-31  2019-12-31  ...  2019-12-31  2019-12-31
   count              60          60  ...          60          60
   mean             43.8      172.34  ...     5864.92     28683.3
   std             45.22      183.15  ...     6498.16     32929.6
   min              6.35       18.62  ...      481.31     2585.48
   1%               6.87       21.56  ...      528.61     2600.09
   10%              9.53       27.81  ...      667.11     3019.31
   25%             13.09       40.34  ...      750.28     3341.11
   50%             19.29       78.43  ...     3294.32     12388.6
   75%             67.14      278.14  ...     9030.16     49917.9
   90%            113.14      461.86  ...       15338     72507.6
   99%            164.27      646.13  ...     25135.2      128625
   max            206.39      827.85  ...     28501.7      149494
   skew             1.47        1.41  ...        1.44        1.47
   kurt             1.62         1.5  ...        1.74        2.13
   mad             36.51      148.07  ...     5182.42     27165.5

   [17 rows x 10 columns] 
   
   In [13]: # annual portfolios 
           _, _, _, = ff_A.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	   _, _, _, = ff_A.comparePortfolios('Characs', ffFreq, startDate, endDate, sortingDim)

   *********************************** ME (10) ************************************
       *********************** Observation frequency: A ************************
    ************************* Returns: 1960-12-31 to 2019-12-31 **************************

   Correlation matrix:
           me0-10  me10-20  me20-30  me30-40  ...  me60-70  me70-80  me80-90  me90-100
   corr:   0.969    0.992    0.989    0.991  ...     0.99    0.986    0.996     0.999

   [1 rows x 10 columns] 

   Average matrix:
                              me0-10  ...         me90-100
   [wrds, kflib]:  [16.85%, 15.07%]  ...  [11.1%, 10.97%]

   [1 rows x 10 columns] 

   Std Deviation matrix:
                              me0-10  ...          me90-100
   [wrds, kflib]:  [30.64%, 29.93%]  ...  [16.85%, 16.78%]

   [1 rows x 10 columns] 

   Elapsed time:  5.69  seconds.

   *********************************** ME (10) ************************************
       *********************** Observation frequency: A ************************
      ************************** (Characteristic: ME) ***************************
      ******************************* NOT AVAILABLE *****************************

   Elapsed time:  5.396  seconds



Portfolios Sorted on `Book-to-Market` ``BM``
#############################################

.. code-block:: ipython

   In [8]: ffFactors, ffsortCharac, ffportCharac = [], ['BM'], ['ME', 'BM']



Portfolios Sorted on `Book-to-Market` ``BM`` : Monthly
*******************************************************


.. code-block:: ipython
   
   In [9]: ffFreq = 'M'
   In [10]: ff_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

**(3 x 1) Sorts**:

.. code-block:: ipython

   In [11]: sortingDim = [3]      
   In [12]: # Summary statistics
	    ff_M.getFamaFrenchStats('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
            ff_M.getFamaFrenchStats('Characs', ffFreq, startDate, endDate, sortingDim)

   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** BM (3) ************************************

       *********************** Observation frequency: M ************************
                  bm0-30     bm30-70    bm70-100
   startdate  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31
   count             723         723         723
   mean            0.01%       0.01%       0.01%
   std             0.05%       0.04%       0.05%
   min            -0.24%      -0.21%      -0.26%
   1%             -0.11%       -0.1%      -0.14%
   10%            -0.05%      -0.04%      -0.04%
   25%            -0.02%      -0.01%      -0.01%
   50%             0.01%       0.01%       0.01%
   75%             0.04%       0.03%       0.04%
   90%             0.06%       0.06%       0.06%
   99%             0.11%       0.11%       0.12%
   max             0.21%       0.18%       0.23%
   skew           -0.42%      -0.42%      -0.61%
   kurt             1.9%        2.4%       3.37%
   mad             0.04%       0.03%       0.04% 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** BM (3) ************************************

       *********************** Observation frequency: M ************************
                  bm0-30     bm30-70    bm70-100
   startdate  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31
   count             723         723         723
   mean             1193        1161        1145
   std               574         473         545
   min                29          24          24
   1%                 29          24          24
   10%               292         388         343
   25%               767         894         776
   50%              1178        1263        1205
   75%              1712        1460        1388
   90%              1924        1677        1981
   99%              2137        2048        2253
   max              2187        2165        2332
   skew               -0          -1          -0
   kurt               -1          -0          -0
   mad               477         369         414 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** BM (3) ************************************

      ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: M ************************
   bm_port        bm0-30     bm30-70    bm70-100
   startdate  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31
   count             723         723         723
   mean          3518.31     2004.91       784.4
   std           4936.54     3063.72     1070.41
   min            227.66      118.11       31.15
   1%             282.44      132.87       34.36
   10%            350.87      269.04      102.17
   25%            475.41      379.56      134.83
   50%            925.31      739.42      354.47
   75%           5757.95     2448.26      852.39
   90%           9194.79     6008.14     2162.87
   99%           28097.8     20796.7      5319.9
   max           32299.9     23487.3     5818.27
   skew             2.73        3.96        2.36
   kurt               10       21.62        5.87
   mad           3564.83     1939.34      763.55 

      ************************** (Characteristic: BM) ***************************
       *********************** Observation frequency: M ************************
   bm_port        bm0-30     bm30-70    bm70-100
   startdate  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31
   count             723         723         723
   mean             0.28        0.69        1.33
   std              0.12        0.28        0.55
   min              0.07         0.3        0.73
   1%               0.08        0.31        0.74
   10%              0.16        0.43        0.83
   25%               0.2        0.48        0.95
   50%              0.24         0.6        1.22
   75%              0.34        0.78        1.47
   90%              0.48        1.08        1.86
   99%               0.7         1.8        3.64
   max              0.72         1.8        4.21
   skew             1.21        1.57        2.19
   kurt             1.32        3.03        6.58
   mad              0.09        0.21        0.38 
	
   In [13]: # monthly portfolios 
            _, _, _, = ff_M.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    _, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
	    _, _, _, = ff_M.comparePortfolios('Characs', ffFreq, startDate, endDate, sortingDim)

   *********************************** BM (3) ************************************
       *********************** Observation frequency: M ************************
    ************************* Returns: 1960-01-31 to 2020-03-31 **************************

   Correlation matrix:
           bm0-30  bm30-70  bm70-100
   corr:   0.997    0.984     0.992 

   Average matrix:
                            bm0-30         bm30-70        bm70-100
   [wrds, kflib]:  [0.86%, 0.87%]  [0.94%, 0.91%]  [1.08%, 1.08%] 

   Std Deviation matrix:
                            bm0-30        bm30-70        bm70-100
   [wrds, kflib]:  [4.63%, 4.62%]  [4.23%, 4.3%]  [4.97%, 4.93%] 

   Elapsed time:  82.019  seconds.


   *********************************** BM (3) ************************************
       *********************** Observation frequency: M ************************
    ************************* NumFirms: 1960-01-31 to 2020-03-31 **************************

   Correlation matrix:
           bm0-30  bm30-70  bm70-100
   corr:    0.98    0.959     0.977 

   Average matrix:
                          bm0-30       bm30-70      bm70-100
   [wrds, kflib]:  [1193, 1235]  [1161, 1204]  [1145, 1149] 

   Std Deviation matrix:
                        bm0-30     bm30-70    bm70-100
   [wrds, kflib]:  [574, 524]  [473, 405]  [545, 472] 

   Elapsed time:  6.995  seconds.

   *********************************** BM (3) ************************************
       *********************** Observation frequency: M ************************
    ************************* (Characteristic: ME): 1960-01-31 to 2020-03-31 ***************************

   Correlation matrix:
           bm0-30  bm30-70  bm70-100
   corr:   0.973    0.834     0.974 

   Average matrix:
                                bm0-30             bm30-70         bm70-100
   [wrds, kflib]:  [3518.31, 3229.51]  [2004.91, 1751.94]  [784.4, 821.77] 

   Std Deviation matrix:
                                bm0-30             bm30-70            bm70-100
   [wrds, kflib]:  [4936.54, 4140.62]  [3063.72, 2117.63]  [1070.41, 1080.39] 

   *********************************** BM (3) ************************************
       *********************** Observation frequency: M ************************
      ************************** (Characteristic: BM) ***************************
      ******************************* NOT AVAILABLE *****************************

   Elapsed time:  4.481  seconds.


**(5 x 1) Sorts**:


.. code-block:: ipython

   In [11]: sortingDim = [5]      
   In [12]: # Summary statistics
	    ff_M.getFamaFrenchStats('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
            ff_M.getFamaFrenchStats('Characs', ffFreq, startDate, endDate, sortingDim)

   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** BM (5) ************************************

       *********************** Observation frequency: M ************************
                  bm0-20     bm20-40     bm40-60     bm60-80    bm80-100
   startdate  1960-01-31  1960-01-31  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31  2020-03-31  2020-03-31
   count             723         723         723         723         723
   mean            0.01%       0.01%       0.01%       0.01%       0.01%
   std             0.05%       0.04%       0.04%       0.05%       0.05%
   min            -0.24%      -0.25%      -0.22%      -0.48%      -0.21%
   1%             -0.12%      -0.11%      -0.11%      -0.15%      -0.15%
   10%            -0.05%      -0.04%      -0.04%      -0.04%      -0.05%
   25%            -0.02%      -0.02%      -0.01%      -0.01%      -0.02%
   50%             0.01%       0.01%       0.01%       0.01%       0.02%
   75%             0.04%       0.04%       0.03%       0.04%       0.04%
   90%             0.06%       0.06%       0.06%       0.06%       0.07%
   99%             0.11%       0.11%       0.11%       0.12%       0.13%
   max             0.22%       0.16%       0.17%       0.22%       0.26%
   skew           -0.37%       -0.5%      -0.49%      -1.76%      -0.29%
   kurt            1.69%       2.28%       2.44%      15.43%       2.07%
   mad             0.04%       0.03%       0.03%       0.03%       0.04% 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** BM (5) ************************************
   
       *********************** Observation frequency: M ************************
                  bm0-20     bm20-40     bm40-60     bm60-80    bm80-100
   startdate  1960-01-31  1960-01-31  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31  2020-03-31  2020-03-31
   count             723         723         723         723         723
   mean              882         605         573         613         825
   std               451         248         236         267         405
   min                19          15          14          13          16
   1%                 19          15          14          13          16
   10%               201         188         197         206         231
   25%               552         438         458         504         500
   50%               822         650         620         637         871
   75%              1278         774         732         742        1036
   90%              1485         850         806         949        1429
   99%              1658        1087        1054        1179        1662
   max              1692        1155        1133        1235        1746
   skew               -0          -1          -1          -0          -0
   kurt               -1          -0          -0          -0          -0
   mad               381         197         185         195         313 

   *********************************** Summary Statistics: Firm Characteristics ***********************************
             *********************************** BM (5) ************************************

      ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: M ************************
   bm_port        bm0-20     bm20-40     bm40-60     bm60-80    bm80-100
   startdate  1960-01-31  1960-01-31  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31  2020-03-31  2020-03-31
   count             723         723         723         723         723
   mean          3855.98     2854.28     1829.46     1239.75      620.67
   std           6213.33     4312.59     2230.86     1498.27      833.82
   min            206.95      139.85      135.58       57.89        22.2
   1%             261.18      166.31      147.51       69.99       24.67
   10%            366.42      278.66       264.4      160.56       76.39
   25%            507.95      388.57      347.39      263.35      115.34
   50%            997.17      902.61      745.15      661.39      251.51
   75%           5931.66     3989.12     2297.31     1443.52      569.19
   90%            8542.2     8891.27     5886.38     3388.98     1878.96
   99%           41645.1     27194.9     8656.41      7796.9     3341.71
   max           48373.6     29893.2     10535.4     8368.98     3673.48
   skew             4.09        3.24         1.7        2.17        1.94
   kurt             22.5       14.56           2         5.4        2.87
   mad           3942.52     2886.93     1696.68     1098.93      618.67 

      ************************** (Characteristic: BM) ***************************
       *********************** Observation frequency: M ************************
   bm_port        bm0-20     bm20-40     bm40-60     bm60-80    bm80-100
   startdate  1960-01-31  1960-01-31  1960-01-31  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  2020-03-31  2020-03-31  2020-03-31
   count             723         723         723         723         723
   mean             0.24        0.49        0.69        0.94        1.57
   std               0.1         0.2        0.27        0.36        0.71
   min              0.06        0.26        0.35        0.54        0.82
   1%               0.06        0.26        0.35        0.54        0.83
   10%              0.13         0.3        0.43        0.62        0.95
   25%              0.17        0.35        0.49        0.69         1.1
   50%               0.2        0.43        0.61        0.84        1.45
   75%              0.29        0.55        0.77        1.03        1.74
   90%              0.41        0.76        1.08        1.43        2.19
   99%              0.54        1.32        1.83         2.5        4.88
   max              0.55        1.32        1.83         2.5        5.36
   skew             1.04        1.66        1.64        1.81        2.63
   kurt             0.51        3.54        3.42        4.42        9.34
   mad              0.08        0.15        0.21        0.26        0.46 
 
   In [13]: # monthly portfolios 
            _, _, _, = ff_M.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    _, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
	    _, _, _, = ff_M.comparePortfolios('Characs', ffFreq, startDate, endDate, sortingDim)

   *********************************** BM (5) ************************************
       *********************** Observation frequency: M ************************
    ************************* Returns: 1960-01-31 to 2020-03-31 **************************

   Correlation matrix:
           bm0-20  bm20-40  bm40-60  bm60-80  bm80-100
   corr:   0.997    0.987    0.988     0.96     0.981 

   Average matrix:
                            bm0-20        bm20-40  ...        bm60-80        bm80-100
   [wrds, kflib]:  [0.85%, 0.85%]  [0.9%, 0.91%]  ...  [0.9%, 0.95%]  [1.17%, 1.13%]

   [1 rows x 5 columns] 

   Std Deviation matrix:
                            bm0-20         bm20-40  ...         bm60-80        bm80-100
   [wrds, kflib]:  [4.77%, 4.76%]  [4.43%, 4.45%]  ...  [4.92%, 4.54%]  [5.18%, 5.32%]

   [1 rows x 5 columns] 

   Elapsed time:  5.842  seconds.

   *********************************** BM (5) ************************************
       *********************** Observation frequency: M ************************
    ************************* NumFirms: 1960-01-31 to 2020-03-31 **************************

   Correlation matrix:
           bm0-20  bm20-40  bm40-60  bm60-80  bm80-100
   corr:   0.985     0.96    0.964    0.954     0.983 

   Average matrix:
                        bm0-20     bm20-40     bm40-60     bm60-80    bm80-100
   [wrds, kflib]:  [882, 909]  [605, 629]  [573, 595]  [613, 631]  [825, 823] 

   Std Deviation matrix:
                        bm0-20     bm20-40     bm40-60     bm60-80    bm80-100
   [wrds, kflib]:  [451, 415]  [248, 215]  [236, 202]  [267, 229]  [405, 356] 

   Elapsed time:  6.303  seconds.

   *********************************** BM (5) ************************************
       *********************** Observation frequency: M ************************
    ************************* (Characteristic: ME): 1960-01-31 to 2020-03-31 ***************************

   Correlation matrix:
           bm0-20  bm20-40  bm40-60  bm60-80  bm80-100
   corr:   0.921    0.902    0.973     0.93      0.98 

   Average matrix:
                                bm0-20  ...          bm80-100
   [wrds, kflib]:  [3855.98, 3327.93]  ...  [620.67, 646.14]

   [1 rows x 5 columns] 

   Std Deviation matrix:
                                bm0-20  ...          bm80-100
   [wrds, kflib]:  [6213.33, 4267.12]  ...  [833.82, 858.66]
   
   [1 rows x 5 columns] 


   *********************************** BM (5) ************************************
       *********************** Observation frequency: M ************************
      ************************** (Characteristic: BM) ***************************
      ******************************* NOT AVAILABLE *****************************

   Elapsed time:  4.758  seconds.

**(10 x 1) Sorts**:

.. code-block:: ipython

   In [11]: sortingDim = [10]      
   In [12]: # Summary statistics
	    ff_M.getFamaFrenchStats('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
            ff_M.getFamaFrenchStats('Characs', ffFreq, startDate, endDate, sortingDim)

   *********************************** Summary Statistics: Portfolio Returns ***********************************
             *********************************** BM (10) ************************************

       *********************** Observation frequency: M ************************
                  bm0-10     bm10-20  ...     bm80-90    bm90-100
   startdate  1960-01-31  1960-01-31  ...  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  ...  2020-03-31  2020-03-31
   count             723         723  ...         723         723
   mean            0.01%       0.01%  ...       0.01%       0.01%
   std             0.05%       0.05%  ...       0.05%       0.06%
   min            -0.23%      -0.25%  ...      -0.21%      -0.23%
   1%             -0.12%      -0.12%  ...      -0.13%      -0.16%
   10%            -0.05%      -0.05%  ...      -0.05%      -0.06%
   25%            -0.02%      -0.02%  ...      -0.02%      -0.02%
   50%             0.01%       0.01%  ...       0.02%       0.01%
   75%             0.04%       0.04%  ...       0.04%       0.05%
   90%             0.07%       0.06%  ...       0.07%       0.08%
   99%             0.13%       0.11%  ...       0.12%       0.16%
   max             0.23%       0.19%  ...       0.22%       0.31%
   skew           -0.28%      -0.46%  ...      -0.38%      -0.23%
   kurt            1.48%       1.74%  ...       1.95%       2.78%
   mad             0.04%       0.04%  ...       0.04%       0.04%

   [17 rows x 10 columns] 

   *********************************** Summary Statistics: Number of Firms ***********************************
             *********************************** BM (10) ************************************
   
       *********************** Observation frequency: M ************************
                  bm0-10     bm10-20  ...     bm80-90    bm90-100
   startdate  1960-01-31  1960-01-31  ...  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  ...  2020-03-31  2020-03-31
   count             723         723  ...         723         723
   mean              531         352  ...         370         455
   std               312         153  ...         185         232
   min                 5          14  ...           8           8
   1%                  5          14  ...           8           8
   10%               102          94  ...         101         130
   25%               288         264  ...         258         258
   50%               453         367  ...         389         476
   75%               828         471  ...         452         590
   90%               971         543  ...         640         708
   99%              1144         601  ...         811         994
   max              1207         620  ...         894        1026
   skew                0          -1  ...           0           0
   kurt               -1          -0  ...          -0          -0
   mad               267         121  ...         141         179

   [17 rows x 10 columns] 
   
   *********************************** Summary Statistics: Firm Characteristics ***********************************
            *********************************** BM (10) ************************************
 
        ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: M ************************
   bm_port        bm0-10     bm10-20  ...     bm80-90    bm90-100
   startdate  1960-01-31  1960-01-31  ...  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  ...  2020-03-31  2020-03-31
   count             723         723  ...         723         723
   mean          4050.37     3686.25  ...      810.33      456.76
   std           6673.92     5936.58  ...        1041      662.57
   min            144.07       159.2  ...       29.55       15.44
   1%             165.33      214.86  ...        32.5       17.99
   10%            337.28      357.23  ...       91.34       49.76
   25%            574.41      480.23  ...      148.69       91.39
   50%           1176.26      860.43  ...         407      156.49
   75%           6170.38     5674.13  ...      829.81      372.95
   90%           8595.05     9212.61  ...     2380.14     1765.69
   99%           46014.7     39383.5  ...     4395.87      2628.7
   max           50793.7     47053.5  ...      4870.1     2885.31
   skew             4.23        4.06  ...        1.92        1.93
   kurt            23.55        22.6  ...        2.96        2.49
   mad           4117.79     3790.67  ...      757.45      487.52

   [17 rows x 10 columns] 

      ************************** (Characteristic: BM) ***************************
       *********************** Observation frequency: M ************************
   bm_port        bm0-10     bm10-20  ...     bm80-90    bm90-100
   startdate  1960-01-31  1960-01-31  ...  1960-01-31  1960-01-31
   enddate    2020-03-31  2020-03-31  ...  2020-03-31  2020-03-31
   count             723         723  ...         723         723
   mean             0.18        0.33  ...        1.26        2.02
   std              0.08        0.13  ...        0.48        0.97
   min              0.01        0.09  ...        0.71           1
   1%               0.01        0.09  ...        0.72        1.01
   10%              0.09         0.2  ...        0.82         1.2
   25%              0.12        0.23  ...        0.93        1.39
   50%              0.15        0.29  ...        1.18         1.8
   75%              0.21        0.39  ...         1.4        2.28
   90%              0.31        0.53  ...        1.81        2.81
   99%              0.39         0.8  ...        3.56        7.23
   max              0.39         0.8  ...        3.57        7.79
   skew              0.9        1.22  ...        2.18        3.02
   kurt             0.26        1.49  ...        7.28       12.48
   mad              0.06         0.1  ...        0.33        0.62

   [17 rows x 10 columns] 
   
   In [13]: # monthly portfolios 
            _, _, _, = ff_M.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
	    _, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
	    _, _, _, = ff_M.comparePortfolios('Characs', ffFreq, startDate, endDate, sortingDim)

   *********************************** BM (10) ************************************
       *********************** Observation frequency: M ************************
    ************************* Returns: 1960-01-31 to 2020-03-31 **************************

   Correlation matrix:
           bm0-10  bm10-20  bm20-30  bm30-40  ...  bm60-70  bm70-80  bm80-90  bm90-100
   corr:   0.993    0.987     0.98    0.966  ...     0.93    0.958    0.972     0.966

   [1 rows x 10 columns] 

   Average matrix:
                            bm0-10         bm10-20  ...         bm80-90       bm90-100
   [wrds, kflib]:  [0.78%, 0.81%]  [0.95%, 0.93%]  ...  [1.17%, 1.13%]  [1.2%, 1.14%]

   [1 rows x 10 columns] 

   Std Deviation matrix:
                            bm0-10         bm10-20  ...         bm80-90        bm90-100
   [wrds, kflib]:  [5.02%, 5.02%]  [4.66%, 4.61%]  ...  [4.99%, 5.03%]  [5.91%, 6.19%]

   [1 rows x 10 columns] 

   Elapsed time:  6.544  seconds.

   *********************************** BM (10) ************************************
       *********************** Observation frequency: M ************************
    ************************* NumFirms: 1960-01-31 to 2020-03-31 **************************

   Correlation matrix:
           bm0-10  bm10-20  bm20-30  bm30-40  ...  bm60-70  bm70-80  bm80-90  bm90-100
   corr:   0.991    0.965    0.959    0.953  ...    0.943    0.953    0.977     0.984

   [1 rows x 10 columns] 

   Average matrix:
                        bm0-10     bm10-20  ...     bm80-90    bm90-100
   [wrds, kflib]:  [531, 546]  [352, 364]  ...  [370, 372]  [455, 451]

   [1 rows x 10 columns] 

   Std Deviation matrix:
                        bm0-10     bm10-20  ...     bm80-90    bm90-100
   [wrds, kflib]:  [312, 290]  [153, 139]  ...  [185, 162]  [232, 206]

   [1 rows x 10 columns] 

   Elapsed time:  6.593  seconds.

   *********************************** BM (10) ************************************
       *********************** Observation frequency: M ************************
    ************************* (Characteristic: ME): 1960-01-31 to 2020-03-31 ***************************

   Correlation matrix:
           bm0-10  bm10-20  bm20-30  bm30-40  ...  bm60-70  bm70-80  bm80-90  bm90-100
   corr:   0.939    0.882    0.963    0.517  ...    0.876    0.958    0.974     0.985

   [1 rows x 10 columns] 

   Average matrix:
                                bm0-10  ...          bm90-100
   [wrds, kflib]:  [4050.37, 3458.62]  ...  [456.76, 467.89]

   [1 rows x 10 columns] 

   Std Deviation matrix:
                                bm0-10  ...          bm90-100
   [wrds, kflib]:  [6673.92, 4568.71]  ...  [662.57, 663.93]

   [1 rows x 10 columns] 


   *********************************** BM (10) ************************************
       *********************** Observation frequency: M ************************
      ************************** (Characteristic: BM) ***************************
      ******************************* NOT AVAILABLE *****************************

   Elapsed time:  4.746  seconds.

Portfolios Sorted on `Book-to-Market` ``BM`` : Annual
*******************************************************


**(3 x 1) Sorts**:

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_unisorts_me_bm_op_inv.py>`_.


**(5 x 1) Sorts**:

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_unisorts_me_bm_op_inv.py>`_.


**(10 x 1) Sorts**:

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_unisorts_me_bm_op_inv.py>`_.


Portfolios Sorted on `Operating Profitability` ``OP``
######################################################


Portfolios Sorted on `Operating Profitability` ``OP`` : Monthly
***************************************************************


**(3 x 1) Sorts**:

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_unisorts_me_bm_op_inv.py>`_.


**(5 x 1) Sorts**:

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_unisorts_me_bm_op_inv.py>`_.


**(10 x 1) Sorts**:

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_unisorts_me_bm_op_inv.py>`_.


Portfolios Sorted on `Operating Profitability` ``OP`` : Annual
***************************************************************


**(3 x 1) Sorts**:

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_unisorts_me_bm_op_inv.py>`_.


**(5 x 1) Sorts**:

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_unisorts_me_bm_op_inv.py>`_.


**(10 x 1) Sorts**:

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_unisorts_me_bm_op_inv.py>`_.




Portfolios Sorted on `Investment` ``INV``
##########################################



Portfolios Sorted on `Investment` ``INV`` : Monthly
****************************************************


**(3 x 1) Sorts**:

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_unisorts_me_bm_op_inv.py>`_.


**(5 x 1) Sorts**:

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_unisorts_me_bm_op_inv.py>`_. 


**(10 x 1) Sorts**:

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_unisorts_me_bm_op_inv.py>`_.


Portfolios Sorted on `Investment` ``INV`` : Annual
***************************************************


**(3 x 1) Sorts**:

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_unisorts_me_bm_op_inv.py>`_.


**(5 x 1) Sorts**:

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_unisorts_me_bm_op_inv.py>`_.


**(10 x 1) Sorts**:

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_unisorts_me_bm_op_inv.py>`_.


Portfolios Sorted on `Size` ``ME`` & `Book-to-Market` ``BM``
############################################################

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_bisorts_me_bm_op_inv.py>`_.


Portfolios Sorted on `Size` ``ME`` & `Operating Profitability` ``OP``
######################################################################

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_bisorts_me_bm_op_inv.py>`_.


Portfolios Sorted on `Size` ``ME`` & `Investment` ``INV``
######################################################################

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_bisorts_me_bm_op_inv.py>`_.


Portfolios Sorted on `Book-to-Market` ``BM`` & `Operating Profitability` ``OP``
################################################################################

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_bisorts_me_bm_op_inv.py>`_.


Portfolios Sorted on `Book-to-Market` ``BM`` & `Investment` ``INV``
################################################################################

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_bisorts_me_bm_op_inv.py>`_.


Portfolios Sorted on `Operating Profitability` ``OP`` & `Investment` ``INV``
################################################################################

See example code `here <https://github.com/christianjauregui/famafrench/blob/master/examples/famafrench_bisorts_me_bm_op_inv.py>`_.



    
