"""
This file is part of famafrench.
Copyright (c) 2020, Christian Jauregui <chris.jauregui@berkeley.edu>
See file LICENSE.txt for license information.

Filename
_________
`examples/famafrenchbisorts_me_bm_op_inv.py`

Construct portfolio returns based using bivariate sorts on
* Size (ME)
* Book-to-Market (BM)
* Operating Profitability (OP)
* Investment (INV)

Ken French online library:
Univariate sorts on Size, B/M, OP, and Inv
__________________________________________
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html

"""
import os
import datetime as dt
import famafrench.famafrench as ff

from importlib import reload
reload(ff)

startDate = dt.date(1960, 1, 1)  # "default" startDate
endDate = dt.date.today()  # "default" endDate
#startDate = dt.date(1970, 1, 1)
#endDate = dt.date(2019, 12, 31)

# pickled_dir
pickled_dir = os.getcwd() + '/famafrench/pickled_db/'

#%%
#**********************************************************************************************#
#**********************************************************************************************#
#*************************        Size (ME) x Book-to-Market (BM)     *************************#
#**********************************************************************************************#
#**********************************************************************************************#

#**********************************************************************************************#
# Daily Portfolios Formed on Size (ME) x Book-to-Market (BM)
#**********************************************************************************************#
runQuery = True
ffFreq = 'D'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'BM'], ['ME', 'BM']
ff_D = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME', 'BM']
sortingDim = [2, 3]
_, _, _, = ff_D.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['ME', 'BM']
sortingDim = [5, 5]
_, _, _, = ff_D.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME', 'BM']
sortingDim = [10, 10]
_, _, _, = ff_D.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Weekly Portfolios Formed on Size (ME) x Book-to-Market (BM)
#**********************************************************************************************#
runQuery = False
ffFreq = 'W'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'BM'], ['ME', 'BM']
ff_W = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME', 'BM']
sortingDim = [2, 3]
_, _, _, = ff_W.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
ff_W.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_W.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_W.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['ME', 'BM']
sortingDim = [5, 5]
ff_W.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_W.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_W.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME', 'BM']
sortingDim = [10, 10]
ff_W.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_W.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_W.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Monthly Portfolios Formed on Size (ME) x Book-to-Market (BM)
#**********************************************************************************************#
runQuery = True
ffFreq = 'M'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'BM'], ['ME', 'BM']
ff_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME', 'BM']
sortingDim = [2, 3]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['ME', 'BM']
sortingDim = [5, 5]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME', 'BM']
sortingDim = [10, 10]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Annual Portfolios Formed on Size (ME) x Book-to-Market (BM)
#**********************************************************************************************#
runQuery = False
ffFreq = 'A'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'BM'], ['ME', 'BM']
ff_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME', 'BM']
sortingDim = [2, 3]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['ME', 'BM']
sortingDim = [5, 5]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME', 'BM']
sortingDim = [10, 10]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
#**********************************************************************************************#
#*********************        Size (ME) x Operating Profitability (OP)     ********************#
#**********************************************************************************************#
#**********************************************************************************************#

#**********************************************************************************************#
# Daily Portfolios Formed on Size (ME) x Operating Profitability (OP)
#**********************************************************************************************#
runQuery = True
ffFreq = 'D'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'OP'], ['ME', 'OP']
ff_D = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME', 'OP']
sortingDim = [2, 3]
_, _, _, = ff_D.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['ME', 'OP']
sortingDim = [5, 5]
_, _, _, = ff_D.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME', 'OP']
sortingDim = [10, 10]
_, _, _, = ff_D.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

#%%
#**********************************************************************************************#
# Monthly Portfolios Formed on Size (ME) x Operating Profitability (OP)
#**********************************************************************************************#
runQuery = True
ffFreq = 'M'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'OP'], ['ME', 'OP']
ff_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME', 'OP']
sortingDim = [2, 3]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['ME', 'OP']
sortingDim = [5, 5]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME', 'OP']
sortingDim = [10, 10]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#**********************************************************************************************#
# Annual Portfolios Formed on Size (ME) x Operating Profitability (OP)
#**********************************************************************************************#
runQuery = False
ffFreq = 'A'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'OP'], ['ME', 'OP']
ff_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME', 'OP']
sortingDim = [2, 3]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['ME', 'OP']
sortingDim = [5, 5]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME', 'OP']
sortingDim = [10, 10]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
#**********************************************************************************************#
#****************************       Size (ME) x Investment (INV)     **************************#
#**********************************************************************************************#
#**********************************************************************************************#

#**********************************************************************************************#
# Daily Portfolios Formed on Size (ME) x Investment (INV)
#**********************************************************************************************#
runQuery = True
ffFreq = 'D'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'INV'], ['ME', 'INV']
ff_D = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME', 'INV']
sortingDim = [2, 3]
_, _, _, = ff_D.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['ME', 'INV']
sortingDim = [5, 5]
_, _, _, = ff_D.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME', 'INV']
sortingDim = [10, 10]
_, _, _, = ff_D.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Monthly Portfolios Formed on Size (ME) x Investment (INV)
#**********************************************************************************************#
runQuery = True
ffFreq = 'M'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'INV'], ['ME', 'INV']
ff_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME', 'INV']
sortingDim = [2, 3]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['ME', 'INV']
sortingDim = [5, 5]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME', 'INV']
sortingDim = [10, 10]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Annual Portfolios Formed on Size (ME) x Investment (INV)
#**********************************************************************************************#
runQuery = False
ffFreq = 'A'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'INV'], ['ME', 'INV']
ff_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['ME', 'INV']
sortingDim = [2, 3]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['ME', 'INV']
sortingDim = [5, 5]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['ME', 'INV']
sortingDim = [10, 10]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
#**********************************************************************************************#
#******************      Book-to-Market (BM) x Operating Profitability (OP)    ****************#
#**********************************************************************************************#
#**********************************************************************************************#

