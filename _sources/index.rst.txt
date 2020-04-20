.. _overview:

****************************************
``famafrench`` - Package Documentation
****************************************

Toolbox for constructing and replicating datasets from `Ken French's online data library <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>`_ by accessing WRDS remotely through its cloud server.  

Future plans are to continue to expand the toolbox to include additional factor-based datasets relevant for empirical asset pricing. 

Please reach out if you have any recommendations or suggestions for improvements. Collaborations are welcomed - reach out!

Contents
========

- What's New?!
- Getting Started
- Applications 
- Connecting to the WRDS cloud server
- WRDS Query Tools 
- Estimating Market Betas and Rolling Residual Variances 
- Constructing Portfolios and Return-Based Factors 
- Comparing to Ken French's Online Library 
- Summary Statistics and Diagnostics 
- Auxiliary Functions and Utilities 
- API Reference

.. toctree::
    :maxdepth: 2
    :hidden:
	
    What's New?! <whatsnew/whatsnew>
    Getting Started <gettingstarted/gettingstarted>
    Applications <applications/applications>
    Connecting to the WRDS cloud server <wrdsconnection/wrdsconnection>
    WRDS Query Tools <wrdscloudquery/wrdscloudquery>
    Estimating Market Betas and Rolling Residual Variances <portfolios/factorregressions>
    Constructing Portfolios and Return-Based Factors <portfolios/portfoliosorting>
    Comparing to Ken French's Online Library <kflibrary/kflibrary>
    Summary Statistics and Diagnostics <statistics-diagnostics/statistics>
    Auxiliary Functions and Utilities <utils/utils>
    API Reference <api>



How to Cite
===========
This package (and its release) should be cited using Zenodo as follows:

.. [*] Christian Jauregui. (2020, April 15). christianjauregui/famafrench: Release 1.0 (Version 0).


*******************
`Todo`
*******************
.. todo::

	`Ken French's data library documentation <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>`_ 
	notes the following regarding the construction of their daily portfolio returns:
	
   	* `In May 2015, we made two changes in the way we compute daily portfolio returns so the process is closer to the way we compute monthly portfolio returns. In daily files produced in May 2015 or thereafter, stocks are dropped from a portfolio immediately after their CRSP delist date; in files produced before May 2015, those stocks are held until the portfolio is reconstituted, at the end of June. Also, in daily files produced before May 2015 we exclude a stock from portfolios during any period in which it is missing prices for more than 10 consecutive trading no price for more than 200 consecutive trading days.`

	Future versions will verify the aforementioned adjustments are accounted for in the package's construction of daily portfolio returns. 


*******************
Indices and Tables
*******************

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
