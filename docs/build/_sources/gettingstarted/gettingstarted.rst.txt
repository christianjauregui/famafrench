.. _gettingstarted:

****************
Getting Started
****************

Overview
#########

The main tool provided by the package is the ``FamaFrench`` class that enables its user to construct 
a multitude of datasets found in `Ken French's online library <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>`_ as well as many others. 

Datasets include portfolio returns (`value`- or `equal`-weighted), number of firms in each portfolio, or `average` anomaly portfolio characteristics. The sample dataset will be for a pre-specified frequency and range of dates characterized by a start and end date. 

In addition, and of utmost interest to most users, the ``FamaFrench`` class enables one to construct some of the most studied Fama-French-style factors: 
	
	* Market Premium (``MKT-RF``)
	* Small Minus Big (``SMB``)
	* High Minus Low (``HML``)
	* Momentum based on Prior (2-12) returns (``MOM``)
	* Short-Term Reversal based on Prior (1-1) returns (``ST_Rev``)
	* Long-Term Reversal based on Prior (13-60) returns (``LT_Rev``)

In almost all applications, the package requires the use of the constructor function :class:`FamaFrench<famafrench.FamaFrench>`:

.. module:: famafrench
   :noindex:

.. currentmodule:: famafrench

.. autosummary::
  :nosignatures:
  :toctree: generated/

     FamaFrench

The constructor function makes use of an altered set of routines borrowed from the `WRDS-Py library <https://github.com/wharton/wrds>`_ to query `CRSP <http://www.crsp.org/products/research-products/crsp-us-stock-databases>`_, `Compustat Fundamentals Annual <https://wrds-web.wharton.upenn.edu/wrds/support/Data/_001Manuals%20and%20Overviews/_001Compustat/_001North%20America%20-%20Global%20-%20Bank/_000dataguide/index.cfm0>`_, and other datafiles provided by `Wharton Research Data Services` `(WRDS) <https://wrds-web.wharton.upenn.edu/wrds/support/>`_. To use the ``famafrench`` package, a user **must** have a subscription to both CRSP and Compustat Fundamentals Annual through WRDS. See :ref:`wrdsconnection/wrdsconnection:Connecting to ``wrds-cloud```.

Alterations of routines borrowed from the `WRDS-Py library <https://github.com/wharton/wrds>`_ enable a user with access to WRDS to add his/her WRDS username and password to their local environment. This is achieved through the use of environment variables via :func:`os.environ`, a mapping object in Python's :mod:`os` module that represents the user’s environment variables. Environment variables provide secure means of storing usernames and passwords. Use of and modifications to the `WRDS-Py library <https://github.com/wharton/wrds>`_ abide by its permissive MIT license (see `LICENSE <https://github.com/christianjauregui/famafrench/blob/master/LICENSE.txt>`_).

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
simple through the constructor :class:`wrdsConnection<wrdsconnect.wrdsConnection>`. This constructor is repeatedly used within the main package constructor :class:`FamaFrench<famafrench.FamaFrench>`.

    

Creating an Instance of the ``FamaFrench`` Class
################################################

Instances of the :class:`FamaFrench<FamaFrench>` object will vary depending on whether the user wants to construct Fama-French-style factors **or** portfolio returns (`value`- or `equal`-weighted), number of firms in each portfolio, and `average` anomaly portfolio characteristics. 

For both types of instances, the frequency of portfolios :attr:`freqType` as well as the starting and end dates must be specified. Both starting and ending dates must be in :class:`datetime.date` format. In addition, attribute :attr:`runQuery` is set to ``True`` or ``False`` depending on whether the user prefers to query all datafiles from `wrds-cloud` from scratch or whether previously queried and locally-saved datafiles are pickled in constructing the instance. The latter choice is particularly useful when updating data following a new set of observation points released by WRDS. Making use of previously queried and locally-saved datafiles significantly speeds up run-time and execution of code. 

