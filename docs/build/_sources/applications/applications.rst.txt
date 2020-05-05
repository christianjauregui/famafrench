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
   mean           109.49      962.72       11721
   std            125.17     1033.02     13199.2
   min             11.81       94.91     1055.29
   1%              12.01       95.48     1055.29
   10%             17.97      133.13     1346.66
   25%             24.82      169.23      1479.8
   50%             44.27      516.41     5220.45
   75%            155.63     1389.35     19406.4
   90%            291.69     2547.87     29253.8
   99%            604.84     4468.11     61026.1
   max            611.05     4468.11     61026.1
   skew             1.74        1.41        1.41
   kurt             2.94        1.28        1.65
   mad             97.43      822.21     10914.7 


        
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
   mean            75.43      396.92      946.17     2312.84     16460.9
   std             84.34      427.92     1034.47     2485.36     18377.4
   min              9.12       38.02       87.82      231.03     1425.96
   1%               9.24        38.1       87.98      231.78     1425.96
   10%             13.15       52.92       119.5      306.94     1806.28
   25%             18.72       73.36      158.25      374.18      2039.4
   50%             30.39      187.26      517.02     1402.77      7104.9
   75%            102.17      556.75     1367.59     3159.59     28339.4
   90%            205.66     1079.52     2459.49     5792.54     40627.3
   99%             407.3     1783.61     4971.89       11719     80726.9
   max            413.51        1790     4971.89       11719     80726.9
   skew             1.71        1.31        1.55        1.53        1.31
   kurt             2.83        0.79        2.17         2.1        1.17
   mad              66.1      348.14      813.84     1951.76     15408.9 

        
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
             *********************************** ME (5) ************************************
 
      *********************** Observation frequency: D ************************
                  me0-20     me20-40     me40-60     me60-80    me80-100
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
             *********************************** ME (5) ************************************

       *********************** Observation frequency: D ************************
                  me0-20     me20-40     me40-60     me60-80    me80-100
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
             *********************************** ME (5) ************************************

      ************************** (Characteristic: ME) ***************************
       *********************** Observation frequency: D ************************
   me_port        me0-10     me10-20  ...     me80-90    me90-100
   startdate  1960-01-04  1960-01-04  ...  1960-01-04  1960-01-04
   enddate    2020-03-31  2020-03-31  ...  2020-03-31  2020-03-31
   count           15164       15164  ...       15164       15164
   mean               45      173.99  ...     5759.98     28098.2
   std             48.97      187.92  ...     6423.82     32520.2
   min              6.79       19.78  ...      508.48     2316.85
   1%               6.88       19.81  ...      508.48     2316.85
   10%              9.15       25.65  ...      637.48     2923.61
   25%             11.71       38.82  ...      769.41     3411.24
   50%             20.75       76.61  ...     3171.85     11164.5
   75%             57.75      236.62  ...     8162.41     51194.3
   90%            117.28      470.49  ...     14766.6     68854.2
   99%            224.47      835.42  ...     32120.8      168218
   max            224.47      838.48  ...     32252.6      168218
   skew             1.71         1.4  ...        1.56         1.6
   kurt             2.55        1.23  ...        2.49        3.02
   mad             38.24      152.32  ...      5118.3       26766
   
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
   mean           109.74      963.44     11733.9
   std            125.54     1034.69     13222.2
   min             11.82       94.98     1055.29
   1%              12.03       95.48     1055.29
   10%             18.31      133.29     1346.66
   25%             24.75      169.19     1482.87
   50%             44.31      516.41     5230.05
   75%            155.65      1389.1       19555
   90%            292.46      2548.3     29237.1
   99%            605.29     4468.11     61026.1
   max            611.05     4468.11     61026.1
   skew             1.74        1.41        1.41
   kurt             2.95        1.28        1.65
   mad             97.69      823.31     10934.1 

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
   corr:   0.952    0.977     0.988 

   Average matrix:
                              me0-30           me30-70              me70-100
   [wrds, kflib]:  [109.74, 105.23]  [963.44, 946.07]  [11733.94, 11808.07] 

   Std Deviation matrix:
                              me0-30            me30-70              me70-100
   [wrds, kflib]:  [125.54, 113.05]  [1034.69, 999.73]  [13222.16, 13245.28] 

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
   mean            75.57      397.31      947.03      2314.5     16476.4
   std             84.57      428.93     1036.32     2489.53     18411.1
   min              9.12       38.02       87.92      231.45     1425.96
   1%               9.26        38.1       87.99      231.78     1425.96
   10%             13.17       53.03      119.53      306.94     1806.28
   25%             18.82       73.36      158.25       373.5      2039.4
   50%             30.38      187.31      517.02     1402.77      7104.9
   75%            102.18      556.74     1367.48      3158.4       28437
   90%            205.87     1085.51     2472.34     5798.12     40609.4
   99%            407.46      1783.4     4971.89       11719     80726.9
   max            413.35     1787.57     4971.89       11719     80726.9
   skew             1.72        1.31        1.55        1.53        1.31
   kurt             2.85        0.79        2.16        2.11        1.17
   mad             66.24      348.75      814.97     1954.89     15433.2 
   
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
   corr:   0.939    0.976    0.964    0.975      0.99 

   Average matrix:
                            me0-20  ...              me80-100
   [wrds, kflib]:  [75.57, 72.27]  ...  [16476.36, 16670.08]

   [1 rows x 5 columns] 

   Std Deviation matrix:
                            me0-20  ...             me80-100
   [wrds, kflib]:  [84.57, 74.75]  ...  [18411.1, 18704.98]

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
   enddate    2020-03-31  2020-03-31  ...  2020-03-31  2020-03-31
   count             723         723  ...         723         723
   mean            45.11      174.18  ...     5764.16     28129.3
   std             49.09      188.34  ...     6432.76     32572.8
   min              6.79       19.79  ...      508.48     2316.85
   1%               6.89       19.81  ...      508.48     2316.85
   10%              9.15       25.71  ...      637.48     2923.61
   25%             11.72       38.83  ...      769.41     3411.24
   50%             20.75       76.77  ...     3171.85     11113.3
   75%             58.25      237.91  ...     8199.71     51358.8
   90%            117.66      472.05  ...     14765.4     68854.2
   99%            224.47      835.08  ...     32120.8      168218
   max            224.47      838.48  ...     32120.8      168218
   skew             1.71        1.41  ...        1.56        1.59
   kurt             2.55        1.23  ...        2.49        3.01
   mad             38.34      152.62  ...     5127.09     26816.3

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
   corr:   0.915    0.961    0.975    0.981  ...     0.98    0.976    0.975      0.98

   [1 rows x 10 columns] 

   Average matrix:
                            me0-10  ...             me90-100
   [wrds, kflib]:  [45.11, 43.31]  ...  [28129.3, 28203.72]

   [1 rows x 10 columns] 

   Std Deviation matrix:
                            me0-10  ...              me90-100
   [wrds, kflib]:  [49.09, 43.18]  ...  [32572.79, 31739.34]

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
   mean           108.52      969.21     11824.4
   std            122.37     1022.79     13207.3
   min             11.78       93.18     1073.21
   1%              12.65      103.58     1092.16
   10%             18.17      128.49     1370.16
   25%             24.63      173.39     1483.79
   50%             43.86      521.55     5431.03
   75%            160.58     1451.19     19347.1
   90%            292.54     2550.73       29576
   99%            452.52     3779.06     50564.1
   max            591.43     3937.65       54121
   skew              1.7        1.28        1.32
   kurt             2.97        0.68        1.17
   mad             95.67      821.98       10941 
   
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
   mean            74.68      394.69      938.54     2309.55     16624.2
   std             82.16      417.48      981.57     2401.37     18446.8
   min              9.07       37.69       86.82      228.74     1465.53
   1%               9.76       42.65       97.23      241.52     1479.96
   10%             13.09       51.87      114.85      304.91     1910.27
   25%             18.78       74.69      163.09      375.84     2034.97
   50%             30.82      187.62      514.68     1393.15      7501.1
   75%            107.25      595.69     1437.92     3346.46     28140.7
   90%             203.5     1029.44     2475.13      5824.2     41044.6
   99%            301.65     1461.11     3480.54     9022.39     69709.9
   max             396.9     1745.95     3838.29     9542.63     72980.1
   skew             1.66        1.25        1.22        1.28        1.25
   kurt             2.79        0.69        0.48        0.81        0.86
   mad             64.76      341.51      796.06     1928.27     15466.1 
   
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
   mean            43.54      173.34  ...     5832.81       28410
   std             44.96      184.27  ...     6428.45     32491.6
   min              6.75        19.6  ...      511.83     2412.97
   1%               7.03       22.04  ...      520.27     2430.66
   10%              9.09       26.73  ...      661.77     3091.47
   25%             12.98       38.82  ...       758.4     3375.32
   50%             20.32       80.13  ...     3194.29     11996.7
   75%             61.88      256.33  ...     8525.23     51014.8
   90%            112.06      463.59  ...     14915.7     69685.3
   99%            167.99      664.54  ...     24602.6      125696
   max            203.33      812.66  ...     28221.9      147577
   skew             1.49        1.38  ...        1.42        1.44
   kurt             1.63        1.27  ...        1.65        2.04
   mad             36.02      149.53  ...     5156.85     26891.2

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
   mean          3357.98     1925.38      755.04
   std           4607.99     2914.14     1059.21
   min            232.23       139.9       35.29
   1%             239.48      141.94       35.74
   10%            362.06      254.03       95.73
   25%            485.63      357.86      129.79
   50%            875.39      721.93      340.61
   75%           5570.12     2504.16      761.46
   90%           8235.88     5879.31     2133.89
   99%           27233.1     20797.4     5655.08
   max           27233.1     20797.4     5871.15
   skew             2.54        3.81        2.55
   kurt             8.58       20.01        7.29
   mad           3418.78     1862.71      738.95 

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
   corr:   0.972    0.839     0.958 

   Average matrix:
                                bm0-30             bm30-70          bm70-100
   [wrds, kflib]:  [3357.98, 3229.51]  [1925.38, 1751.94]  [755.04, 821.77] 

   Std Deviation matrix:
                                bm0-30             bm30-70            bm70-100

   [wrds, kflib]:  [4607.99, 4140.62]  [2914.14, 2117.63]  [1059.21, 1080.39] 

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
   mean          3626.21      2787.7     1752.49     1198.38      591.82
   std           5488.56     4344.54     2118.65     1495.99      806.72
   min            209.09      177.45       151.3       69.07       26.42
   1%             217.13      180.49      153.31       70.25       26.62
   10%            362.25      263.73      252.98       167.5       76.47
   25%             545.7      370.25      336.17      283.42      100.59
   50%            960.68      926.35      694.79      601.96      239.61
   75%           5987.77     3964.81      2025.6     1434.54      493.21
   90%           7737.39     8650.54     5282.06     3438.31     1961.49
   99%           37614.7     30047.6     8086.98     8314.74      3436.1
   max           37614.7     30047.6     8086.98     8495.83     3588.63
   skew             3.55        3.55        1.63        2.43        1.96
   kurt            17.29       17.49        1.61        7.28           3
   mad           3711.38     2823.34     1622.76     1074.17      595.09 

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
   corr:   0.938    0.881    0.972    0.917     0.964 

   Average matrix:
                                bm0-20  ...          bm80-100
   [wrds, kflib]:  [3626.21, 3327.93]  ...  [591.82, 646.14]

   [1 rows x 5 columns] 

   Std Deviation matrix:
                                bm0-20  ...          bm80-100
   [wrds, kflib]:  [5488.56, 4267.12]  ...  [806.72, 858.66]

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
   mean          3942.11     3416.34  ...      779.33      430.86
   std           6757.87     4997.43  ...     1013.54      632.74
   min            147.22       206.8  ...       34.08       19.55
   1%             153.34       206.8  ...       34.36       20.11
   10%            347.06      351.09  ...       92.15       64.29
   25%            577.17       501.3  ...      136.44       83.06
   50%           1098.18      838.65  ...      399.63      137.04
   75%           5785.37     5648.94  ...      734.67      355.81
   90%           8788.02     8710.24  ...     2427.99     1578.89
   99%           51165.5     32775.2  ...     4520.31     2412.05
   max           51165.5     32775.2  ...     4664.76     2498.37
   skew             4.66        3.14  ...        1.94        1.92
   kurt            28.07       13.74  ...        3.09        2.36
   mad           4032.13     3506.67  ...      735.64      462.68

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
   corr:   0.916     0.92    0.962    0.478  ...    0.877    0.942    0.963     0.964

   [1 rows x 10 columns] 

   Average matrix:
                                bm0-10  ...          bm90-100
   [wrds, kflib]:  [3942.11, 3458.62]  ...  [430.86, 467.89]

   [1 rows x 10 columns] 

   Std Deviation matrix:
                               bm0-10  ...          bm90-100
   [wrds, kflib]:  [6757.87, 4568.71]  ...  [632.74, 663.93]

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



    
