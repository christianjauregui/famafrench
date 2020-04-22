.. _gettingstarted:

****************
Getting Started
****************

Overview
#########

The main tool provided by the package is the ``FamaFrench`` class that enables its user to construct 
a multitude of datasets found in `Ken French's online library <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>`_ as well as many others. 

Datasets include portfolio returns (`value`- or `equal`-weighted), number of firms in each portfolio, or `average` anomaly portfolio characteristics. The sample dataset will be for a pre-specified frequency and range of dates characterized by a start and end date. 

In addition, and of most interest to the average user, the ``FamaFrench`` class enables a user to construct some of the most studied Fama-French-style factors: 
	
	* Market Premium (``MKT-RF``)
	* Small Minus Big (``SMB``)
	* High Minus Low (``HML``)
	* Momentum based on Prior (2-12) returns (``MOM``)
	* Short-Term Reversal based on Prior (1-1) returns (``ST_Rev``)
	* Long-Term Reversal based on Prior (13-60) returns (``LT_Rev``)

In almost all applications, the package requires the use of the constructor function :class:`FamaFrench`:

.. module:: famafrench
   :noindex:

.. currentmodule:: famafrench

.. autosummary::
  :nosignatures:
  :toctree: generated/

     FamaFrench

The constructor function makes use of an altered set of routines borrowed from the `WRDS-Py library <https://github.com/wharton/wrds>`_ to query `CRSP <http://www.crsp.org/products/research-products/crsp-us-stock-databases>`_, `Compustat Fundamentals Annual <https://wrds-web.wharton.upenn.edu/wrds/support/Data/_001Manuals%20and%20Overviews/_001Compustat/_001North%20America%20-%20Global%20-%20Bank/_000dataguide/index.cfm0>`_, and other datafiles provided by `Wharton Research Data Services` `(WRDS) <https://wrds-web.wharton.upenn.edu/wrds/support/>`_. To use the ``famafrench`` package, a user **must** have a subscription to both CRSP and Compustat Fundamentals Annual through WRDS. See :ref:`wrdsconnection/wrdsconnection:Connecting to ``wrds-cloud```.

Alterations of routines borrowed from the `WRDS-Py library <https://github.com/wharton/wrds>`_ enable a user with access to WRDS to add his/her WRDS username and password to their local environment. This is achieved through the use of environment variables via :func:`os.environ`, a mapping object in Python's :mod:`os` module that represents the user’s environment variables. Environment variables provide secure means of storing usernames and passwords. Use of and modifications to the `WRDS-Py library <https://github.com/wharton/wrds>`_ abide by its permissive MIT license (see `LICENSE <https://github.com/christianjauregui/famafrench/blob/master/LICENSE>`_).

.. note::

   To securely set up the WRDS username and password as environment variables:

   1. If it does not exist already, create an ``.env`` file in your home directory. This should be the same directory where ``~/.bash_profile`` is stored. 
   2. Open ``~/.bash_profile`` and add the following: ``source ~/.env``. In ``.env``, you add your WRDS username and password as environment variables as follows:     
   
   .. code-block:: bash
   
      export WRDS_USERNAME="FILL IN"
      export WRDS_PASSWORD="FILL IN"
   
   2. This can also be done directly in Python:  
   
   .. code-block:: ipython
      
      import os
      os.environ["WRDS_USERNAME"] = "FILL IN"
      os.environ["WRDS_PASSWORD"] = "FILL IN"


Having set up the WRDS username and password, connecting remotely to WRDS through `wrds-cloud` is made
simple through the constructor :class:`wrdsConnection<wrdsconnect.wrdsConnection>`. This constructor is repeatedly used within the main package constructor :class:`FamaFrench<FamaFrench>`.

    

Creating an Instance of the ``FamaFrench`` Class
################################################

Instances of the :class:`FamaFrench<FamaFrench>` object will vary depending on whether the user wants to construct Fama-French-style factors **or** portfolio returns (`value`- or `equal`-weighted), number of firms in each portfolio, and `average` anomaly portfolio characteristics. 

