.. _overview:

****************************************
``famafrench`` - Package Documentation
****************************************

Toolbox for constructing and replicating datasets from `Ken French's online data library <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>`_ by accessing `WRDS <https://wrds-www.wharton.upenn.edu/>`_ remotely through its cloud server.  

``famafrench``'s current efficient performance results from features such as the use of a `least recently used (LRU) cache <https://medium.com/lambda-automotive/python-and-lru-cache-f812bbdcbb51>`_ implemented using Python's :func:`functools.lru_cache`.

Future plans are to continue to expand the toolbox to include additional factor-based datasets relevant for empirical asset pricing. These include the following:

- `AQR Capital Management's <https://www.aqr.com/library/data-sets>`_:
   
      * `Betting Against Beta` (BAB)
      * `Quality Minus Junk` (QMJ)
      * `Modified Value - High Minus Low` (HMLD)

- `Lettau, Ludvigson, and Ma (2019) <https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12772>`_ Capital Share Factor:

    * `Capital Share of Aggregate Income` (KS)

- `Pastor and Stambaugh (2003) <https://faculty.chicagobooth.edu/-/media/faculty/lubos-pastor/data/liq_data_1962_2019.txt>`_ Liquidity Factors:
      
      * `Non-Traded Liquidity Factor`
      * `Traded Liquidity Factor`

- `Sadka (2006) <https://drive.google.com/file/d/1hTnBk7uasanA3x1gRFBNg6hFE1A0JJEO/view>`_ Liquidity Factors:
      
      * `Fixed-Transitory Factor`
      * `Variable-Permanent Factor`

- `Stambaugh and Yuan (2017) <https://academic.oup.com/rfs/article/30/4/1270/2965095>`_ `Clustered` Mispricing Factors:
       
      * `Management-related Factor` (MGMT)
      * `Performance-related Factor` (PERF)
      * `Mispricing (non-clustered) Factor` (UMO)


Please reach out if you have any recommendations or suggestions for improvements. Collaborations are welcomed - reach out at **chris.jauregui@berkeley.edu**!

Contents
========

- What's New?!
- Getting Started
- Applications and Examples
- Connecting to the WRDS cloud server
- WRDS Query Tools 
- Estimating Market Betas and Rolling Residual Variances 
- Constructing Portfolios and Return-Based Factors 
- Comparing to Ken French's Online Library 
- Summary Statistics and Diagnostics 
- Auxiliary Functions and Utilities 
- API Reference
- Change Log

.. toctree::
    :maxdepth: 2
    :hidden:
	
    What's New?! <whatsnew/whatsnew>
    Getting Started <gettingstarted/gettingstarted>
    Applications and Examples <applications/applications>
    Connecting to the WRDS cloud server <wrdsconnection/wrdsconnection>
    WRDS Query Tools <wrdscloudquery/wrdscloudquery>
    Estimating Market Betas and Rolling Residual Variances <portfolios/factorregressions>
    Constructing Portfolios and Return-Based Factors <portfolios/portfoliosorting>
    Comparing to Ken French's Online Library <kflibrary/kflibrary>
    Summary Statistics and Diagnostics <statistics-diagnostics/statistics>
    Auxiliary Functions and Utilities <utils/utils>
    API Reference <api>
    Change Log <changes/changes>


************
How to Cite
************
This package (and its release as of April 20, 2020) should be cited using Zenodo. For example, for the 0.1.0 release, 

   [*] Christian Jauregui. (2020, April 20). christianjauregui/famafrench: Release 0.1.0 (Initial Release). Zenodo. https://sandbox.zenodo.org/record/530634#.XqNbfJNKi_t

      .. image:: https://sandbox.zenodo.org/badge/doi/10.5072/zenodo.530634.svg
         :target: https://sandbox.zenodo.org/record/530634#.XqNawZNKi_s

*******************
`Todo`
*******************
.. todo::

	`Ken French's data library documentation <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>`_ 
	notes the following regarding the construction of their daily portfolio returns:
	
   	* `In May 2015, we made two changes in the way we compute daily portfolio returns so the process is closer to the way we compute monthly portfolio returns. In daily files produced in May 2015 or thereafter, stocks are dropped from a portfolio immediately after their CRSP delist date; in files produced before May 2015, those stocks are held until the portfolio is reconstituted, at the end of June. Also, in daily files produced before May 2015 we exclude a stock from portfolios during any period in which it is missing prices for more than 10 consecutive trading no price for more than 200 consecutive trading days.`

	Future versions will verify the aforementioned adjustments are accounted for in the package's construction of daily portfolio returns. 

.. todo::
	* Include option to construct the `Fama and French (2018) <https://www.sciencedirect.com/science/article/abs/pii/S0304405X18300515>`_ cash-based profitability factor, ``RMWc``.
        * Within the instance method used for constructing market betas and rolling residual variances, :meth:`getFactorResults`, extend the `Dimson (1979) <https://www.sciencedirect.com/science/article/abs/pii/0304405X79900138>`_ methodology based on `Scholes and Williams (1977) <https://www.sciencedirect.com/science/article/abs/pii/0304405X77900411>`_ to other factor quantities of risk beyond the `market (CAPM)` beta (eg, `SMB` and `HML` quantities of risk).
        * Verify the `pandas-datareader <https://pandas-datareader.readthedocs.io/en/latest/>`_ Python library is still unable to pull monthly and annual datafiles for the `Short-Term Reversal` or `Long-Term Reversal` Fama-French-style factors made public through `Ken French's online library <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>`_. 
        * When applicable, constructed portfolios, specifically portfolio returns, number of firms in each portfolio, and `average` anomaly portfolio characteristics are compared with those provided by Ken French for the same frequency and over the same period. The sample `Pearson correlations`, sample `means`, and sample `standard deviations` for the following portfolios **can be improved**:
   		
		- `Portfolios Formed on Dividend Yield <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_port_form_dp.html>`_
		- `6 Portfolios Formed on Size and Dividend Yield <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/six_portfolios_me_dp.html>`_
		- `Portfolios Formed on Accruals <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_port_form_AC.html>`_
		- `25 Portfolios Formed on Size and Accruals <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/tw_5_ports_me_AC.html>`_
		- `Portfolios Formed on Market Beta <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_port_form_BETA.html>`_
		- `25 Portfolios Formed on Size and Market Beta <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/tw_5_ports_me_BETA.html>`_
		
	 To improve the statistical metrics, adjustments in how the aforementioned anomaly characteristics are computed or estimated will be incorporated in future releases. 
	
        
*******************
Indices and Tables
*******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
