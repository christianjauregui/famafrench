"""
# This file is part of famafrench
# Copyright (c) 2020, Christian Jauregui <chris.jauregui@berkeley.edu>
# See file LICENSE.txt for license information.

Filename
_________
`examples/famafrench_allsorts_me_ac.py`

Construct portfolio returns based using univariate or bivariate sorts on
* Size (ME)
* Accruals (AC)

Ken French online library:
Portfolios Formed on Accruals
____________________________________
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_port_form_AC.html

25 Portfolios Formed on Size and Accruals
____________________________________
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/tw_5_ports_me_AC.html

"""
import famafrench.famafrench as ff
import datetime as dt

startDate = dt.date(1950, 1, 1)  # "default" startDate
endDate = dt.date.today()  # "default" endDate
#startDate = dt.date(1970, 1, 1)
#endDate = dt.date(2019, 12, 31)


#%%
#**************************************************************************#
#**************************************************************************#
#*******************           Accruals (AC)          *********************#
#**************************************************************************#
#**************************************************************************#

#**********************************************************************************************#
# Daily Portfolios Formed on Accruals (AC)
#**********************************************************************************************#
runQuery = True
ffFreq = 'D'
ffFactors, ffsortCharac, ffportCharac = [], ['AC'], ['AC']
ff_D = ff.FamaFrench(runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 3 portfolios (3x1) sorted on ['AC']
sortingDim = [3]
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 5 portfolios (5x1) sorted on ['AC']
sortingDim = [5]
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 10 portfolios (10x1) sorted on ['AC']
sortingDim = [10]
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Monthly Portfolios Formed on Accruals (AC)
#**********************************************************************************************#
runQuery = True
ffFreq = 'M'
ffFactors, ffsortCharac, ffportCharac = [], ['AC'], ['ME', 'AC']
ff_M = ff.FamaFrench(runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 3 portfolios (3x1) sorted on ['AC']
sortingDim = [3]
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 5 portfolios (5x1) sorted on ['AC']
sortingDim = [5]
#portTableM = ff_M.getPortfolioReturns(False, startDate, endDate, sortingDim, 'vw')
#kfportTableM = ff_M.getkfPortfolioReturns(ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms',  ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 10 portfolios (10x1) sorted on ['AC']
sortingDim = [10]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms',  ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Annual Portfolios Formed on Accruals (AC)
#**********************************************************************************************#
runQuery = False
ffFreq = 'A'
ffFactors, ffsortCharac, ffportCharac = [], ['AC'], ['ME', 'AC']
ff_A = ff.FamaFrench(runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 3 portfolios (3x1) sorted on ['AC']
sortingDim = [3]
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 5 portfolios (5x1) sorted on ['AC']
sortingDim = [5]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 10 portfolios (10x1) sorted on ['AC']
sortingDim = [10]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#*******************************************************************************#
#*******************************************************************************#
#*************              Size (ME) x Accruals (AC)              *************#
#*******************************************************************************#
#*******************************************************************************#

#**********************************************************************************************#
# Daily Portfolios Formed on Size (ME) x Accruals (AC)
#**********************************************************************************************#
runQuery = True
ffFreq = 'D'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'AC'], ['ME', 'AC']
ff_D = ff.FamaFrench(runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME, 'AC']
sortingDim = [2, 3]
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['ME, 'AC']
sortingDim = [5, 5]
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME, 'AC']
sortingDim = [10, 10]
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Monthly Portfolios Formed on Size (ME) x Accruals (AC)
#**********************************************************************************************#
runQuery = True
ffFreq = 'M'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'AC'], ['ME', 'AC']
ff_M = ff.FamaFrench(runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME, 'AC']
sortingDim = [2, 3]
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x15 sorted on ['ME, 'AC']
sortingDim = [5, 5]
#portTableM = ff_M.getPortfolioReturns(False, startDate, endDate, sortingDim, 'vw')
#kfportTableM = ff_M.getkfPortfolioReturns(ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms',  ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME, 'AC']
sortingDim = [10, 10]
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Annual Portfolios Formed on Size (ME) x Accruals (AC)
#**********************************************************************************************#
runQuery = False
ffFreq = 'A'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'AC'], ['ME', 'AC']
ff_A = ff.FamaFrench(runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME, 'AC']
sortingDim = [2, 3]
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x15 sorted on ['ME, 'AC']
sortingDim = [5, 5]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME, 'AC']
sortingDim = [10, 10]
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)