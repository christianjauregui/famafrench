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
   
   ~wrdsconnect.wrdsConnection.connect
   ~wrdsconnect.wrdsConnection.close
   ~wrdsconnect.wrdsConnection.get_wrds_table
   ~wrdsconnect.wrdsConnection.raw_sql


``wrds-cloud`` Query Tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   ~FamaFrench.queryComp
   ~FamaFrench.queryCrsp
   ~FamaFrench.queryCrspdlret
   ~FamaFrench.queryrf1m
   ~FamaFrench.getCrspDailyRollVar
   ~FamaFrench.aggregateME
   ~FamaFrench.getMEDec
   ~FamaFrench.getMEJune
   ~FamaFrench.mergeCCM


Estimating Market Betas and Rolling Residual Variances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   ~FamaFrench.getFactorRegResults


Constructing Portfolios and Return-Based Factors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   ~FamaFrench.getNyseThresholdsAndRet
   ~FamaFrench.getPortfolios
   ~FamaFrench.getPortfolioReturns
   ~FamaFrench.getNumFirms
   ~FamaFrench.getCharacs
   ~FamaFrench.getFFfactors


Comparing to Ken French's Online Library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   ~FamaFrench.kfLibrary
   ~FamaFrench.getkfPortfolioReturns
   ~FamaFrench.getkfNumFirms
   ~FamaFrench.getkfCharacs
   ~FamaFrench.getkfFFfactors


Summary Statistics and Diagnostics
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   ~FamaFrench.getFamaFrenchStats
   ~FamaFrench.comparePortfolios
   

Auxiliary Functions and Utilities
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autosummary::
   :nosignatures:

   ~utils.lru_cached_method
   ~utils.get_kfpriorfactors_directly
   ~utils.timing
   ~utils.any_in
   ~utils.priormonthToDay
   ~utils.grouped_vwAvg
   ~utils.portRetAvg
   ~utils.get_statsTable	
 