A required attribute is the absolute path directory where pickled datafiles will be saved. Starting from the current working directory, we will create a folder ``pickled_db`` and save all pickled files there. To do that, let's define the string variable ``pickled_dir`` as follows:

.. code-block:: ipython
   
   In [1]: import os
   In [2]: pickled_dir = os.getcwd() + '/pickled_db/'

For example, to construct the **Fama-French 3 factors**: the `Market Premium` ``MKT-RF``, `Small Minus Big` ``SMB``, and `High Minus Low` ``HML``, at the monthly frequency (from 1960 to the present, or the most recent date for which there is stock returns data available in CRPS and fundamentals data in Compustat), we execute the following lines of Python code:

**Fama-French 3 Factors:**

.. code-block:: ipython
    
   In [3]: import datetime as dt
   In [4]: import famafrench.famafrench as ff
   
   In [5]: startDate = dt.date(1960, 1, 1)
   In [6]: endDate = dt.date.today()
   In [7]: runQuery = True
   In [8]: ffFreq = 'M'
   In [9]: ffsortCharac = ['ME', 'BM']
   In [10]: ffFactors = ['MKT-RF', 'SMB', 'HML']
   In [11]: ff3 = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors) 

   In [12]: factorsTableM = ff3.getFFfactors(startDate, endDate)
   
   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [00:03<00:00,  1.73s/it]
   Historical risk-free interest rate (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   
   In [13]: factorsTableM.head()
   Out[13]: 
                    mkt    mkt-rf       smb       hml
   date                                              
   1960-01-31 -0.066497 -0.069797  0.017755  0.025267
   1960-02-29  0.014547  0.011647  0.006323 -0.010965
   1960-03-31 -0.012873 -0.016373 -0.001480 -0.034610
   1960-04-30 -0.015113 -0.017013 -0.001671 -0.008266
   1960-05-31  0.033918  0.031218  0.022134 -0.040884
 

- To construct Fama-French-style factors, :attr:`factorsId` (here, passed as parameter ``ffFactors``) must be passed as a list of strings with the names of the factors per the naming convention outlined in the documentation for :class:`FamaFrench<FamaFrench>`. 
- Although one can pass the anomaly portfolio characteristics used for portfolio sorting in the construction of the factors, :attr:`sortCharacsId` (here, passed as parameter ``ffsortCharac``), the constructor does not require this. Here, :attr:`mainCharacsId` is also not required for obvious reasons (when omitted, :attr:`mainCharacsId` is set to :attr:`sortCharacsId` by default).

We can compare the constructed factors to those provided by `Ken French <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_factors.html>`_: 


.. code-block:: ipython
    
   In [14]: kffactorsTableM = ff3.getkfFFfactors(ffFreq, startDate, endDate)
   In [15]: kffactorsTableM.head()
   Out[15]: 
                  mkt  mkt-rf     smb     hml
   1960-01-31 -0.0665 -0.0698  0.0209  0.0273
   1960-02-29  0.0146  0.0117  0.0051 -0.0199
   1960-03-31 -0.0128 -0.0163 -0.0051 -0.0285
   1960-04-30 -0.0152 -0.0171  0.0031 -0.0223
   1960-05-31  0.0339  0.0312  0.0121 -0.0376

   In [16]: _, _, _, = ff3.comparePortfolios('Factors', ffFreq, startDate, endDate)
   
   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...
   CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...
   Constructing Fama-French return factor(s): 100%|██████████| 2/2 [00:03<00:00,  1.78s/it]
   Historical risk-free interest rate (monthly) dataset currently NOT saved locally. Querying from wrds-cloud...
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

 
- The instance method :meth:`FamaFrench.comparePortfolios <famafrench.FamaFrench.comparePortfolios>` compares our constructed factors with those provided by French at the same frequency over the same sample period. Current output of the method includes sample `Pearson correlations`, sample `means`, and sample `standard deviations`.

**Other examples:** To form the 6 (ie 2 x 3) monthly, portfolios (also from 1960 to the present, or the most recent date for which there is stock returns data available in CRPS and fundamentals data in Compustat) sorted on `Size` ``ME`` and `Book-to-Market` ``BM`` and construct the `value`-weighted portfolio returns, number of firms in each portfolio, and the `average` anomaly portfolio characteristics used in the construction of the portfolios: market value of equity ``ME`` and book-to-market equity ``BM``, we execute the following lines of Python code:

`Value` **-weighted portfolio returns:**
 
.. code-block:: ipython
    
   In [3]: import datetime as dt
   In [4]: import famafrench.famafrench as ff
   
   In [5]: startDate = dt.date(1960, 1, 1)
   In [6]: endDate = dt.date.today()
   In [7]: runQuery = True
   In [8]: ffFreq = 'M'
   In [9]: sortingDim = [2, 3]
   In [10]: retType = 'vw'

   In [11]: ffsortCharac = ['ME', 'BM']
   In [12]: ffFactors = []
   In [13]: me_bm_2x3 = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors) 

   In [14]: returnsTableM = me_bm_2x3.getPortfolioReturns(False, startDate, endDate, sortingDim, retType)  
   
   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   
   In [15]: returnsTableM.head()
   Out[15]: 
               me0-50_bm0-30  me0-50_bm30-70  ...  me50-100_bm30-70  me50-100_bm70-100
   date 
   1960-01-31      -0.065363       -0.053950  ...         -0.045400          -0.071003                                                             
   1960-02-29       0.022127        0.006104  ...          0.038354          -0.014447
   1960-03-31      -0.013744       -0.031140  ...         -0.013633          -0.054888
   1960-04-30      -0.010691       -0.016785  ...         -0.020938          -0.014375
   1960-05-31       0.043435        0.035750  ...          0.010110          -0.017830
   
   In [16]: kfreturnsTableM = me_bm_2x3.getkfPortfolioReturns(ffFreq, startDate, endDate, sortingDim, retType) 
   In [17]: kfreturnsTableM.head()
   Out[17]:
               small lobm   me1 bm2  small hibm  big lobm   me2 bm2  big hibm
   1960-01-31   -0.057876 -0.031988   -0.029368 -0.082071 -0.043931 -0.055931
   1960-02-29    0.020772  0.014530    0.005015  0.013139  0.022903 -0.010929
   1960-03-31   -0.023385 -0.024016   -0.038293 -0.008789 -0.010768 -0.050967
   1960-04-30    0.000545 -0.021162   -0.029614 -0.015721 -0.013525 -0.030143
   1960-05-31    0.053034  0.018239    0.023730  0.043100  0.018242 -0.002716
   
   In [18]:  _, _, _, = me_bm_2x3.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, retType) 
   
   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** ME x BM (2 x 3) ************************************
       *********************** Observation frequency: M ************************
       ************************* Returns: 1960-01-31 to 2020-03-31 **************************

   Correlation matrix:
             bm0-30 bm30-70 bm70-100
    me0-50     0.99    0.99    0.994
    me50-100  0.997   0.982    0.984 

    Average matrix:
                       bm0-30         bm30-70        bm70-100
    me0-50    [0.82%, 0.84%]  [1.11%, 1.15%]  [1.28%, 1.26%]
    me50-100  [0.87%, 0.88%]  [0.92%, 0.88%]  [0.97%, 1.01%] 

    Std Deviation matrix:
                       bm0-30        bm30-70        bm70-100
    me0-50    [6.68%, 6.69%]  [5.47%, 5.4%]  [5.62%, 5.63%]
    me50-100  [4.55%, 4.54%]  [4.2%, 4.28%]  [5.06%, 4.91%] 

    Elapsed time:  84.751  seconds.


