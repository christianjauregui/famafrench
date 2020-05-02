"""
This file is part of famafrench.
Copyright (c) 2020, Christian Jauregui <chris.jauregui@berkeley.edu>
See file LICENSE.txt for license information.

Filename
________
`examples/famafrench_priorreturnsfactors.py`

Construct Fama/French Factors based on Prior Returns:
* Momentum: prior (2-12) returns (MOM)
* Short-Term Reversal: prior (1-1) returns (ST_Rev)
* Long-Term Reversal: prior (13-60) returns (LT_Rev)

Ken French online library:
Momentum
________
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_mom_factor.html
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_mom_factor_daily.html

Short-Term Reversal
___________________
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_st_rev_factor.html
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_st_rev_factor_daily.html

Long-Term Reversal
__________________
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_lt_rev_factor.html
https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_lt_rev_factor_daily.html

"""
import os
import datetime as dt
import famafrench.famafrench as ff

startDate = dt.date(1960, 1, 1)  # "default" startDate
endDate = dt.date.today()  # "default" endDate
#startDate = dt.date(1970, 1, 1)
#endDate = dt.date(2019, 12, 31)

ffsortCharac = ['ME', 'PRIOR_2_12']
ffFactors = ['MKT-RF', 'MOM', 'ST_Rev', 'LT_Rev']
ffportCharac = ['ME', 'PRIOR_2_12', 'PRIOR_1_1', 'PRIOR_13_60']

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

# Compare daily Fama-French factors based on prior returns constructed here to those provided in Ken French's online library
portTableD = ff_D.getFFfactors(startDate, endDate)
kfportTableD = ff_D.getkfFFfactors(ffFreq, startDate, endDate)
_, _, _, = ff_D.comparePortfolios('Factors', ffFreq, startDate, endDate)


#%%
#********************************************************************************************#
# Example 2: monthly sample
#********************************************************************************************#
runQuery = True
ffFreq = 'M'
ff_M = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# Summary statistics
ff_M.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)

# Compare monthly Fama-French factors based on prior returns constructed here to those provided in Ken French's online library
portTableM = ff_M.getFFfactors(startDate, endDate)
kfportTableM = ff_M.getkfFFfactors(ffFreq, startDate, endDate)
_, _, _, = ff_M.comparePortfolios('Factors', ffFreq, startDate, endDate)


#%%
#********************************************************************************************#
# Example 3: annual sample
#********************************************************************************************#
runQuery = False
ffFreq = 'A'
ff_A = ff.FamaFrench(pickled_dir, runQuery, ffFreq, ffsortCharac, ffFactors, ffportCharac)

# Summary statistics
ff_A.getFamaFrenchStats('Factors', ffFreq, startDate, endDate)

# Compare annual Fama-French factors based on prior returns constructed here to those provided in Ken French's online library
_, _, _, = ff_A.comparePortfolios('Factors', ffFreq, startDate, endDate)




