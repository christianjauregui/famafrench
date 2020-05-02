"""
This file is part of famafrench.
Copyright (c) 2020, Christian Jauregui <chris.jauregui@berkeley.edu>
See file LICENSE.txt for license information.

Filename
_________
`examples/famafrench_trisorts_me_bm_op_inv.py`

Construct portfolio returns based using trivariate sorts on
* Size (ME)
* Book-to-Market (BM)
* Operating Profitability (OP)
* Investment (INV)

Ken French online library:
32 Portfolios Formed on Size, Book-to-Market, and Operating Profitability (2 x 4 x 4)
______________________________________________________________________________________
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/32_ports_me_beme_op.html

32 Portfolios Formed on Size, Book-to-Market, and Investment (2 x 4 x 4)
_________________________________________________________________________
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/32_ports_me_beme_inv.html

32 Portfolios Formed on Size, Operating Profitability, and Investment (2 x 4 x 4)
__________________________________________________________________________________
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/32_ports_me_op_inv.html

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
#**********************************************************************************************#
#**********************************************************************************************#
#*********       Size (ME) x Book-to-Market (BM) x Operating Profitability (OP)       *********#
#**********************************************************************************************#
#**********************************************************************************************#

#**********************************************************************************************#
# Monthly Portfolios Formed on Size (ME) x Book-to-Market (BM) x Operating Profitability (OP)
#**********************************************************************************************#
runQuery = True
ffFreq = 'M'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'BM', 'OP'], ['ME', 'BM', 'OP', 'INV']
ff_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 32 portfolios (2x4x4) sorted on ['ME', 'BM', 'OP']
sortingDim = [2, 4, 4]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Annual Portfolios Formed on Size (ME) x Book-to-Market (BM) x Operating Profitability (OP)
#**********************************************************************************************#
runQuery = False
ffFreq = 'A'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'BM', 'OP'], ['ME', 'BM', 'OP', 'INV']
ff_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 32 portfolios (2x4x4) sorted on ['ME', 'BM', 'OP']
sortingDim = [2, 4, 4]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
#**********************************************************************************************#
#***************       Size (ME) x Book-to-Market (BM) x Investment (INV)       ***************#
#**********************************************************************************************#
#**********************************************************************************************#

#**********************************************************************************************#
# Monthly Portfolios Formed on Size (ME) x Book-to-Market (BM) x Investment (INV)
#**********************************************************************************************#
runQuery = True
ffFreq = 'M'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'BM', 'INV'], ['ME', 'BM', 'OP', 'INV']
ff_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 32 portfolios (2x4x4) sorted on ['ME', 'BM', 'INV']
sortingDim = [2, 4, 4]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Annual Portfolios Formed on Size (ME) x Book-to-Market (BM) x Investment (INV)
#**********************************************************************************************#
runQuery = False
ffFreq = 'A'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'BM', 'INV'], ['ME', 'BM', 'OP', 'INV']
ff_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 32 portfolios (2x4x4) sorted on ['ME', 'BM', 'INV']
sortingDim = [2, 4, 4]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
#**********************************************************************************************#
#***********       Size (ME) x Operating Profitability (OP) x Investment (INV)       **********#
#**********************************************************************************************#
#**********************************************************************************************#

#**********************************************************************************************#
# Monthly Portfolios Formed on Size (ME) x Operating Profitability (OP) x Investment (INV)
#**********************************************************************************************#
runQuery = True
ffFreq = 'M'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'OP', 'INV'], ['ME', 'BM', 'OP', 'INV']
ff_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 32 portfolios (2x4x4) sorted on ['ME', 'OP', 'INV']
sortingDim = [2, 4, 4]
_, _, _, = ff_M.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_M.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_M.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_M.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_M.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)


#%%
#**********************************************************************************************#
# Annual Portfolios Formed on Size (ME) x Operating Profitability (OP) x Investment (INV)
#**********************************************************************************************#
runQuery = False
ffFreq = 'A'
ffFactors, ffsortCharac, ffportCharac = [], ['ME', 'OP', 'INV'], ['ME', 'BM', 'OP', 'INV']
ff_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# - 32 portfolios (2x4x4) sorted on ['ME', 'OP', 'INV']
sortingDim = [2, 4, 4]
_, _, _, = ff_A.comparePortfolios('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
_, _, _, = ff_A.comparePortfolios('NumFirms', ffFreq, startDate, endDate, sortingDim)
_, _, _, = ff_A.comparePortfolios('Characs',  ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Returns',  ffFreq, startDate, endDate, sortingDim, 'vw')
ff_A.getFamaFrenchStats('NumFirms', ffFreq, startDate, endDate, sortingDim)
ff_A.getFamaFrenchStats('Characs',  ffFreq, startDate, endDate, sortingDim)