**Number of firms in each portfolio:**

.. code-block:: ipython
    
   In [19]: firmsTableM = me_bm_2x3.getNumFirms(False, startDate, endDate, sortingDim)  
   In [20]: firmsTableM.head()
   Out[20]: 
               me0-50_bm0-30  me0-50_bm30-70  ...  me50-100_bm30-70  me50-100_bm70-100
   date                                       ...                                     
   1960-01-31             21              49  ...                69                 27
   1960-02-29             21              49  ...                69                 27
   1960-03-31             21              49  ...                69                 27
   1960-04-30             21              49  ...                69                 27
   1960-05-31             21              49  ...                69                 27
   
   In [21]: kffirmsTableM = me_bm_2x3.getkfNumFirms(ffFreq, startDate, endDate, sortingDim) 
   In [22]: kffirmsTableM.head()
   Out[22]:
               small lobm  me1 bm2  small hibm  big lobm  me2 bm2  big hibm
   1960-01-31          66      193         223       228      199        72
   1960-02-29          66      193         222       228      199        72
   1960-03-31          66      192         222       228      199        72
   1960-04-30          66      190         221       228      199        72
   1960-05-31          66      187         221       228      199        72
   
   In [23]:  _, _, _, = me_bm_2x3.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim) 
   
   *********************************** ME x BM (2 x 3) ************************************
       *********************** Observation frequency: M ************************
       ************************* NumFirms: 1960-01-31 to 2020-03-31 **************************

   Correlation matrix:
             bm0-30 bm30-70 bm70-100
   me0-50     0.99   0.969     0.98
   me50-100  0.894   0.854     0.93 

   Average matrix:
                  bm0-30     bm30-70      bm70-100
   me0-50    [857, 877]  [878, 902]  [1022, 1014]
   me50-100  [336, 358]  [282, 302]    [124, 135] 

   Std Deviation matrix:
                  bm0-30     bm30-70    bm70-100
   me0-50    [501, 479]  [400, 362]  [522, 458]
   me50-100   [124, 96]    [79, 49]    [45, 34] 

   Elapsed time:  7.179  seconds.


