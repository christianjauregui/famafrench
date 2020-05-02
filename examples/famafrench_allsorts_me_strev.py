"""
This file is part of famafrench.
Copyright (c) 2020, Christian Jauregui <chris.jauregui@berkeley.edu>
See file LICENSE.txt for license information.

Filename
________
`examples/famafrench_allsorts_me_strev.py`

Construct portfolio returns based using univariate or bivariate sorts on
* Size (ME)
* Short-Term Reversal: Prior (1-1) returns (PRIOR_1_1)

Ken French online library:
10 Portfolios Formed on Short-Term Reversal
____________________________________
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_10_port_form_pr_1_0.html
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_10_port_form_pr_1_0_daily.html

6 Portfolios Formed on Size and Short-Term Reversal (2 x 3)
____________________________________
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_6_port_form_sz_pr_1_0.html
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_6_port_form_sz_pr_1_0_daily.html

25 Portfolios Formed on Size and Short-Term Reversal (5 x 5)
____________________________________
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_25_port_form_sz_pr_1_0.html
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_25_port_form_sz_pr_1_0_daily.html

"""
import os
import datetime as dt
import famafrench.famafrench as ff

startDate = dt.date(1960, 1, 1)  # "default" startDate
endDate = dt.date.today()  # "default" endDate
#startDate = dt.date(1970, 1, 1)
#endDate = dt.date(2019, 12, 31)

# pickled_dir
pickled_dir = os.getcwd() + '/famafrench/pickled_db/'

#%%
#**************************************************************************#
#**************************************************************************#
#******     Short-Term Reversal: Prior (1-1) returns (PRIOR_1_1)     ******#
#**************************************************************************#
#**************************************************************************#

#**********************************************************************************************#
# Daily Portfolios Formed on Prior (1-1) returns (PRIOR_1_1)
#**********************************************************************************************#
runQuery = True
ffFreq = 'D'
ffFactors, ffsortCharac, ffportCharac = [], ['PRIOR_1_1'], ['ME', 'PRIOR_1_1']
ff_D = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 3 portfolios (3x1) sorted on ['PRIOR_1_1']
sortingDim = [3]
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 5 portfolios (5x1) sorted on ['PRIOR_1_1']
sortingDim = [5]
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 10 portfolios (10x1) sorted on ['PRIOR_1_1']
sortingDim = [10]
_, _, _, = ff_D.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Monthly Portfolios Formed on Prior (1-1) returns (PRIOR_1_1)
#**********************************************************************************************#
runQuery = True
ffFreq = 'M'
ffFactors, ffsortCharac, ffportCharac = [], ['PRIOR_1_1'], ['ME', 'PRIOR_1_1']
ff_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 3 portfolios (3x1) sorted on ['PRIOR_1_1']
sortingDim = [3]
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 5 portfolios (5x1) sorted on ['PRIOR_1_1']
sortingDim = [5]
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 10 portfolios (10x1) sorted on ['PRIOR_1_1']
sortingDim = [10]
#portTableM = ff_M.getPortfolioReturns(False, startDate, endDate, sortingDim, 'vw')
#kfportTableM = ff_M.getkfPortfolioReturns(ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Annual Portfolios Formed on Prior (1-1) returns (PRIOR_1_1)
#**********************************************************************************************#
runQuery = False
ffFreq = 'A'
ffFactors, ffsortCharac, ffportCharac = [], ['PRIOR_1_1'], ['ME', 'PRIOR_1_1']
ff_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 3 portfolios (3x1) sorted on ['PRIOR_1_1']
sortingDim = [3]
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 5 portfolios (5x1) sorted on ['PRIOR_1_1']
sortingDim = [5]
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 10 portfolios (10x1) sorted on ['PRIOR_1_1']
sortingDim = [10]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#****************************************************************************#
#****************************************************************************#
#****  Size (ME) x Short-Term Reversal: Prior (1-1) returns (PRIOR_1_1)  ****#
#****************************************************************************#
#****************************************************************************#

#**********************************************************************************************#
# Daily Portfolios Formed on Size (ME) x Prior (1-1) returns (PRIOR_1_1)
#**********************************************************************************************#
runQuery = True
ffFreq = 'D'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'PRIOR_1_1'], ['ME', 'PRIOR_1_1']
ff_D = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME, 'PRIOR_1_1']
sortingDim = [2, 3]
_, _, _, = ff_D.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['ME, 'PRIOR_1_1']
sortingDim = [5, 5]
_, _, _, = ff_D.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME, 'PRIOR_1_1']
sortingDim = [10, 10]
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Monthly Portfolios Formed on Size (ME) x Prior (1-1) returns (PRIOR_1_1)
#**********************************************************************************************#
runQuery = True
ffFreq = 'M'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'PRIOR_1_1'], ['ME', 'PRIOR_1_1']
ff_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME, 'PRIOR_1_1']
sortingDim = [2, 3]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['ME, 'PRIOR_1_1']
sortingDim = [5, 5]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME, 'PRIOR_1_1']
sortingDim = [10, 10]
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Annual Portfolios Formed on Size (ME) x Prior (1-1) returns (PRIOR_1_1)
#**********************************************************************************************#
runQuery = False
ffFreq = 'A'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'PRIOR_1_1'], ['ME', 'PRIOR_1_1']
ff_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME, 'PRIOR_1_1']
sortingDim = [2, 3]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['ME, 'PRIOR_1_1']
sortingDim = [5, 5]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME, 'PRIOR_1_1']
sortingDim = [10, 10]
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

