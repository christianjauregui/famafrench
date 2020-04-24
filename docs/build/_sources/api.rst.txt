.. _api:

******************************
API Reference
******************************
This is a comprehensive reference for everything you get when you ``import famafrench``.

.. contents:: Table of Contents
    :local:
    :depth: 4

.. module:: famafrench


``FamaFrench`` Constructor
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:
   
   ~FamaFrench


``wrdsConnection`` Constructor
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:
   
   ~wrdsconnect.wrdsConnection

Connecting to ``wrds-cloud``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:
   
   ~famafrench.wrdsconnect.wrdsConnection.connect
   ~famafrench.wrdsconnect.wrdsConnection.close
   ~famafrench.wrdsconnect.wrdsConnection.get_wrds_table
   ~famafrench.wrdsconnect.wrdsConnection.raw_sql


``wrds-cloud`` Query Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   ~famafrench.FamaFrench.queryComp
   ~famafrench.FamaFrench.queryCrsp
   ~famafrench.FamaFrench.queryCrspdlret
   ~famafrench.FamaFrench.queryrf1m
   ~famafrench.FamaFrench.getCrspDailyRollVar
   ~famafrench.FamaFrench.aggregateME
   ~famafrench.FamaFrench.getMEDec
   ~famafrench.FamaFrench.getMEJune
   ~famafrench.FamaFrench.mergeCCM


Estimating Market Betas and Rolling Residual Variances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   ~famafrench.FamaFrench.getFactorRegResults


Constructing Portfolios and Return-Based Factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   ~famafrench.FamaFrench.getNyseThresholdsAndRet
   ~famafrench.FamaFrench.getPortfolios
   ~famafrench.FamaFrench.getPortfolioReturns
   ~famafrench.FamaFrench.getNumFirms
   ~famafrench.FamaFrench.getCharacs
   ~famafrench.FamaFrench.getFFfactors


Comparing to Ken French's Online Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   ~famafrench.FamaFrench.kfLibrary
   ~famafrench.FamaFrench.getkfPortfolioReturns
   ~famafrench.FamaFrench.getkfNumFirms
   ~famafrench.FamaFrench.getkfCharacs
   ~famafrench.FamaFrench.getkfFFfactors


Summary Statistics and Diagnostics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   ~famafrench.FamaFrench.getFamaFrenchStats
   ~famafrench.FamaFrench.comparePortfolios
   

Auxiliary Functions and Utilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   ~famafrench.utils.lru_cached_method
   ~famafrench.utils.get_kfpriorfactors_directly
   ~famafrench.utils.timing
   ~famafrench.utils.any_in
   ~famafrench.utils.priormonthToDay
   ~famafrench.utils.grouped_vwAvg
   ~famafrench.utils.portRetAvg
   ~famafrench.utils.get_statsTable	
 