#**********************************************************************************************#
# Daily Portfolios Formed on Book-to-Market (BM) x Operating Profitability (OP)
#**********************************************************************************************#
runQuery = True
ffFreq = 'D'
ffFactors, ffsortCharac, ffportCharac = [], ['BM', 'OP'], ['BM', 'OP']
ff_D = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['BM', 'OP']
sortingDim = [2, 3]
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['BM', 'OP']
sortingDim = [5, 5]
_, _, _, = ff_D.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['BM', 'OP']
sortingDim = [10, 10]
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Monthly Portfolios Formed on Book-to-Market (BM) x Operating Profitability (OP)
#**********************************************************************************************#
runQuery = True
ffFreq = 'M'
ffFactors, ffsortCharac, ffportCharac = [], ['BM', 'OP'], ['BM', 'OP']
ff_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['BM', 'OP']
sortingDim = [2, 3]
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['BM', 'OP']
sortingDim = [5, 5]
#portTableM = ff_M.getPortfolioReturns(False, startDate, endDate, sortingDim, 'vw')
#kfportTableM = ff_M.getkfPortfolioReturns(ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['BM', 'OP']
sortingDim = [10, 10]
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Annual Portfolios Formed on Book-to-Market (BM) x Operating Profitability (OP)
#**********************************************************************************************#
runQuery = False
ffFreq = 'A'
ffFactors, ffsortCharac, ffportCharac = [], ['BM', 'OP'], ['BM', 'OP']
ff_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['BM', 'OP']
sortingDim = [2, 3]
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['BM', 'OP']
sortingDim = [5, 5]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['BM', 'OP']
sortingDim = [10, 10]
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
#**********************************************************************************************#
#***********************      Book-to-Market (BM) x Investment (INV)      *********************#
#**********************************************************************************************#
#**********************************************************************************************#

#**********************************************************************************************#
# Daily Portfolios Formed on Book-to-Market (BM) x Investment (INV)
#**********************************************************************************************#
runQuery = True
ffFreq = 'D'
ffFactors, ffsortCharac, ffportCharac = [], ['BM', 'INV'], ['BM', 'INV']
ff_D = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['BM', 'INV']
sortingDim = [2, 3]
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['BM', 'INV']
sortingDim = [5, 5]
_, _, _, = ff_D.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['BM', 'INV']
sortingDim = [10, 10]
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Monthly Portfolios Formed on Book-to-Market (BM) x Investment (INV)
#**********************************************************************************************#
runQuery = True
ffFreq = 'M'
ffFactors, ffsortCharac, ffportCharac = [], ['BM', 'INV'], ['BM', 'INV']
ff_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['BM', 'INV']
sortingDim = [2, 3]
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['BM', 'INV']
sortingDim = [5, 5]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['BM', 'INV']
sortingDim = [10, 10]
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Annual Portfolios Formed on Book-to-Market (BM) x Investment (INV)
#**********************************************************************************************#
runQuery = False
ffFreq = 'A'
ffFactors, ffsortCharac, ffportCharac = [], ['BM', 'INV'], ['BM', 'INV']
ff_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['BM', 'INV']
sortingDim = [2, 3]
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['BM', 'INV']
sortingDim = [5, 5]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['BM', 'INV']
sortingDim = [10, 10]
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
#**********************************************************************************************#
#*******************      Operating Profitability (OP) x Investment (INV)      ****************#
#**********************************************************************************************#
#**********************************************************************************************#

#**********************************************************************************************#
# Daily Portfolios Formed on Operating Profitability (OP) x Investment (INV)
#**********************************************************************************************#
runQuery = True
ffFreq = 'D'
ffFactors, ffsortCharac, ffportCharac = [], ['OP', 'INV'], ['OP', 'INV']
ff_D = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['OP', 'INV']
sortingDim = [2, 3]
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['OP', 'INV']
sortingDim = [5, 5]
_, _, _, = ff_D.comparePortfolios('Returns', ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['OP', 'INV']
sortingDim = [10, 10]
ff_D.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_D.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_D.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Monthly Portfolios Formed on Operating Profitability (OP) x Investment (INV)
#**********************************************************************************************#
runQuery = True
ffFreq = 'M'
ffFactors, ffsortCharac, ffportCharac = [], ['OP', 'INV'], ['OP', 'INV']
ff_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['OP', 'INV']
sortingDim = [2, 3]
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['OP', 'INV']
sortingDim = [5, 5]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['OP', 'INV']
sortingDim = [10, 10]
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

#%%
#**********************************************************************************************#
# Annual Portfolios Formed on Operating Profitability (OP) x Investment (INV)
#**********************************************************************************************#
runQuery = False
ffFreq = 'A'
ffFactors, ffsortCharac, ffportCharac = [], ['OP', 'INV'], ['OP', 'INV']
ff_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 6 portfolios (2x3) sorted on ['OP', 'INV']
sortingDim = [2, 3]
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 25 portfolios (5x5) sorted on ['OP', 'INV']
sortingDim = [5, 5]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)

# - 100 portfolios (10x10) sorted on ['OP', 'INV']
sortingDim = [10, 10]
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)