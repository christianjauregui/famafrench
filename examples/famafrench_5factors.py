"""
This file is part of famafrench.
Copyright (c) 2020, Christian Jauregui <chris.jauregui@berkeley.edu>
See file LICENSE.txt for license information.

Filename
_________
`examples/famafrench_5factors.py`

Construct Fama/French 5 Factors:
* Market premium
* Small Minus Big (SMB)
* High Minus Low (HML)
* Robust Minus Weak (RMW)
* Conservative Minus Aggressive (CMA)

Ken French online library:
Fama/French 5 Factors (2x3)
___________________________
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/f-f_5_factors_2x3.html

"""
import os
import datetime as dt
import famafrench.famafrench as ff

startDate = dt.date(1960, 1, 1)  # "default" startDate
endDate = dt.date.today()  # "default" endDate
#startDate = dt.date(1970, 1, 1)
#endDate = dt.date(2019, 12, 31)

ffsortCharac = ['ME', 'BM']
ffFactors = ['MKT-RF', 'SMB', 'HML', 'RMW', 'CMA']
ffportCharac = ['ME', 'BM', 'OP', 'INV']

# pickled_dir
pickled_dir = os.getcwd() + '/famafrench/pickled_db/'

#%%
#********************************************************************************************#
# Example 1: daily sample
#********************************************************************************************#
runQuery = True
ffFreq = 'D'
ff_D = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# Summary statistics
ff_D.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)

# Compare daily Fama-French 5 factors constructed here to those provided in Ken French's online library
portTableD = ff_D.getFFfactors(startDate, endDate)
kfportTableD = ff_D.getkfFFfactors(ffFreq, startDate, endDate)
_, _, _, = ff_D.comparePortfolios('Factors', ffFreq, startDate, endDate)


#%%
#********************************************************************************************#
# Example 2: weekly sample
#********************************************************************************************#
runQuery = False
ffFreq = 'W'
ff_W = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# Summary statistics
portTableW = ff_W.getFFfactors(startDate, endDate)
ff_W.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)


#%%
#********************************************************************************************#
# Example 3: monthly sample
#********************************************************************************************#
runQuery = True
ffFreq = 'M'
ff_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# Summary statistics
ff_M.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)

# Compare monthly Fama-French 5 factors constructed here to those provided in Ken French's online library
portTableM = ff_M.getFFfactors(startDate, endDate)
kfportTableM = ff_M.getkfFFfactors(ffFreq, startDate, endDate)
_, _, _, = ff_M.comparePortfolios('Factors', ffFreq, startDate, endDate)


#%%
#********************************************************************************************#
# Example 4: annual sample
#********************************************************************************************#
runQuery = False
ffFreq = 'A'
ff_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# Summary statistics
ff_A.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)

# Compare annual Fama-French 5 factors constructed here to those provided in Ken French's online library
portTableA = ff_A.getFFfactors(startDate, endDate)
kfportTableA = ff_A.getkfFFfactors(ffFreq, startDate, endDate)
_, _, _, = ff_A.comparePortfolios('Factors', ffFreq, startDate, endDate)