`Equal` **-weighted average firm size** ``ME`` **and** `Value` **-weighted average** ``BM`` **for each portfolio:**

.. code-block:: ipython
    
   In [24]: characsTableM = me_bm_2x3.getCharacs(False, startDate, endDate, sortingDim)  
   In [25]: for charac in list(me_bm_2x3.mainCharacsId):
		print(charac, '\n', characsTableM[charac].head())
   
   ME

   me_bm_port  me0-50_bm0-30  me0-50_bm30-70  ...  me50-100_bm30-70  me50-100_bm70-100
   date                                       ...                                     
   1960-01-31      51.073622       44.046426  ...        602.187406         359.904699
   1960-02-29      52.018226       44.155492  ...        622.733703         352.869472
   1960-03-31      51.117399       42.638931  ...        611.268864         332.592130
   1960-04-30      50.570687       41.867309  ...        598.093774         326.359000
   1960-05-31      52.645482       43.170724  ...        601.328670         319.054963

   [5 rows x 6 columns]
   BM

   me_bm_port  me0-50_bm0-30  me0-50_bm30-70  ...  me50-100_bm30-70  me50-100_bm70-100
   date                                       ...                                     
   1960-01-31       0.442664        0.835413  ...          0.715368           1.495814
   1960-02-29       0.443257        0.835101  ...          0.716441           1.495995
   1960-03-31       0.444962        0.834058  ...          0.716098           1.479376
   1960-04-30       0.444282        0.834749  ...          0.715577           1.470528
   1960-05-31       0.442410        0.834351  ...          0.716156           1.474706
  
   [5 rows x 6 columns]
   
   In [26]: kfcharacsTableM = me_bm_2x3.getkfCharacs(ffFreq, startDate, endDate, sortingDim) 
   In [27]: for charac in list(me_bm_2x3.mainCharacsId):
		print(charac, '\n', kfcharacsTableM[charac].head())
   ME

               small lobm  me1 bm2  small hibm  big lobm  me2 bm2  big hibm
   1960-01-31       37.66    31.88       21.40    743.00   405.35    239.89
   1960-02-29       35.48    30.82       20.81    681.54   386.94    226.11
   1960-03-31       36.12    31.09       20.85    687.18   393.99    222.53
   1960-04-30       35.11    30.35       19.99    679.88   388.21    210.41
   1960-05-31       35.12    29.88       19.38    668.63   382.39    203.68
   BM

               small lobm  me1 bm2  small hibm  big lobm  me2 bm2  big hibm
   1960-01-31      0.4158   0.8464      1.7597    0.3443   0.7227    1.6961
   1960-02-29      0.4163   0.8457      1.7650    0.3454   0.7226    1.7006
   1960-03-31      0.4171   0.8449      1.7559    0.3429   0.7220    1.6942
   1960-04-30      0.4181   0.8440      1.7532    0.3412   0.7209    1.6762
   1960-05-31      0.4175   0.8428      1.7422    0.3395   0.7201    1.6721
   
   In [28]:  _, _, _, = me_bm_2x3.comparePortfolios('Characs', ffFreq, startDate, endDate, sortingDim) 
   
   CRSP (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   CRSP delisted returns (monthly) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...
   *********************************** ME x BM (2 x 3) ************************************
       *********************** Observation frequency: M ************************
    ************************* (Characteristic: ME): 1960-01-31 to 2020-03-31 ***************************

   Correlation matrix:
             bm0-30 bm30-70 bm70-100
   me0-50    0.926    0.97     0.98
   me50-100  0.996   0.932     0.98 

   Average matrix:
                          bm0-30             bm30-70           bm70-100
   me0-50      [278.71, 237.67]     [259.65, 229.2]   [150.23, 135.05]
   me50-100  [9210.17, 8892.67]  [6763.25, 6296.73]  [5489.91, 5675.8] 

   Std Deviation matrix:
                           bm0-30             bm30-70            bm70-100
   me0-50       [365.01, 269.64]     [302.07, 254.2]    [173.26, 147.65]
   me50-100  [10231.33, 9921.44]  [8525.22, 7200.64]  [6790.97, 6998.62] 
   
   *********************************** ME x BM (2 x 3) ************************************
       *********************** Observation frequency: M ************************
    ************************* (Characteristic: BM): 1960-01-31 to 2020-03-31 ***************************

   Correlation matrix:
              bm0-30 bm30-70 bm70-100
   me0-50    0.996   0.994    0.972
   me50-100  0.991   0.992    0.723 

   Average matrix:
                    bm0-30       bm30-70      bm70-100
   me0-50     [0.3, 0.31]  [0.71, 0.73]  [1.43, 1.51]
   me50-100  [0.28, 0.29]  [0.68, 0.71]   [1.3, 1.32] 

   Std Deviation matrix:
                     bm0-30       bm30-70      bm70-100
   me0-50    [0.13, 0.13]  [0.28, 0.28]  [0.53, 0.55]
   me50-100  [0.12, 0.12]  [0.27, 0.27]   [0.6, 0.47] 


   Elapsed time:  68.136  seconds.


- If attribute :attr:`mainCharacsId` is not specified (as in the example above), then the class constructor sets it to :attr:`sortCharacsId` (here, passed as parameter ``ffsortCharac``). 
- Since the focus is on constructing portfolios, not factors, :attr:`factorsId` (here, passed as parameter ``ffFactors``) is set to an empty list. 
- Lastly, :attr:`sortingDim` is set to ``[2, 3]`` and :attr:`retType` is set to ``vw`` in order to form the 6 (ie 2 x 3) portfolios. 

More applications and detailed examples are provided in :ref:`applications/applications:Applications and Examples`.


    