For both types of instances, the frequency of portfolios :attr:`freqType` as well as the starting and ending dates must be specified. Both starting and ending dates must be in :class:`datetime.date` format. In addition, attribute :attr:`runQuery` is set to ``True`` or ``False`` depending on whether the user prefers to query all datafiles from `wrds-cloud` from scratch or whether previously queried and locally-saved datafiles are pickled in constructing the instance. The latter choice is particularly useful when updating data following a new set of observation points released by WRDS. Making use of previously queried and locally-saved datafiles significantly speeds up run-time and execution of code. 


For example, to construct the **Fama-French 3 factors**: the `Market Premium` ``MKT-RF``, `Small Minus Big` ``SMB``, and `High Minus Low` ``HML``, at the monthly frequency (from 1970 to the present, or the most recent date for which there is stock returns data available in CRPS), we execute the following lines of Python code:

**Fama-French 3 Factors:**

.. code-block:: ipython
    
   In [1]: import datetime as dt
   In [2]: import famafrench.famafrench as ff
   
   In [3]: startDate = dt.date(1970, 1, 1)
   In [4]: endDate = dt.date.today()
   In [5]: runQuery = True
   In [6]: ffFreq = 'M'
   In [7]: ffsortCharac = ['ME', 'BM']
   In [8]: ffFactors = ['MKT-RF', 'SMB', 'HML']
   In [9]: ff3 = ff.FamaFrench(runQuery=runQuery, freqType=ffFreq, sortCharacsId=ffsortCharac, factorsId=ffFactors) 

   In [10]: factorsTableM = ff3.getFFfactors(dt_start=startDate, dt_end=endDate)
   
   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [00:03<00:00,  1.73s/it]
   Historical risk-free interest rate (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   
   In [11]: factorsTableM.head()
   Out[11]: 
                    mkt    mkt-rf       smb       hml
   date                                              
   1970-01-31 -0.074878 -0.080878  0.031418  0.027965
   1970-02-28  0.057439  0.051239 -0.025979  0.040931
   1970-03-31 -0.004881 -0.010581 -0.018887  0.041828
   1970-04-30 -0.104866 -0.109866 -0.058987  0.064264
   1970-05-31 -0.063964 -0.069264 -0.046954  0.034585
 

- To construct Fama-French-style factors, :attr:`factorsId` must be passed as a list of strings with the names of the factors (per the naming convention outlined in the documentation for :class:`FamaFrench<FamaFrench>`). 
- Although one can pass the anomaly portfolio characteristics used for portfolio sorting in the construction of the factors, :attr:`sortCharacsId`, the constructor does not require this. Here, :attr:`mainCharacsId` is also not required for obvious reasons (when omitted, :attr:`mainCharacsId` is set to :attr:`sortCharacsId` by default).

We can compare the constructed factors to those provided by `Ken French <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html>`_: 


.. code-block:: ipython
    
   In [12]: kffactorsTableM = ff3.getkfFFfactors(freq=ffFreq, dt_start=startDate, dt_end=endDate)
   In [13]: kffactorsTableM.head()
   Out[13]: 
                  mkt  mkt-rf     smb     hml
   1970-01-31 -0.0750 -0.0810  0.0290  0.0304
   1970-02-28  0.0575  0.0513 -0.0240  0.0404
   1970-03-31 -0.0049 -0.0106 -0.0232  0.0425
   1970-04-30 -0.1050 -0.1100 -0.0611  0.0639
   1970-05-31 -0.0639 -0.0692 -0.0452  0.0360

   In [14]: _, _, _, = ff3.comparePortfolios(kfType='Factors', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate)
   
   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [00:03<00:00,  1.78s/it]
   Historical risk-free interest rate (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   *********************************** Factor Returns: 1970-01-31 to 2020-02-29 ***********************************
       
      *********************** Observation frequency: M ************************
   Fama-French factors: Correlation matrix:
           mkt  mkt-rf    smb    hml
   corr:  1.0     1.0  0.991  0.984 
   
   Fama-French factors: Average matrix:
                             mkt        mkt-rf           smb         hml
   [wrds, kflib]:  [0.93, 0.93]  [0.55, 0.55]  [0.13, 0.12]  [0.3, 0.3] 
   
   Fama-French factors: Std Deviation matrix:
                           mkt        mkt-rf           smb           hml
   [wrds, kflib]:  [4.5, 4.5]  [4.51, 4.51]  [3.05, 3.06]  [2.98, 2.92] 
   
   Elapsed time:  68.613  seconds.

 
- The instance method :meth:`comparePortfolios` compares our constructed factors with those provided by French over the same sample period. Current output of the method includes sample `Pearson correlations`, sample `means`, and sample `standard deviations` for the sample period.

**Other examples:** To form the 6 (ie 2 x 3) monthly, portfolios (also from 1970 to the present, or the most recent date for which there is stock returns data available in CRPS) sorted on `Size` ``ME`` and `Book-to-Market` ``BM`` and construct the `value`-weighted portfolio returns, number of firms in each portfolio, and the `average` anomaly portfolio characteristics used in the construction of the portfolios: market value of equity ``ME`` and book-to-market equity ``BM``, we execute the following lines of Python code:

`Value` **-weighted portfolio returns:**
 
.. code-block:: ipython
    
   In [1]: import datetime as dt
   In [2]: import famafrench.famafrench as ff
   
   In [3]: startDate = dt.date(1970, 1, 1)
   In [4]: endDate = dt.date.today()
   In [5]: runQuery = True
   In [6]: ffFreq = 'M'
   In [7]: sortingDim = [2, 3]
   In [8]: retType = 'vw'

   In [9]: ffsortCharac = ['ME', 'BM']
   In [10]: ffFactors = []
   In [11]: me_bm_2x3 = ff.FamaFrench(runQuery=runQuery, freqType=ffFreq, sortCharacsId=ffsortCharac, factorsId=ffFactors) 

   In [12]: returnsTableM = me_bm_2x3.getPortfolioReturns(factorsBool=False, dt_start=startDate, dt_end=endDate, pDim=sortingDim, pRetType=retType)  
   
   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   
   In [13]: returnsTableM.head()
   Out [13]: 
               me0-50_bm0-30  me0-50_bm30-70  ...  me50-100_bm30-70  me50-100_bm70-100
   date                                       ...                                     
   1970-01-31      -0.075423       -0.066817  ...         -0.072045          -0.079993
   1970-02-28       0.035483        0.030274  ...          0.071287           0.076770
   1970-03-31      -0.049978        0.000497  ...          0.016178           0.011756
   1970-04-30      -0.200480       -0.140580  ...         -0.087627          -0.074118
   1970-05-31      -0.110463       -0.101711  ...         -0.059225          -0.022641
   
   In [14]: kfreturnsTableM = me_bm_2x3.getkfPortfolioReturns(freq=ffFreq, dt_start=startDate, dt_end=endDate, dim=sortingDim, retType=retType) 
   In [15]: kfreturnsTableM.head()
   Out [15]:
               small lobm   me1 bm2  small hibm  big lobm   me2 bm2  big hibm
   1970-01-31   -0.060745 -0.051124   -0.023747 -0.080621 -0.085096 -0.056797
   1970-02-28    0.025803  0.035260    0.061994  0.036058  0.078464  0.080637
   1970-03-31   -0.053084 -0.011075    0.001495 -0.019099  0.014691  0.011248
   1970-04-30   -0.208565 -0.139240   -0.111768 -0.105894 -0.095480 -0.074793
   1970-05-31   -0.114140 -0.105260   -0.079967 -0.079879 -0.041648 -0.042096
   
   In [16]:  _, _, _, = me_bm_2x3.comparePortfolios(kfType='Returns', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim, kfRetType=retType) 
   
   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** ME x BM (2 x 3) ************************************
       *********************** Observation frequency: M ************************
       ************************* Returns: 1970-01-31 to 2020-02-29 **************************
   
   Correlation matrix:
             bm0-30 bm30-70 bm70-100
   me0-50    0.992   0.996    0.993
   me50-100  0.998   0.993    0.991 
   
   Average matrix:
                      bm0-30         bm30-70        bm70-100
   me0-50    [0.82%, 0.83%]  [1.17%, 1.19%]   [1.3%, 1.29%]
   me50-100  [0.92%, 0.93%]  [0.98%, 0.95%]  [1.06%, 1.07%] 
   
   Std Deviation matrix:
                      bm0-30         bm30-70        bm70-100
   me0-50    [6.84%, 6.82%]  [5.45%, 5.42%]  [5.66%, 5.61%]
   me50-100  [4.65%, 4.67%]  [4.36%, 4.38%]  [5.02%, 4.93%] 
   
   Elapsed time:  66.627  seconds. 



**Number of firms in each portfolio:**

.. code-block:: ipython
    
   In [16]: firmsTableM = me_bm_2x3.getNumFirms(factorsBool=False, dt_start=startDate, dt_end=endDate, pDim=sortingDim)  
   In [17]: firmsTableM.head()
   Out [17]: 
               me0-50_bm0-30  me0-50_bm30-70  ...  me50-100_bm30-70  me50-100_bm70-100
   date                                       ...                                     
   1970-01-31            396             499  ...                90                121
   1970-02-28            395             499  ...                90                121
   1970-03-31            396             499  ...                90                121
   1970-04-30            396             499  ...                90                121
   1970-05-31            394             499  ...                90                121
   
   In [18]: kffirmsTableM = me_bm_2x3.getkfNumFirms(freq=ffFreq, dt_start=startDate, dt_end=endDate, dim=sortingDim) 
   In [19]: kffirmsTableM.head()
   Out [19]:
               small lobm  me1 bm2  small hibm  big lobm  me2 bm2  big hibm
   1970-01-31         475      400         297       211      246       143
   1970-02-28         475      399         297       211      246       143
   1970-03-31         474      399         297       211      246       141
   1970-04-30         472      397         296       211      246       141
   1970-05-31         470      395         296       211      246       141
   
   In [20]:  _, _, _, = me_bm_2x3.comparePortfolios(kfType='NumFirms', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim) 
   
   *********************************** ME x BM (2 x 3) ************************************
       *********************** Observation frequency: M ************************
       ************************* NumFirms: 1970-01-31 to 2020-02-29 **************************
   
   Correlation matrix:
             bm0-30 bm30-70 bm70-100
   me0-50    0.986   0.933    0.965
   me50-100  0.876    0.76    0.892 

   Average matrix:
                   bm0-30       bm30-70      bm70-100
   me0-50    [995, 1011]  [1012, 1024]  [1178, 1153]
   me50-100   [373, 381]    [308, 316]    [138, 144] 

   Std Deviation matrix:
                  bm0-30     bm30-70    bm70-100
   me0-50    [427, 407]  [286, 261]  [420, 369]
   me50-100   [102, 87]    [58, 41]    [33, 28] 

   Elapsed time:  4.93  seconds.


`Equal` **-weighted average firm size** ``ME`` **and** `Value` **-weighted average** ``BM`` **for each portfolio:**

.. code-block:: ipython
    
   In [16]: characsTableM = me_bm_2x3.getCharacs(factorsBool=False, dt_start=startDate, dt_end=endDate, pDim=sortingDim)  
   In [17]: for charac in set(list(me_bm_2x3.mainCharacsId)):
		print(charac, '\n', characsTableM[charac].head())
   
   ME

   me_bm_port  me0-50_bm0-30  me0-50_bm30-70  ...  me50-100_bm30-70  me50-100_bm70-100
   date                                       ...                                     
   1970-01-31      80.534648         88.4552  ...       1514.275631        1553.468291
   1970-02-28      80.631874         88.4552  ...       1514.275631        1553.468291
   1970-03-31      80.589856         88.4552  ...       1514.275631        1553.468291
   1970-04-30      80.657533         88.4552  ...       1514.275631        1553.468291
   1970-05-31      80.685602         88.4552  ...       1514.275631        1553.468291

   [5 rows x 6 columns]
   BM

   me_bm_port  me0-50_bm0-30  me0-50_bm30-70  ...  me50-100_bm30-70  me50-100_bm70-100
   date                                       ...                                     
   1970-01-31       0.154248        0.372900  ...          0.369096           0.722310
   1970-02-28       0.154723        0.373592  ...          0.370108           0.723227
   1970-03-31       0.154757        0.374245  ...          0.370769           0.724581
   1970-04-30       0.155672        0.375810  ...          0.370403           0.724732
   1970-05-31       0.154938        0.376080  ...          0.370257           0.723313

   [5 rows x 6 columns]
   
   In [18]: kfcharacsTableM = me_bm_2x3.getkfCharacs(freq=ffFreq, dt_start=startDate, dt_end=endDate, dim=sortingDim) 
   In [19]: for charac in set(list(me_bm_2x3.mainCharacsId)):
		print(charac, '\n', kfcharacsTableM[charac].head())
   ME

               small lobm  me1 bm2  small hibm  big lobm  me2 bm2  big hibm
   1970-01-31       45.73    39.19       41.70   1131.57   706.41    771.55
   1970-02-28       42.91    37.14       40.61   1039.82   645.16    725.75
   1970-03-31       44.04    38.31       42.95   1074.20   691.17    785.33
   1970-04-30       41.71    37.91       43.00   1052.42   699.74    792.46
   1970-05-31       32.85    32.50       38.09    940.38   632.27    731.43
   BM

               small lobm  me1 bm2  small hibm  big lobm  me2 bm2  big hibm
   1970-01-31      0.1952   0.4649      0.9195    0.1900   0.4962    0.8532
   1970-02-28      0.1963   0.4661      0.9226    0.1909   0.4955    0.8570
   1970-03-31      0.1966   0.4662      0.9243    0.1912   0.4949    0.8521
   1970-04-30      0.1979   0.4671      0.9213    0.1922   0.4948    0.8521
   1970-05-31      0.2010   0.4684      0.9222    0.1931   0.4953    0.8512
   
   In [20]:  _, _, _, = me_bm_2x3.comparePortfolios(kfType='NumFirms', kfFreq=ffFreq, dt_start=startDate, dt_end=endDate, kfDim=sortingDim) 
   
   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** ME x BM (2 x 3) ************************************
       *********************** Observation frequency: M ************************
       ************************* (Characteristic: ME): 1970-01-31 to 2020-02-29 ***************************
   
   Correlation matrix:
             bm0-30 bm30-70 bm70-100
   me0-50    0.968   0.972    0.957
   me50-100  0.989   0.966    0.971 
   
   Average matrix:
                            bm0-30             bm30-70           bm70-100
   me0-50        [291.82, 276.32]    [276.92, 266.87]   [160.56, 155.53]
   me50-100  [10156.02, 10422.39]  [7423.11, 7410.82]  [6224.8, 6700.63] 
   
   Std Deviation matrix:
                          bm0-30             bm30-70           bm70-100
   me0-50      [307.14, 277.81]    [281.24, 261.46]   [171.98, 152.91]
   me50-100  [9469.6, 10076.59]  [7741.04, 7357.28]  [6854.91, 7221.4] 
   
   *********************************** ME x BM (2 x 3) ************************************
       *********************** Observation frequency: M ************************
       ************************* (Characteristic: BM): 1970-01-31 to 2020-02-29 ***************************

   Correlation matrix:
             bm0-30 bm30-70 bm70-100
   me0-50    0.996   0.999    0.998
   me50-100  0.996   0.994    0.756 

   Average matrix:
                    bm0-30       bm30-70      bm70-100
   me0-50      [0.3, 0.3]  [0.72, 0.73]  [1.45, 1.48]
   me50-100  [0.29, 0.29]   [0.7, 0.72]   [1.32, 1.3] 

   Std Deviation matrix:
                    bm0-30      bm30-70      bm70-100
   me0-50    [0.14, 0.14]   [0.3, 0.3]  [0.58, 0.58]
   me50-100  [0.13, 0.13]  [0.3, 0.29]  [0.63, 0.49] 

   Elapsed time:  68.136  seconds.


- If attribute :attr:`mainCharacsId` is not specified (as in the example above), then the class constructor sets it to :attr:`sortCharacsId`. 
- Since the focus is on constructing portfolios, not factors, :attr:`factorsId` is set to an empty list. 
- Lastly, :attr:`sortingDim` is set to ``[2, 3]`` and :attr:`retType` is set to ``vw`` in order to form the 6 (ie 2 x 3) portfolios. 

More applications and detailed examples are provided in :ref:`applications/applications:Applications and Examples`.


    
