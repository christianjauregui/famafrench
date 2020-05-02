"""
This file is part of famafrench.
Copyright (c) 2020, Christian Jauregui <chris.jauregui@berkeley.edu>
See file LICENSE.txt for license information.

Filename
_________
`famafrench/famafrench.py`

Descriptions
____________
Error
    General error validation object class
FamaFrench
    Object parent class w/ methods and attributes needed for constructing Fama-French-style
    portfolio returns, anomaly-based factors, and portfolio anomaly characteristics.
"""

__author__ = 'Christian Jauregui <chris.jauregui@berkeley.edu'
__all__ = ["Error", "FamaFrench"]

# Standard Imports
import os
import errno
import pickle
import copy
import sqlalchemy

import pandas as pd
import numpy as np
import pandas_datareader.data as web
import pandas_market_calendars as mcal

from pathlib import Path
from termcolor import cprint
from re import sub, compile
from dateutil.relativedelta import relativedelta
from pandas_datareader._utils import RemoteDataError
from pandas.tseries.offsets import *
from importlib import reload
from tqdm import tqdm
from dotenv import load_dotenv
from famafrench import wrdsconnect as wrds
from famafrench import utils # import 'utils' module w/ auxilary functions

nyse_cal = mcal.get_calendar('NYSE')
np.seterr(divide='raise')  # warn/error if taking np.log() if non-positive number.
pd.options.mode.chained_assignment = 'raise'
pd.options.mode.use_inf_as_na = True

# Reloads the .env file in your home directory.
load_dotenv()
reload(wrds)

# Establish remote connection to wrds-cloud using user-defined class adjusted from the 'WRDS-Py' library
if 'wrdsConn' in locals():
    print("wrds-cloud connection already open!")
else:
    wrdsConn = wrds.wrdsConnection()


# Declare 'Error" object child class for error validation
class Error(Exception):
    __doc__ = """
    General-purpose error validation class.
    
    Note
    ____
    This class is not documented in the main (online) documentation since it is sparingly used 
    and because it is an auxiliary class.
    """

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


# Declare 'FamaFrench' object parent class
class FamaFrench:
    __doc__ = """
    Class providing tools for constructing and replicating datasets from 
    `Ken French's online library <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>`_ 
    via queries to CRSP, Compustat Fundamentals Annual, and other sources accessed through 
    `wrds-cloud <https://wrds-www.wharton.upenn.edu/>`_.   
        
    Attributes
    -----------  
    pickled_dir : str
        Absolute path directory where pickled datasets will be saved.     
    runQuery: bool
        Flag for choosing whether to query datafiles from `wrds-cloud <https://wrds-www.wharton.upenn.edu/>`_ or import locally-pickled files. 
    freqType: str 
        Observation frequency of the portfolios. Possible choices are    
            
            * ``D`` : daily
            * ``W`` : weekly
            * ``M`` : monthly
            * ``Q`` : quarterly (3-months)
            * ``A`` : annual
    sortCharacsId: list, str
        Names of the anomaly characteristics used for portfolio sorting. The list will contain one, two, or three elements. 
        The order of the elements matters and should be consistent w/ the orders presented in 
        `Ken French's online library <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>`_. 
        Possible choices are:
            
            * ``ME`` : Size
            * ``BE`` : Book equity
            * ``BM`` : Book-to-Market equity
            * ``OP`` : Operating Profitability
            * ``INV`` : Investment
            * ``EP`` : Earnings/Price
            * ``CFP`` : Cashflow/Price
            * ``DP`` : Dividend Yield (i.e. Dividends/Price)
            * ``PRIOR_2_12`` : Prior (2-12) Returns
            * ``PRIOR_1_1`` : Prior (1-1) Returns
            * ``PRIOR_60_13`` : Prior (13-60) Returns
            * ``AC`` : Accruals
            * ``BETA`` : Market Beta (estimated using the Scholes-Williams (1977) methodology)
            * ``VAR`` : Variance (Daily and calculated using last 60 days (w/ 20 minimum)
            * ``RESVAR`` : Fama-French Three-factor model Residual Variance  (Daily and calculated using last 60 days (w/ 20 minimum)
            * ``NI`` : Net Share Issues  
    factorsId: None or list, str
        Names of the anomaly/risk-based factors following Fama and French (1992, 1993, 2008, 2015, 2017). 
        Possible choices are:
        
            * ``MKT-RF`` : Market premium
            * ``SMB`` : Small Minus Big
            * ``HML`` : High Minus Low
            * ``RMW`` : Robust Minus Weak
            * ``RMWc`` : Cash-based Robust Minus Weak (**Todo**)
            * ``CMA`` : Conservative Minus Aggressive
            * ``MOM`` : Momentum - based on Prior (2-12) returns
            * ``ST_Rev`` : Short-Term Reversal - based on Prior (1-1) returns
            * ``LT_Rev`` : Long-Term Reversal - based on Prior (13-60) returns
    mainCharacsId: None or list, str,  default None
         Names of the anomaly characteristics computed as averages for each portfolio bucket and constructed using the list ``sortCharacsId``.
         If *None*, ``mainCharacsI`` is set to the list ``sortCharacsId``.
    runEstimation: bool, default False
        Flag for choosing whether to run any estimation procedures for the first time/re-estimate procedures 
        by querying `wrds-cloud <https://wrds-www.wharton.upenn.edu/>`_ datafiles
        `or` import locally-pickled files storing existing estimates.   
    runFactorReg : bool, default True
        Flag for initializing the estimation of market beta's and/or rolling residual variances required 
        for sorting portfolios on ``BETA`` and/or ``RESVAR``. 
        This boolean is set internally - no need for user to specify it externally. 

    """
    # Constructor for the 'FamaFrench' object parent class
    def __init__(self, pickled_dir, runQuery, freqType, sortCharacsId, factorsId, mainCharacsId=None, runEstimation=False):
        """
        Constructor for the 'FamaFrench' object parent class
        """
        self.freqType = freqType
        self.sortCharacsId = sortCharacsId
        if mainCharacsId is None:
            self.mainCharacsId = self.sortCharacsId
        else:
            self.mainCharacsId = mainCharacsId
        self.factorsId = factorsId

        # NOTE: The following is required if 'BETA', 'RESVAR' are in the list 'sortCharacsId':
        # Initialize Boolean attribute needed to iteratively estimate market betas and/or residual variances:
        # NOTE: Need to set to 'True' when running an object's methods more than ONCE!
        self.runFactorReg = True

        # NOTE: A "temporary" list of the factor variables is created for special cases in which all
        # the Fama-French 3 or 5 factors are needed in estimation or output results.
        self.factorsIdtemp = copy.deepcopy(factorsId)

        # NOTE: The following boolean attributes are needed if the user wants to query directly from wrds-cloud
        # instead of using locally saved files to pickle or if the user wants to re-estimate factor regressions,
        # when applicable.
        self.runQuery = runQuery
        self.runEstimation = runEstimation

        # Pickled datasets are saved in the directory w/ a specific absolute path:
        for subdir in ['', 'daily/', 'monthly/', 'weekly/', 'quarterly/', 'annual/']:
            if not os.path.exists(os.path.dirname(pickled_dir + subdir)):
                try:
                    os.makedirs(os.path.dirname(pickled_dir + subdir))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise
        self.pickled_dir = pickled_dir


    @utils.lru_cached_method(maxsize=32)
    def queryComp(self, dt_start, dt_end):
        """
        Query Compustat Fundamentals Annual files from `wrds-cloud`.

        Parameters
        ___________
        dt_start: datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end: datetime.date
            Ending date for the dataset queried or locally retrieved.

        Returns
        ________
        dfcomp: pandas.DataFrame
            Dataset containing Compustat data cleaned from `wrds-cloud` queries.
        dfcomp_list: list, str
            Names of the anomaly portfolio characteristics computed from Compustat Fundamentals Annual.

        Note
        ____
        Following `Fama and French <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/variable_definitions.html>`_:

            *  `Book Equity` is calculated as follows: `book value of stockholders’ equity`
               + `balance sheet deferred taxes and investment tax credit (if available)`
               - `the book value of preferred stock`.
               Depending on availability, use the redemption, liquidation, or par value
               (in that order) to estimate the `book value of preferred stock` **ps**.

            *  `Stockholders’ equity` is the value reported by Moody’s or Compustat, if it is available.
               If not, measure `book value of stockholders’ equity` as the book value of common equity
               plus the par value of preferred stock, or the book value of assets minus total liabilities (in that order).

            * We must flag for number of years in Compustat (less than two years are likely backfilled data)

        Note
        ____
        List of Compustat Fundamentals Annual (XpressFeed) variables:

            - **gvkey**    : Unique permanent identifier assigned by Compustat at the company-level
            - **datadate** : Reporting date for data record
            - **indfmt**   : Item used to identify whether a company reports in a "Financial Services" or "Industrial" format
            - **datafmt**  : Item indicating how the company's data is collected and presented
            - **popsrc**   : Item indicating whether source of the data is domestic or international
            - **consol**   : Item used to identify whether a company's financials represent consolidate or nonconsolidated information
            - **at**       : Total Assets
            - **lt**       : Total Liabilities
            - **ceq**      : Total Common/Ordinary Equity = [Common/Ordinary Stock (Capital) + Capital Surplus/Share Premium Reserve + Retained Earnings - Total Treasury Stock (All Capital)] (= **cstk** + **caps** + **re** - **tstk**)
            - **seq**      : Parent's Stockholders Equity (= **ceq** + **pstk**)
            - **pstkrv**   : Redemption Value of Preferred Stock
            - **pstkl**    : Liquidating Value of Preferred Stock
            - **pstk**     : Total Preferred/Preference Stock (Capital) = [Redeemable Preferred/Preference Stock + Nonredeemable Preferred/Preference Stock] (= **pstkr** + **pstkn**)
            - **txdb**     : Deferred Taxes (Balance Sheet)
            - **itcb**     : Investment Tax Credit (Balance Sheet)
            - **txditc**   : Deferred Taxes and Investment Tax Credit (= **txdb** + **itcb**)
            - **revt**     : Total Revenue
            - **cogs**     : Cost of Goods Sold
            - **xint**     : Total Interest and Related Expense
            - **xsga**     : Selling, General and Administrative Expense
            - **mib**      : Non-controlling/Minority Interest (Balance Sheet)
            - **ib**       : Income Before Extraordinary Items
            - **txdi**     : Deferred Income Taxes
            - **dp**       : Depreciation and Amortization
            - **chso**     : Common Shares Outstanding
            - **adjex_f**  : Fiscal-Year, Cumulative Adjustment Factor by Ex-Date
            - **act**      : Total Current Assets
            - **lct**      : Total Current Liabilities
            - **che**      : Cash and Short-Term Investments
            - **dlc**      : Total Debt in Current Liabilities

        Note
        ______
        Depending on a user's WRDS subscription, data variables will be queried from the most frequently updated
        Compustat datafiles. Compustat offers daily, monthly, and annually updated files for annual observations.
        The **default** datafiles are updated monthly. See `wrds-cloud` SAS Library Names below:

            - ``compd`` : dataset `Compustat - NA, Bank, Global - Daily Update`
            - ``compm`` : dataset `Compustat - NA - Monthly Update`
            - ``compa`` : dataset `Compustat - NA - Annual Update`
            - ``comp`` : **default** dataset `Compustat - NA, Bank, Global, Execucomp - Monthly Update`

        """
        startdate, enddate = dt_start.strftime('%m/%d/%Y'), dt_end.strftime('%m/%d/%Y')

        def get_comp_sqlQuery(wrds_update, start_date, end_date):
            """
            Create SQL query string for Compustat Fundamentals Annual datafiles.

            Parameters
            ___________
            wrds_update : str
            start_date : datetime.date
            end_date : datetime.date

            Returns
            ________
            comp_sqlQuery : str
            """
            if wrds_update == 'daily':
                compdb = 'compd.funda'
            elif wrds_update == 'monthly':
                compdb = 'compm.funda'
            elif wrds_update == '':
                compdb = 'comp.funda'
            else:
                compdb = 'compa.funda'
            comp_sql = {'compDb': compdb,
                        'compIndFmt': '\'INDL\'',
                        'compDataFmt': '\'STD\'',
                        'compStartDate': '\'' + start_date + '\'',
                        'compEndDate': '\'' + end_date + '\''}

            comp_sqlQuery = """
                             SELECT gvkey, EXTRACT(YEAR FROM datadate) AS year, datadate, fyear, 
                             at, lt, ceq, seq, pstkrv, pstkl, pstk, txdb, itcb, txditc, 
                             revt, cogs, xint, xsga, mib, ib, txdi, dp AS depr, csho, adjex_f, act, lct, che, dlc
                                FROM {0}
                                WHERE indfmt = {1}
                                AND datafmt = {2}
                                AND popsrc ='D'
                                AND consol ='C'
                                AND datadate BETWEEN {3} AND {4}
                            """.format(comp_sql['compDb'],
                                       comp_sql['compIndFmt'],
                                       comp_sql['compDataFmt'],
                                       comp_sql['compStartDate'],
                                       comp_sql['compEndDate'])
            return comp_sqlQuery

        # Load local file if it exists (and dates can be found), else query from wrds-cloud.
        comp_file = Path(self.pickled_dir + 'annual/comp_annual.pickle')
        if self.runQuery is False and comp_file.is_file():
            file_to_pickle = open(comp_file, 'rb')
            dfcomp = pickle.load(file_to_pickle)
            file_to_pickle.close()
            date_min, date_max = dfcomp['datadate'].min(), dfcomp['datadate'].max()
            year_min, year_max = int(dfcomp['year'].min()), int(dfcomp['year'].max())
            if (dt_start.year < year_min) | (year_max < dt_end.year):
                cprint('Compustat (annual) dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...', 'grey', 'on_white')

                # Query missing observations BEFORE 'year_min' and append to locally saved copy.
                if dt_start.year < year_min:
                    enddate = date_min.strftime('%m/%d/%Y')
                    try:
                        dfcomp_pre = wrdsConn.raw_sql(sqlquery=get_comp_sqlQuery('daily', startdate, enddate))
                    except sqlalchemy.exc.ProgrammingError:
                        try:
                            dfcomp_pre = wrdsConn.raw_sql(sqlquery=get_comp_sqlQuery('monthly', startdate, enddate))
                        except sqlalchemy.exc.ProgrammingError:
                            try:
                                dfcomp_pre = wrdsConn.raw_sql(sqlquery=get_comp_sqlQuery('', startdate, enddate))
                            except sqlalchemy.exc.ProgrammingError:
                                dfcomp_pre = wrdsConn.raw_sql(sqlquery=get_comp_sqlQuery('annual', startdate, enddate))

                    dfcomp = dfcomp[(dfcomp['year'] <= dt_end.year)]
                    dfcomp = dfcomp_pre.append(dfcomp, ignore_index=True)
                    dfcomp = dfcomp.sort_values(by=['gvkey', 'datadate'], ascending=[1, 1]).drop_duplicates(keep='first').reset_index(drop=True)
                    file_to_pickle = open(comp_file, 'wb')
                    pickle.dump(dfcomp, file_to_pickle)
                    file_to_pickle.close()

                    # Delete pandas.DataFrame no longer needed in memory.
                    lst = [dfcomp_pre]
                    del dfcomp_pre
                    del lst
                # Query missing observations AFTER 'year_max' and append to locally saved copy.
                if year_max < dt_end.year:
                    startdate = date_max.strftime('%m/%d/%Y')
                    enddate = dt_end.strftime('%m/%d/%Y')
                    try:
                        dfcomp_post = wrdsConn.raw_sql(sqlquery=get_comp_sqlQuery('daily', startdate, enddate))
                    except sqlalchemy.exc.ProgrammingError:
                        try:
                            dfcomp_post = wrdsConn.raw_sql(sqlquery=get_comp_sqlQuery('monthly', startdate, enddate))
                        except sqlalchemy.exc.ProgrammingError:
                            try:
                                dfcomp_post = wrdsConn.raw_sql(sqlquery=get_comp_sqlQuery('', startdate, enddate))
                            except sqlalchemy.exc.ProgrammingError:
                                dfcomp_post = wrdsConn.raw_sql(sqlquery=get_comp_sqlQuery('annual', startdate, enddate))

                    dfcomp = dfcomp[(dt_start.year <= dfcomp['year'])]
                    dfcomp = dfcomp.append(dfcomp_post, ignore_index=True)
                    dfcomp = dfcomp.sort_values(by=['gvkey', 'datadate'], ascending=[1, 1]).drop_duplicates(
                        keep='first').reset_index(drop=True)
                    file_to_pickle = open(comp_file, 'wb')
                    pickle.dump(dfcomp, file_to_pickle)
                    file_to_pickle.close()

                    # Delete pandas.DataFrame no longer needed in memory.
                    lst = [dfcomp_post]
                    del dfcomp_post
                    del lst
            else:
                cprint('Compustat (annual) dataset currently saved locally w/ required dates.', 'grey', 'on_cyan')
                dfcomp = dfcomp[(dt_start.year <= dfcomp['year']) & (dfcomp['year'] <= dt_end.year)]
        else:
            cprint('Compustat (annual) dataset currently NOT saved locally. Querying from wrds-cloud...', 'grey', 'on_white')
            try:
                dfcomp = wrdsConn.raw_sql(sqlquery=get_comp_sqlQuery('daily', startdate, enddate))
            except sqlalchemy.exc.ProgrammingError:
                try:
                    dfcomp = wrdsConn.raw_sql(sqlquery=get_comp_sqlQuery('monthly', startdate, enddate))
                except sqlalchemy.exc.ProgrammingError:
                    try:
                        dfcomp = wrdsConn.raw_sql(sqlquery=get_comp_sqlQuery('', startdate, enddate))
                    except sqlalchemy.exc.ProgrammingError:
                        dfcomp = wrdsConn.raw_sql(sqlquery=get_comp_sqlQuery('annual', startdate, enddate))
            file_to_pickle = open(comp_file, 'wb')
            pickle.dump(dfcomp, file_to_pickle)
            file_to_pickle.close()

        # Replace any Python objects 'None' to np.nan
        dfcomp = dfcomp.fillna(value=np.nan)

        # Get datetime objects...
        dfcomp['datadate'] = pd.to_datetime(dfcomp['datadate'])

        dfcomp_list = []
        if utils.any_in(['BE', 'BM', 'OP', 'AC'], set(self.sortCharacsId).union(set(self.mainCharacsId))) \
                or utils.any_in(['SMB', 'HML', 'RMW'], set(self.factorsId).union(set(self.factorsIdtemp))):
            # Create "preferred stock" - 'ps' - according to Fama and French (1993);
            # SOURCE: http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/variable_definitions.html
            dfcomp['ps'] = np.where(dfcomp['pstkrv'].isnull(), dfcomp['pstkl'], dfcomp['pstkrv'])
            dfcomp['ps'] = np.where(dfcomp['ps'].isnull(), dfcomp['pstk'], dfcomp['ps'])
            dfcomp['ps'] = np.where(dfcomp['ps'].isnull(), 0, dfcomp['ps'])

            # Create "deferred taxes and investment tax credit" - 'dtaxes_ic':
            dfcomp['dtaxes_ic'] = np.where(dfcomp['txditc'].isnull(), dfcomp['txdb'].fillna(0) + dfcomp['itcb'].fillna(0), dfcomp['txditc'])
            dfcomp['dtaxes_ic'] = np.where(dfcomp['dtaxes_ic'].isnull(), 0, dfcomp['dtaxes_ic'])

            # Create "book equity" - 'be' - following Fama and French (1993):
            # SOURCE: http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/variable_definitions.html
            dfcomp['bseq'] = np.where(dfcomp['seq'].isnull(), dfcomp['ceq'] + dfcomp['pstk'].fillna(0), dfcomp['seq'])
            dfcomp['bseq'] = np.where(dfcomp['bseq'].isnull(), dfcomp['at'] - dfcomp['lt'], dfcomp['bseq'])

            # NOTE: Because of changes in the treatment of deferred taxes described in FASB 109,
            #       files produced by Ken French after August 2016 no longer add
            #       Deferred Taxes and Investment Tax Credit to 'be' for fiscal years ending in 1993 or later.
            dfcomp['be'] = np.where((dfcomp['fyear'] < 1993), dfcomp['bseq'] + dfcomp['dtaxes_ic'] - dfcomp['ps'], dfcomp['bseq'] - dfcomp['ps'])
            dfcomp['be'] = np.where(dfcomp['be'] > 0, dfcomp['be'], np.nan)
            dfcomp_list.append('be')

        if ('OP' in set(self.sortCharacsId).union(set(self.mainCharacsId))) or (utils.any_in(['RMW', 'CMA'], set(self.factorsId).union(set(self.factorsIdtemp)))):
            # Create "operating profitability" - 'op' - following Fama and French (2015):
            # SOURCE: http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/variable_definitions.html
            # NOTE: 'op' uses annual revenues minus costs of goods 'cogs', interest expense 'xint', as well as
            #        selling, and general, and administrative expenses 'xsga' at the end of fiscal year {t-1}
            #        divided by (book equity 'be' at the end of fiscal year {t-1}
            #        plus minority interest 'mib' at the end of fiscal year {t-1})
            dfcomp['xp_allnan'] = (dfcomp['cogs'].isnull()) & (dfcomp['xsga'].isnull()) & (dfcomp['xint'].isnull())
            dfcomp['profit'] = dfcomp['revt'] - dfcomp['cogs'].fillna(0) - dfcomp['xint'].fillna(0) - dfcomp['xsga'].fillna(0)
            dfcomp['op'] = dfcomp['profit'] / (dfcomp['be'] + dfcomp['mib'].fillna(0))
            dfcomp['op'] = np.where((dfcomp['be'] > 0) & (~dfcomp['op'].isnull()) & (~dfcomp['revt'].isnull()) & (~dfcomp['xp_allnan']), dfcomp['op'], np.nan)

            # NOTE: Compustat data yields gross outliers in 'op' w/ ratios as large as '1,000'.
            #       To be consistent w/ summary statistics for characteristics provided by Ken French's online library,
            #       values for 'op' outside the 99th percentile are set to missing.
            dfcomp['op'] = np.where((dfcomp['op'] <= dfcomp['op'].quantile(0.99)), dfcomp['op'], np.nan)
            dfcomp_list.append('op')
            dfcomp_list.append('revt')
            dfcomp_list.append('xp_allnan')

        if ('INV' in set(self.sortCharacsId).union(set(self.mainCharacsId))) or (utils.any_in(['RMW', 'CMA'], set(self.factorsId).union(set(self.factorsIdtemp)))):
            # Create "asset growth (i.e. investment)" - 'inv' following Fama and French (2015):
            # SOURCE: http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/variable_definitions.html
            try:
                dfcomp['inv'] = np.log(dfcomp['at']) - np.log(dfcomp.groupby(['gvkey'])['at'].shift(1))
            except FloatingPointError:
                dfcomp['inv'] = (dfcomp['at'] / dfcomp.groupby(['gvkey'])['at'].shift(1)) - 1

            dfcomp['inv'] = np.where(~dfcomp['inv'].isnull(), dfcomp['inv'], np.nan)
            # NOTE: Compustat data yields gross outliers in 'inv' w/ percentages as low as '-100%' and as large as '10,000%'.
            #       These outliers are pervasive on the left tail of the distribution.
            #       To be consistent w/ summary statistics for characteristics provided by Ken French's online library,
            #       values for 'inv' outside [15th, 99th] percentiles are winsorized.
            dfcomp['inv'] = np.where((dfcomp['inv'].quantile(0.15) <= dfcomp['inv']), dfcomp['inv'], dfcomp['inv'].quantile(0.15))
            dfcomp['inv'] = np.where((dfcomp['inv'] <= dfcomp['inv'].quantile(0.99)), dfcomp['inv'], dfcomp['inv'].quantile(0.99))
            dfcomp_list.append('inv')

        if 'EP' in set(self.sortCharacsId).union(set(self.mainCharacsId)):
            dfcomp['ib'] = np.where(~dfcomp['ib'].isnull(), dfcomp['ib'], np.nan)
            dfcomp_list.append('ib')  # 'ib' is income before taxes or "earnings"

        if 'CFP' in set(self.sortCharacsId).union(set(self.mainCharacsId)):
            # Create "cash flow" - 'cf' - following Fama and French (2015):
            # SOURCE: http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/variable_definitions.html
            dfcomp['cf'] = dfcomp['ib'] + dfcomp['txdi'].fillna(0) + dfcomp['depr'].fillna(0)
            dfcomp['cf'] = np.where(~dfcomp['cf'].isnull(), dfcomp['cf'], np.nan)
            dfcomp_list.append('cf')

        if 'AC' in set(self.sortCharacsId).union(set(self.mainCharacsId)):
            # Create "accruals" - 'ac' - following Fama and French (2015):
            # SOURCE: http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/variable_definitions.html
            dfcomp['csho_adj'] = np.where(((dfcomp['csho'] * dfcomp['adjex_f']) > 0), (dfcomp['csho'] * dfcomp['adjex_f']), np.nan)
            dfcomp['owcap_adj'] = ((dfcomp['act'] - dfcomp['che']) - (dfcomp['lct'].fillna(0) - dfcomp['dlc'].fillna(0))) / dfcomp['csho_adj']
            dfcomp['d_owcap_adj'] = (dfcomp['owcap_adj'] - dfcomp.groupby(['gvkey'])['owcap_adj'].shift(1))
            dfcomp_list.append('d_owcap_adj')
            dfcomp_list.append('csho_adj')

        if 'NI' in set(self.sortCharacsId).union(set(self.mainCharacsId)):
            # Create "net income shares" - 'ni' - following Fama and French (2015):
            # SOURCE: http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/variable_definitions.html
            dfcomp['ni_csho_adj'] = np.where(((dfcomp['csho'] * dfcomp['adjex_f']) > 0), (dfcomp['csho'] * dfcomp['adjex_f']), np.nan)
            try:
                dfcomp['ni'] = np.log(dfcomp['ni_csho_adj']) - np.log(dfcomp.groupby(['gvkey'])['ni_csho_adj'].shift(1))
            except FloatingPointError:
                dfcomp['ni'] = (dfcomp['ni_csho_adj'] / dfcomp.groupby(['gvkey'])['ni_csho_adj'].shift(1)) - 1
            dfcomp['ni'] = np.where(~dfcomp['ni'].isnull(), dfcomp['ni'], np.nan)
            # NOTE: Compustat data yields outliers in 'ni' w/ ratios as large as '20'.
            #       To be consistent w/ summary statistics for characteristics provided by Ken French's online library,
            #       values for 'ni' outside the 99.9th percentile are set to missing.
            dfcomp['ni'] = np.where((dfcomp['ni'] <= dfcomp['ni'].quantile(0.999)), dfcomp['ni'], np.nan)
            dfcomp_list.append('ni')

        # Obtain the number of years in Compustat:
        dfcomp['count'] = dfcomp.groupby(['gvkey']).cumcount()

        # Sub-select required 'dfcomp' columns:
        dfcomp = dfcomp[['gvkey', 'year', 'datadate', 'count'] + dfcomp_list]
        return dfcomp, dfcomp_list


    @utils.lru_cached_method(maxsize=32)
    def queryCrsp(self, freq, dt_start, dt_end):
        """
        Query CRSP Stock/Security files from `wrds-cloud`.

        Parameters
        ___________
        freq : str
            Observation frequency. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.

        Returns
        ________
        dfcrsp : pandas.DataFrame
            Cleaned CRSP data queried from `wrds-cloud` w/ observations at frequency ``freq`` over sample period from ``dt_start`` to ``dt_end``.

        Note
        ______
        List of queried CRSP variables:

            - **permno**   : Unique permanent identifier assigned by CRSP at the security-level
            - **permco**   : Unique permanent identifier assigned by CRSP at the company-level
            - **date**     : Trading day
            - **shrcd**    : 2-digit code describing the type of shares traded
            - **exchcd**   : Code indicating the exchange on which security is listed
            - **ret**      : Holding period return w dividends
            - **retx**     : Holding period return w/out dividends
            - **shrout**   : Number of publicly held shares (thousands)
            - **prc**      : Closing price or negative bid/ask average for a trading day

        Note
        ______
        Depending on a user's WRDS subscription, data variables will be queried from the most frequently updated
        CRSP datafiles. CRSP offers monthly, quarterly, and annually updated files for both daily and monthly observations.
        The **default** datafiles are updated annually. See `wrds-cloud` SAS Library Names below:

            - ``crspm`` : dataset `CRSP Monthly Update`
            - ``crspq`` : dataset `CRSP Quarterly Update`
            - ``crspa`` : **default** dataset `CRSP Annual Update`

        """
        if freq in ['D', 'W']:
            freqTypeFull = 'daily'
        elif freq in ['M', 'Q', 'A']:
            freqTypeFull = 'monthly'
        else:
            raise ValueError('frequency is not a standard type.\n'
                             'Please specify one of the following: \'D\', \'W\', \'M\', \'Q\', or \'A\'')

        # Since monthly observations have a date ending on the last day of each month, then for any 'dt_start' that doesn't
        # coincide w/ the last day of any month, we adjust it so it does and the query pulls the monthly observation of interest.
        if freq in ['M', 'Q', 'A']:
            if dt_start != (dt_start + MonthEnd(0)).date():
                dt_start = (dt_start + MonthEnd(0)).date()
            if dt_end != (dt_end + MonthEnd(0)).date():
                dt_end = (dt_end + MonthEnd(0)).date()
        startdate, enddate = dt_start.strftime('%m/%d/%Y'), dt_end.strftime('%m/%d/%Y')

        def get_crsp_sqlQuery(wrds_update, freqTypeFullstr, start_date, end_date):
            """
            Create SQL query string for CRSP stock datafiles.

            Parameters
            ___________
            wrds_update : str
            freqTypeFullstr : str
            start_date : datetime.date
            end_date : datetime.date

            Returns
            ________
            crsp_sqlQuery : str
            """
            if wrds_update == 'monthly':
                crspdb = 'crspm.' + freqTypeFullstr[0] + 'sf'
                crspnames = 'crspm.' + freqTypeFullstr[0] + 'senames'
            elif wrds_update == 'quarterly':
                crspdb = 'crspq.' + freqTypeFullstr[0] + 'sf'
                crspnames = 'crspq.' + freqTypeFullstr[0] + 'senames'
            else:
                crspdb = 'crspa.' + freqTypeFullstr[0] + 'sf'
                crspnames = 'crspa.' + freqTypeFullstr[0] + 'senames'
            crsp_sql = {'crspDb': crspdb,
                        'crspNames': crspnames,
                        'crspStartDate': '\'' + start_date + '\'',
                        'crspEndDate': '\'' + end_date + '\''}

            crsp_sqlQuery = """
                            SELECT CAST(a.permno AS INT), CAST(a.permco AS INT), a.date, CAST(b.shrcd AS INT), 
                            CAST(b.exchcd AS INT), a.ret, a.retx, a.shrout, a.prc
                                FROM {0} AS a
                                LEFT JOIN {1} AS b
                                ON a.permno = b.permno
                                AND b.namedt <= a.date
                                AND a.date <= b.nameendt
                                WHERE a.date BETWEEN {2} AND {3}
                                AND b.exchcd BETWEEN 1 AND 3
                            """.format(crsp_sql['crspDb'],
                                       crsp_sql['crspNames'],
                                       crsp_sql['crspStartDate'],
                                       crsp_sql['crspEndDate'])
            return crsp_sqlQuery

        # Load local file if it exists (and dates can be found), else query from wrds-cloud.
        crsp_file = Path(self.pickled_dir + freqTypeFull + '/crsp_' + freqTypeFull + '.pickle')
        if self.runQuery is False and crsp_file.is_file():
            file_to_pickle = open(crsp_file, 'rb')
            dfcrsp = pickle.load(file_to_pickle)
            file_to_pickle.close()
            date_min, date_max = dfcrsp['date'].min(), dfcrsp['date'].max()
            if (dt_start < date_min) | (date_max < dt_end):
                cprint('CRSP (' + freqTypeFull + ') dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...', 'grey', 'on_white')

                # Query missing observations BEFORE 'date_min' and append to locally saved copy.
                if dt_start < date_min:
                    enddate = date_min.strftime('%m/%d/%Y')
                    try:
                        dfcrsp_pre = wrdsConn.raw_sql(sqlquery=get_crsp_sqlQuery('monthly', freqTypeFull, startdate, enddate))
                    except sqlalchemy.exc.ProgrammingError:
                        try:
                            dfcrsp_pre = wrdsConn.raw_sql(
                                sqlquery=get_crsp_sqlQuery('quarterly', freqTypeFull, startdate, enddate))
                        except sqlalchemy.exc.ProgrammingError:
                            dfcrsp_pre = wrdsConn.raw_sql(sqlquery=get_crsp_sqlQuery('annual', freqTypeFull, startdate, enddate))
                    dfcrsp = dfcrsp[(dfcrsp['date'] <= dt_end)]
                    dfcrsp = dfcrsp_pre.append(dfcrsp, ignore_index=True)
                    dfcrsp = dfcrsp.sort_values(by=['permno', 'date'], ascending=[1, 1]).drop_duplicates(keep='first').reset_index(drop=True)
                    file_to_pickle = open(crsp_file, 'wb')
                    pickle.dump(dfcrsp, file_to_pickle)
                    file_to_pickle.close()

                    # Delete pandas.DataFrame no longer needed in memory.
                    lst = [dfcrsp_pre]
                    del dfcrsp_pre
                    del lst
                # Query missing observations AFTER 'date_max' and append to locally saved copy.
                if date_max < dt_end:
                    startdate = date_max.strftime('%m/%d/%Y')
                    enddate = dt_end.strftime('%m/%d/%Y')
                    try:
                        dfcrsp_post = wrdsConn.raw_sql(sqlquery=get_crsp_sqlQuery('monthly', freqTypeFull, startdate, enddate))
                    except sqlalchemy.exc.ProgrammingError:
                        try:
                            dfcrsp_post = wrdsConn.raw_sql(sqlquery=get_crsp_sqlQuery('quarterly', freqTypeFull, startdate, enddate))
                        except sqlalchemy.exc.ProgrammingError:
                            dfcrsp_post = wrdsConn.raw_sql(sqlquery=get_crsp_sqlQuery('annual', freqTypeFull, startdate, enddate))
                    dfcrsp = dfcrsp[(dt_start <= dfcrsp['date'])]
                    dfcrsp = dfcrsp.append(dfcrsp_post, ignore_index=True)
                    dfcrsp = dfcrsp.sort_values(by=['permno', 'date'], ascending=[1, 1]).drop_duplicates(keep='first').reset_index(drop=True)
                    file_to_pickle = open(crsp_file, 'wb')
                    pickle.dump(dfcrsp, file_to_pickle)
                    file_to_pickle.close()

                    # Delete pandas.DataFrame no longer needed in memory.
                    lst = [dfcrsp_post]
                    del dfcrsp_post
                    del lst
            else:
                cprint('CRSP (' + freqTypeFull + ') dataset currently saved locally w/ required dates.', 'grey', 'on_cyan')
                dfcrsp = dfcrsp[(dt_start <= dfcrsp['date']) & (dfcrsp['date'] <= dt_end)]
        else:
            cprint('CRSP (' + freqTypeFull + ') dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...', 'grey', 'on_white')
            try:
                dfcrsp = wrdsConn.raw_sql(sqlquery=get_crsp_sqlQuery('monthly', freqTypeFull, startdate, enddate))
            except sqlalchemy.exc.ProgrammingError:
                try:
                    dfcrsp = wrdsConn.raw_sql(sqlquery=get_crsp_sqlQuery('quarterly', freqTypeFull, startdate, enddate))
                except sqlalchemy.exc.ProgrammingError:
                    dfcrsp = wrdsConn.raw_sql(sqlquery=get_crsp_sqlQuery('annual', freqTypeFull, startdate, enddate))
            file_to_pickle = open(crsp_file, 'wb')
            pickle.dump(dfcrsp, file_to_pickle)
            file_to_pickle.close()

        # Get datetime objects...
        dfcrsp['date'] = pd.to_datetime(dfcrsp['date'])
        dfcrsp = dfcrsp.rename(columns={'date': 'date_crsp'})

        # Convert trading dates to end-of-month, if 'freq' does not pertain to daily or weekly frequency.
        if freq in ['D', 'W']:
            dfcrsp.insert(dfcrsp.columns.get_loc('shrcd'), 'date', dfcrsp['date_crsp'])
        elif freq in ['M', 'Q', 'A']:
            dfcrsp.insert(dfcrsp.columns.get_loc('shrcd'), 'date', dfcrsp['date_crsp'] + MonthEnd(0))
        else:
            raise ValueError('frequency is not a standard type.\n'
                             'Please specify one of the following: \'D\', \'W\', \'M\', \'Q\', or \'A\'')
        dfcrsp = dfcrsp.drop(columns=['date_crsp'])
        return dfcrsp



    @utils.lru_cached_method(maxsize=32)
    def queryCrspdlret(self, freq, dt_start, dt_end):
        """
        Query CRSP's Stock Event - Delisting files on `wrds-cloud`.

        Parameters
        ___________
        freq : str
            Observation frequency. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.

        Returns
        ________
        dfcrsp_full : pandas.DataFrame
            Dataset constructed by merging CRSP stock/security dataset w/
            CRSP delisted returns information.

        Note
        ______
        List of queried CRSP Delisting variables:

            - **permno**   : Unique permanent identifier assigned by CRSP at the security-level
            - **dlret**    : Return (w/ dividends) of the security after being delisted
            - **dlretx**   : Return (w/out dividends) of the security after being delisted
            - **dlstdt**   : 3-digit integer code indicating whether security is still trading or the specific reason why it was delisted.
        Note
        ______
        Depending on a user's WRDS subscription, delisted data variables will be queried from the most frequently updated
        CRSP datafiles. CRSP offers monthly, quarterly, and annually updated files for daily observations.
        The **default** datafiles are updated annually. See `wrds-cloud` SAS Library Names below:

            - ``crspm`` : dataset `CRSP Monthly Update`
            - ``crspq`` : dataset `CRSP Quarterly Update`
            - ``crspa`` : **default** dataset `CRSP Annual Update`

        """
        dfcrsp = self.queryCrsp(freq, dt_start, dt_end)

        if freq in ['D', 'W']:
            freqTypeFull = 'daily'
        else:
            freqTypeFull = 'monthly'

        def get_crspdlret_sqlQuery(wrds_update, freqType):
            """
            Create SQL query string for CRSP delisted datafiles.

            Parameters
            ___________
            wrds_update : str
            freqType : str
            crspdlret_sqlQuery: str

            Returns
            ________
            crspdlret_sqlQuery : str
            """
            if freqType in ['D', 'W']:
                freqTypeFull = 'daily'
            else:
                freqTypeFull = 'monthly'

            if wrds_update == 'monthly':
                crspdb = 'crspm.' + freqTypeFull[0] + 'sedelist'
            elif wrds_update == 'quarterly':
                crspdb = 'crspq.' + freqTypeFull[0] + 'sedelist'
            else:
                crspdb = 'crspa.' + freqTypeFull[0] + 'sedelist'
            crspdlret_sqlQuery = """
                                SELECT CAST(permno AS INT), dlret, dlretx, dlstdt 
                                    FROM {0}
                                """.format(crspdb)
            return crspdlret_sqlQuery

        # Load local file if it exists (and dates can be found), else query from wrds-cloud.
        crspdlret_file = Path(self.pickled_dir + freqTypeFull + '/crspdelist_' + freqTypeFull + '.pickle')
        if self.runQuery is False and crspdlret_file.is_file():
            file_to_pickle = open(crspdlret_file, 'rb')
            dfcrspdlret = pickle.load(file_to_pickle)
            file_to_pickle.close()
            date_min, date_max = dfcrspdlret['dlstdt'].min(), dfcrspdlret['dlstdt'].max()
            if (dt_start < date_min) | (date_max < dt_end):
                cprint('CRSP delisted returns (' + freqTypeFull + ') dataset currently NOT saved locally w/ required dates. '
                                                                  'Querying from wrds-cloud...', 'grey', 'on_white')
                try:
                    dfcrspdlret = wrdsConn.raw_sql(sqlquery=get_crspdlret_sqlQuery('monthly', freq))
                except sqlalchemy.exc.ProgrammingError:
                    try:
                        dfcrspdlret = wrdsConn.raw_sql(sqlquery=get_crspdlret_sqlQuery('quarterly', freq))
                    except sqlalchemy.exc.ProgrammingError:
                        dfcrspdlret = wrdsConn.raw_sql(sqlquery=get_crspdlret_sqlQuery('annual', freq))
                file_to_pickle = open(crspdlret_file, 'wb')
                pickle.dump(dfcrspdlret, file_to_pickle)
                file_to_pickle.close()
            else:
                cprint('CRSP delisted returns (' + freqTypeFull + ') dataset currently saved locally w/ required dates.', 'grey', 'on_cyan')
                dfcrspdlret = dfcrspdlret[(dt_start <= dfcrspdlret['dlstdt']) & (dfcrspdlret['dlstdt'] <= dt_end)]
        else:
            cprint('CRSP delisted returns (' + freqTypeFull + ') dataset currently NOT saved locally. Querying from wrds-cloud...', 'grey', 'on_white')
            try:
                dfcrspdlret = wrdsConn.raw_sql(sqlquery=get_crspdlret_sqlQuery('monthly', freq))
            except sqlalchemy.exc.ProgrammingError:
                try:
                    dfcrspdlret = wrdsConn.raw_sql(sqlquery=get_crspdlret_sqlQuery('quarterly', freq))
                except sqlalchemy.exc.ProgrammingError:
                    dfcrspdlret = wrdsConn.raw_sql(sqlquery=get_crspdlret_sqlQuery('annual', freq))
            file_to_pickle = open(crspdlret_file, 'wb')
            pickle.dump(dfcrspdlret, file_to_pickle)
            file_to_pickle.close()

        # Get datetime objects...
        dfcrspdlret['dlstdt'] = pd.to_datetime(dfcrspdlret['dlstdt'])

        # Convert trading dates to end-of-period, if 'freq' does not pertain to daily or weekly frequency.
        dfcrspdlret = dfcrspdlret.dropna(axis=0, how='any')
        if freq in ['D', 'W']:
            dfcrspdlret['date'] = dfcrspdlret['dlstdt']
        elif freq in ['M', 'Q', 'A']:
            dfcrspdlret['date'] = dfcrspdlret['dlstdt'] + MonthEnd(0)
        else:
            raise ValueError('frequency is not a standard type.\n '
                             'Please specify one of the following: \'D\', \'W\', \'M\', \'Q\', or \'A\'')

        # Merge CRSP stock returns w/ CRSP delisted returns.
        dfcrsp_full = dfcrsp.merge(right=dfcrspdlret, how='left', on=['permno', 'date'])
        if 'DP' in set(self.sortCharacsId).union(set(self.mainCharacsId)):
            dfcrsp_full[['dlret', 'dlretx', 'ret', 'retx']] = dfcrsp_full[['dlret', 'dlretx', 'ret', 'retx']].fillna(0)

            # Returns (w/ and w/out dividends) adjusted for delisting.
            dfcrsp_full.insert(dfcrsp_full.columns.get_loc('ret'), 'retadj', ((1 + dfcrsp_full['ret']) * (1 + dfcrsp_full['dlret'])) - 1)
            dfcrsp_full.insert(dfcrsp_full.columns.get_loc('retx'), 'retadjx', ((1 + dfcrsp_full['retx']) * (1 + dfcrsp_full['dlretx'])) - 1)
            dfcrsp_cols = ['dlret', 'dlretx', 'dlstdt', 'shrout']
        else:
            dfcrsp_full[['dlret', 'ret']] = dfcrsp_full[['dlret', 'ret']].fillna(0)

            # Returns (w/ dividends) adjusted for delisting.
            dfcrsp_full.insert(dfcrsp_full.columns.get_loc('ret'), 'retadj', ((1 + dfcrsp_full['ret']) * (1 + dfcrsp_full['dlret'])) - 1)
            dfcrsp_cols = ['dlret', 'dlstdt', 'shrout']

        # Calculate market value of equity 'me'.
        dfcrsp_full['me'] = dfcrsp_full['prc'].abs() * dfcrsp_full['shrout']
        dfcrsp_full = dfcrsp_full.drop(columns=dfcrsp_cols).sort_values(by=['date', 'permco', 'me'])
        return dfcrsp_full



    @utils.lru_cached_method(maxsize=32)
    def queryrf1m(self, freq, dt_start, dt_end):
        """
        Query the risk-free interest rate (ie 1-month Treasury Bill rate) from `wrds-cloud`.
        The risk-free interest rate is compounded to higher frequencies when needed.

        Parameters
        ___________
        freq : str
            Observation frequency. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start: datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end: datetime.date
            Ending date for the dataset queried or locally retrieved.

        Returns
        ________
        rf1m : pandas.DataFrame
            Cleaned dataset w/ time-series of the risk-free interest rate (ie 1-month Treasury Bill rate)
            used in the construction of the Market Premium.

        """
        if freq == 'D':
            freqTypeFulldir, freqTypeFull = 'daily', 'daily'
        elif freq == 'W':
            freqTypeFulldir, freqTypeFull = 'weekly', 'daily'
        elif freq == 'M':
            freqTypeFulldir, freqTypeFull = 'monthly', 'monthly'
        elif freq == 'Q':
            freqTypeFulldir, freqTypeFull = 'quarterly', 'monthly'
        elif freq == 'A':
            freqTypeFulldir, freqTypeFull = 'annual', 'monthly'
        else:
            raise ValueError('frequency is not a standard type.\n'
                             'Please specify one of the following: \'D\', \'W\', \'M\', \'Q\', or \'A\'')

        # Since monthly observations have a date starting on the 1st of each month, then for any 'dt_start' that doesn't
        # coincide w/ the 1st of any month, we adjust it so it does and the query pulls the monthly observation of interest.
        if freq in ['M', 'Q', 'A'] and dt_start != (dt_start + MonthBegin(-1)).date():
            dt_start = (dt_start + MonthBegin(-1)).date()
        startdate, enddate = dt_start.strftime('%m/%d/%Y'), dt_end.strftime('%m/%d/%Y')

        def get_rf1m_sqlQuery(freqType, start_date, end_date):
            """
            Create SQL query string for the risk-free interest rate (ie 1-month Treasury Bill rate)

            Parameters
            ___________
            freqType : str
            start_date : datetime.date
            end_date : datetime.date

            Returns
            ________
            rf1m_sqlQuery : str
            """
            if freqType in ['D', 'W']:
                freqTypeFull = 'daily'
            else:
                freqTypeFull = 'monthly'

            # SQL script text depends on frequency
            if freqType == 'D':
                diff_sql = 'EXTRACT(DAY FROM LEAD(date) OVER (ORDER BY date)) - EXTRACT(DAY FROM date) AS diff'
                freq_sql = 'rf AS cumrf'
            elif freqType == 'W':
                diff_sql = 'EXTRACT(WEEK FROM LEAD(date) OVER (ORDER BY date)) - EXTRACT(WEEK FROM date) AS diff'
                freq_sql = 'EXP(SUM(LN(1 + rf)) OVER (PARTITION BY EXTRACT(YEAR FROM date), EXTRACT(WEEK FROM date))) - 1 AS cumrf'
            elif freqType == 'M':
                diff_sql = 'EXTRACT(MONTH FROM LEAD(date) OVER (ORDER BY date)) - EXTRACT(MONTH FROM date) AS diff'
                freq_sql = 'rf AS cumrf'
            elif freqType == 'Q':
                diff_sql = 'EXTRACT(QUARTER FROM LEAD(date) OVER (ORDER BY date)) - EXTRACT(QUARTER FROM date) AS diff'
                freq_sql = 'EXP(SUM(LN(1 + rf)) OVER (PARTITION BY EXTRACT(YEAR FROM date), EXTRACT(QUARTER FROM date))) - 1 AS cumrf'
            else:
                diff_sql = 'EXTRACT(YEAR FROM LEAD(date) OVER (ORDER BY date)) - EXTRACT(YEAR FROM date) AS diff'
                freq_sql = 'EXP(SUM(LN(1 + rf)) OVER (PARTITION BY EXTRACT(YEAR FROM date))) - 1 AS cumrf'

            rf1m_sql = {'rf1mDiff': diff_sql,
                        'rf1mFreq': freq_sql,
                        'rf1mDb': 'factors_' + freqTypeFull,
                        'rf1mDbStartDate': '\'' + start_date + '\'',
                        'rf1mDbEndDate': '\'' + end_date + '\''}

            rf1m_sqlQuery = """
                            SELECT date_crsp, cumrf
                                FROM                 
                                (SELECT date AS date_crsp, {0}, rf, {1}                
                                    FROM {2} 
                                    WHERE date BETWEEN {3} AND {4}
                                ) as crsp_cumrf
                                WHERE diff!=0 OR diff is NULL
                            """.format(rf1m_sql['rf1mDiff'],
                                       rf1m_sql['rf1mFreq'],
                                       rf1m_sql['rf1mDb'],
                                       rf1m_sql['rf1mDbStartDate'],
                                       rf1m_sql['rf1mDbEndDate'])
            return rf1m_sqlQuery

        # Load local file if it exists (and dates can be found), else query from wrds-cloud.
        rf1m_file = Path(self.pickled_dir + freqTypeFulldir + '/rf1m_' + freqTypeFulldir + '.pickle')
        if self.runQuery is False and rf1m_file.is_file():
            file_to_pickle = open(rf1m_file, 'rb')
            rf1m = pickle.load(file_to_pickle)
            file_to_pickle.close()
            date_min, date_max = rf1m['date_crsp'].min(), rf1m['date_crsp'].max()
            if (dt_start < date_min) | (date_max < dt_end):
                cprint('Historical risk-free interest rate (' + freqTypeFulldir + ') dataset currently NOT saved locally w/ required dates. '
                                                                               'Querying from wrds-cloud...', 'grey', 'on_white')

                # Query missing observations BEFORE 'date_min' and append to locally saved copy.
                if dt_start < date_min:
                    enddate = date_min.strftime('%m/%d/%Y')
                    rf1m_pre = wrdsConn.raw_sql(sqlquery=get_rf1m_sqlQuery(freq, startdate, enddate))

                    rf1m = rf1m[(rf1m['date_crsp'] <= dt_end)]
                    rf1m = rf1m_pre.append(rf1m, ignore_index=True)
                    rf1m = rf1m.sort_values(by=['date_crsp'], ascending=[1]).drop_duplicates(subset=['date_crsp'], keep='first').reset_index(drop=True)
                    file_to_pickle = open(rf1m_file, 'wb')
                    pickle.dump(rf1m, file_to_pickle)
                    file_to_pickle.close()

                    # Delete pandas.DataFrame no longer needed in memory
                    lst = [rf1m_pre]
                    del rf1m_pre
                    del lst
                # Query missing observations AFTER 'date_max' and append to locally saved copy.
                if date_max < dt_end:
                    startdate = date_max.strftime('%m/%d/%Y')
                    enddate = dt_end.strftime('%m/%d/%Y')
                    rf1m_post = wrdsConn.raw_sql(sqlquery=get_rf1m_sqlQuery(freq, startdate, enddate))

                    rf1m = rf1m[(dt_start <= rf1m['date_crsp'])]
                    rf1m = rf1m.append(rf1m_post, ignore_index=True)
                    rf1m = rf1m.sort_values(by=['date_crsp'], ascending=[1]).drop_duplicates(subset=['date_crsp'], keep='first').reset_index(drop=True)
                    file_to_pickle = open(rf1m_file, 'wb')
                    pickle.dump(rf1m, file_to_pickle)
                    file_to_pickle.close()

                    # Delete pandas.DataFrame no longer needed in memory.
                    lst = [rf1m_post]
                    del rf1m_post
                    del lst
            else:
                cprint('Historical risk-free interest rate (' + freqTypeFulldir + ') dataset currently saved locally w/ required dates.', 'grey', 'on_cyan')
                rf1m = rf1m[(dt_start <= rf1m['date_crsp']) & (rf1m['date_crsp'] <= dt_end)]
        else:
            cprint('Historical risk-free interest rate (' + freqTypeFulldir + ') dataset currently NOT saved locally. Querying from wrds-cloud...', 'grey', 'on_white')
            rf1m = wrdsConn.raw_sql(sqlquery=get_rf1m_sqlQuery(freq, startdate, enddate))
            file_to_pickle = open(rf1m_file, 'wb')
            pickle.dump(rf1m, file_to_pickle)
            file_to_pickle.close()

        # Convert trading dates to end-of-period if 'freq' does not pertain to daily or weekly frequency.
        if freq in ['D', 'W']:
            rf1m.insert(rf1m.columns.get_loc('date_crsp'), 'date', rf1m['date_crsp'])
        elif freq == 'M':
            rf1m.insert(rf1m.columns.get_loc('date_crsp'), 'date', rf1m['date_crsp'] + MonthEnd(0))
        elif freq == 'Q':
            rf1m.insert(rf1m.columns.get_loc('date_crsp'), 'date', rf1m['date_crsp'] + QuarterEnd(0))
        elif freq == 'A':
            rf1m.insert(rf1m.columns.get_loc('date_crsp'), 'date', rf1m['date_crsp'] + YearEnd(0))
        else:
            raise ValueError('frequency is not a standard type.\n'
                             'Please specify one of the following: \'D\', \'W\', \'M\', \'Q\', or \'A\'')

        rf1m = rf1m.rename(columns={'cumrf': 'rf'})[['date', 'rf']]
        if freq == 'D':
            rf1m = rf1m[(pd.to_datetime(rf1m['date']).dt.weekday < 5)]
        if freq == 'W':
            # NOTE: Ken French's weekly datasets provide incorrect dates for some weeks prior to 1953.
            #       Specifically, some weeks end on a Saturday, instead of the correct trading weekday.
            #       An adjustment is made to correct for the error, assuming the only mistake is in the
            #       the weekly dates provided by Ken French and not how the daily returns are cumulated
            #       for the aforementioned weeks.
            rf1m.loc[:, 'date'] = np.where(pd.to_datetime(rf1m['date']).dt.day_name().isin(['Saturday', 'Sunday']), (rf1m['date'] - BDay(1)).dt.date, rf1m['date'])

            # NYSE trading day holiday calendar
            nyse_holidays = pd.DataFrame(nyse_cal.holidays().holidays, columns=['nyse_date'])
            nyse_holidays = nyse_holidays[(dt_start <= nyse_holidays['nyse_date'].dt.date) & (dt_end >= nyse_holidays['nyse_date'].dt.date)]['nyse_date'].dt.date.tolist()
            rf1m.loc[:, 'date'] = np.where(rf1m['date'].isin(nyse_holidays), (rf1m['date'] - BDay(1)).dt.date, rf1m['date'])
        if freq in ['M', 'Q', 'A']:
            rf1m.loc[:, 'date'] = rf1m['date'].dt.date
        rf1m.set_index('date', inplace=True)
        return rf1m



    @utils.lru_cached_method(maxsize=32)
    def getCrspDailyRollVar(self, roll_window, min_periods, freq, dt_start, dt_end):
        """
        Calculate rolling `daily` variance of stock returns for all CRSP stocks queried from `wrds-cloud`.

        Parameters
        ___________
        roll_window : int
            Fixed size of the rolling (moving) window.
            This is the number of observations used for calculating the realized `daily` variance.
            Similar to parameter ``window`` in `pandas` method :meth:`pandas.DataFrame.rolling`.
        min_periods : int
            Minimum number of observations in each window necessary to have an estimated value.
            Similar to parameter ``min_periods`` in `pandas` method :meth:`pandas.DataFrame.rolling`.
        freq : str
            Observation frequency. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.

        Returns
        ________
        dfcrsprollvar : pandas.DataFrame
            Dataset w/ panel of rolling `daily` variances calculated using ``roll_window`` days of lagged returns (w/ minimum of ``min_periods`` days).

        Note
        ______
        For a short description of how Fama and French construct portfolios formed on the variance of daily returns, see
        `Detail for Portfolios Formed Monthly on Variance <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/Data_Library/det_port_form_VAR.html>`_.

        Note
        ______
        Depending on a user's WRDS subscription, data variables will be queried from the most frequently updated
        CRSP datafiles. CRSP offers monthly, quarterly, and annually updated files for daily observations.
        The **default** datafiles are updated annually. See `wrds-cloud` SAS Library Names below:

            - ``crspm`` : dataset `CRSP Monthly Update`
            - ``crspq`` : dataset `CRSP Quarterly Update`
            - ``crspa`` : **default** dataset `CRSP Annual Update`

        """
        if freq in ['D', 'W']:
            freqTypeFull = 'daily'
        elif freq in ['M', 'Q', 'A']:
            freqTypeFull = 'monthly'
        else:
            raise ValueError('frequency is not a standard type.\n'
                             'Please specify one of the following: \'D\', \'W\', \'M\', \'Q\', or \'A\'')

        # Need to query AT A MINIMUM (minus) -'roll_window' days before 'dt_start' so we have a non-missing observation for 'dt_start':
        dt_start = (dt_start - Day(roll_window)).date()
        startdate, enddate = dt_start.strftime('%m/%d/%Y'), dt_end.strftime('%m/%d/%Y')

        def get_crsprollvar_sqlQuery(wrds_update, freqType, roll_win, min_per, start_date, end_date):
            """
            Create SQL query string for calculating rolling daily variances from CRSP stock datafiles.
            
            Parameters
            ___________            
            wrds_update : str
            freqType : str
            roll_win : int
            min_per : int
            start_date : datetime.date
            end_date : datetime.date

            Returns
            ________
            crsprollvar_sqlQuery : str
            """
            if freqType in ['D', 'W']:
                diff_sql = ''
                diff_filter = ''
            else:
                diff_sql = 'EXTRACT(MONTH FROM LEAD(a.date) OVER (PARTITION BY a.permno ORDER BY a.date)) - EXTRACT(MONTH FROM a.date) AS mdiff,'
                diff_filter = 'AND (mdiff!=0 OR mdiff is NULL)'

            if wrds_update == 'monthly':
                crspdb = 'crspm.dsf'
                crspnames = 'crspm.dsenames'
            elif wrds_update == 'quarterly':
                crspdb = 'crspq.dsf'
                crspnames = 'crspq.dsenames'
            else:
                crspdb = 'crspa.dsf'
                crspnames = 'crspa.dsenames'
            crsprollvar_sql = {'window': '\'' + str(roll_win - 1) + '\'',
                               'min_periods': '\'' + str(min_per) + '\'',
                               'crspDb': crspdb,
                               'crspNames': crspnames,
                               'crspStartDate': '\'' + start_date + '\'',
                               'crspEndDate': '\'' + end_date + '\'',
                               'crspDiff': diff_sql,
                               'crspDiffFilter': diff_filter}

            # Calculate the rolling daily variance (by permno) within SQL query.
            crsprollvar_sqlQuery = """
                                SELECT permno, date, ret_rollvar
                                    FROM
                                    (SELECT CAST(a.permno AS INT), a.date, {0}
                                    ROW_NUMBER() OVER (PARTITION BY a.permno ORDER BY a.date) AS obs_count, a.ret,                      
                                    VARIANCE(a.ret) OVER (PARTITION BY a.permno ORDER BY a.date 
                                    ROWS BETWEEN {1} PRECEDING AND CURRENT ROW) AS ret_rollvar
                                    FROM {2} AS a
                                    LEFT JOIN {3} AS b
                                    ON a.permno = b.permno
                                    AND b.namedt <= a.date
                                    AND a.date <= b.nameendt
                                    WHERE a.date BETWEEN {4} AND {5}
                                    AND b.exchcd BETWEEN 1 AND 3
                                    AND b.shrcd BETWEEN 10 AND 11
                                    ORDER BY a.permno ASC, a.date ASC
                                    ) AS retrollVar
                                    WHERE obs_count >= {6} {7}
                                """.format(crsprollvar_sql['crspDiff'],
                                           crsprollvar_sql['window'],
                                           crsprollvar_sql['crspDb'],
                                           crsprollvar_sql['crspNames'],
                                           crsprollvar_sql['crspStartDate'],
                                           crsprollvar_sql['crspEndDate'],
                                           crsprollvar_sql['min_periods'],
                                           crsprollvar_sql['crspDiffFilter'])
            return crsprollvar_sqlQuery

        # Load local file if it exists (and dates can be found), else query from wrds-cloud.
        crsprollvar_file = Path(self.pickled_dir + freqTypeFull + '/crsprollvar_' + freqTypeFull + '.pickle')
        if self.runQuery is False and crsprollvar_file.is_file():
            file_to_pickle = open(crsprollvar_file, 'rb')
            dfcrsprollvar = pickle.load(file_to_pickle)
            file_to_pickle.close()
            date_min, date_max = dfcrsprollvar['date'].min(), dfcrsprollvar['date'].max()
            print('VAR period', dt_start, date_min, ' ', date_max, dt_end)
            if (dt_start < date_min) | (date_max < dt_end):
                cprint('CRSP rolling daily variance dataset currently NOT saved locally w/ required dates. Querying from wrds-cloud...', 'grey', 'on_white')

                # Query missing observations BEFORE 'date_min' and append to locally saved copy.
                if dt_start < date_min:
                    # Force an overlap of 'roll_window' days so observations WITHIN 'roll_window' days of 'date_min' are not
                    # constructed using less than 'roll_window' days as a result of an artificially truncated sample.
                    date_min = (date_min + Day(roll_window)).date()
                    enddate = date_min.strftime('%m/%d/%Y')
                    try:
                        dfcrsprollvar_pre = wrdsConn.raw_sql(sqlquery=get_crsprollvar_sqlQuery('monthly', freq, roll_window, min_periods, startdate, enddate))
                    except sqlalchemy.exc.ProgrammingError:
                        try:
                            dfcrsprollvar_pre = wrdsConn.raw_sql(sqlquery=get_crsprollvar_sqlQuery('quarterly', freq, roll_window,
                                                                                                   min_periods, startdate, enddate))
                        except sqlalchemy.exc.ProgrammingError:
                            dfcrsprollvar_pre = wrdsConn.raw_sql(sqlquery=get_crsprollvar_sqlQuery('annual', freq, roll_window, min_periods, startdate, enddate))
                    dfcrsprollvar_pre.insert(0, 'id', 0)

                    dfcrsprollvar = dfcrsprollvar[(dfcrsprollvar['date'] <= dt_end)]
                    dfcrsprollvar.insert(0, 'id', 1)

                    dfcrsprollvar = dfcrsprollvar_pre.append(dfcrsprollvar, ignore_index=True)
                    dfcrsprollvar = dfcrsprollvar.sort_values(by=['permno', 'date', 'id'], ascending=[1, 1, 1])
                    dfcrsprollvar = dfcrsprollvar.drop_duplicates(subset=['permno', 'date'], keep='first').reset_index(drop=True)
                    dfcrsprollvar = dfcrsprollvar.drop(columns=['id'])
                    file_to_pickle = open(crsprollvar_file, 'wb')
                    pickle.dump(dfcrsprollvar, file_to_pickle)
                    file_to_pickle.close()

                    # Delete pandas.DataFrame no longer needed in memory.
                    lst = [dfcrsprollvar_pre]
                    del dfcrsprollvar_pre
                    del lst
                # Query missing observations AFTER 'date_max' and append to locally saved copy.
                if date_max < dt_end:
                    # Force an overlap of 'roll_window' days so observations WITHIN 'roll_window' days of 'date_max' are not
                    # constructed using less than 'roll_window' days as a result of an artificially truncated sample.
                    date_max = (date_max - Day(2 * roll_window)).date()
                    startdate = date_max.strftime('%m/%d/%Y')
                    enddate = dt_end.strftime('%m/%d/%Y')
                    try:
                        dfcrsprollvar_post = wrdsConn.raw_sql(sqlquery=get_crsprollvar_sqlQuery('monthly', freq, roll_window, min_periods, startdate, enddate))
                    except sqlalchemy.exc.ProgrammingError:
                        try:
                            dfcrsprollvar_post = wrdsConn.raw_sql(sqlquery=get_crsprollvar_sqlQuery('quarterly', freq, roll_window, min_periods, startdate,
                                                                  enddate))
                        except sqlalchemy.exc.ProgrammingError:
                            dfcrsprollvar_post = wrdsConn.raw_sql(sqlquery=get_crsprollvar_sqlQuery('annual', freq, roll_window, min_periods, startdate, enddate))
                    dfcrsprollvar_post.insert(0, 'id', 0)

                    dfcrsprollvar = dfcrsprollvar[(dt_start <= dfcrsprollvar['date'])]
                    dfcrsprollvar.insert(0, 'id', 1)

                    dfcrsprollvar = dfcrsprollvar.append(dfcrsprollvar_post, ignore_index=True)
                    dfcrsprollvar = dfcrsprollvar.sort_values(by=['permno', 'date', 'id'], ascending=[1, 1, 1])
                    dfcrsprollvar = dfcrsprollvar.drop_duplicates(subset=['permno', 'date'], keep='last').reset_index(drop=True)
                    dfcrsprollvar = dfcrsprollvar.drop(columns=['id'])
                    file_to_pickle = open(crsprollvar_file, 'wb')
                    pickle.dump(dfcrsprollvar, file_to_pickle)
                    file_to_pickle.close()

                    # Delete pandas.DataFrame no longer needed in memory.
                    lst = [dfcrsprollvar_post]
                    del dfcrsprollvar_post
                    del lst
            else:
                cprint('CRSP rolling daily variance dataset currently saved locally w/ required dates.', 'grey', 'on_cyan')
                dfcrsprollvar = dfcrsprollvar[(dt_start <= dfcrsprollvar['date']) & (dfcrsprollvar['date'] <= dt_end)]
        else:
            cprint('CRSP rolling daily variance dataset currently NOT saved locally. Querying from wrds-cloud...', 'grey', 'on_white')
            try:
                dfcrsprollvar = wrdsConn.raw_sql(sqlquery=get_crsprollvar_sqlQuery('monthly', freq, roll_window, min_periods, startdate, enddate))
            except sqlalchemy.exc.ProgrammingError:
                try:
                    dfcrsprollvar = wrdsConn.raw_sql(sqlquery=get_crsprollvar_sqlQuery('quarterly', freq, roll_window, min_periods, startdate, enddate))
                except sqlalchemy.exc.ProgrammingError:
                    dfcrsprollvar = wrdsConn.raw_sql(sqlquery=get_crsprollvar_sqlQuery('annual', freq, roll_window, min_periods, startdate, enddate))
            file_to_pickle = open(crsprollvar_file, 'wb')
            pickle.dump(dfcrsprollvar, file_to_pickle)
            file_to_pickle.close()

        if freq in ['D', 'W']:
            dfcrsprollvar = dfcrsprollvar.rename(columns={'ret_rollvar': 'var'})
            dfcrsprollvar.loc[:, 'date'] = pd.to_datetime(dfcrsprollvar['date'])
        else:
            # Get end-of-month datetimes if 'freq' pertains to monthly, quarterly, or annual portfolios.
            dfcrsprollvar = dfcrsprollvar.rename(columns={'date': 'date_crsp', 'ret_rollvar': 'var'})
            dfcrsprollvar.insert(dfcrsprollvar.columns.get_loc('date_crsp'), 'date', pd.to_datetime(dfcrsprollvar['date_crsp']) + MonthEnd(0))
        dfcrsprollvar = dfcrsprollvar[['permno', 'date', 'var']]
        return dfcrsprollvar



    @utils.lru_cached_method(maxsize=32)
    def aggregateME(self, freq, dt_start, dt_end):
        """
        Aggregate market value of equity **me** for cases in which the same firm (ie single **permco** identifer) has
        two or more securities (ie multiple **permno** identifiers) for a given **date**.

        Parameters
        ___________
        freq : str
            Observation frequency. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.

        Returns
        ________
        dfcrsp2 : pandas.DataFrame
            Dataset containing single **permno** (by date) w/ the largest market value of equity **me**.

        Note
        ____
        For the purpose of constructing firm-level **me** it's crucial to aggregate **me** for each (**permco**, **date**) identifier pair.
        This **me** is assigned to the **permno** w/ the largest **me**.
        The approach followed here is similar to the one implemented in SAS found through `WRDS Research Applications
        <https://wrds-www.wharton.upenn.edu/pages/support/applications/risk-factors-and-industry-benchmarks/fama-french-factors/>`_.

        """
        dfcrsp_full = self.queryCrspdlret(freq, dt_start, dt_end)

        # Sum of market value of equity - 'me' - across different 'permno' belonging to same 'permco' for a given 'date'.
        dfcrsp_aggme = dfcrsp_full.groupby(['date', 'permco'])['me'].sum().reset_index()

        # Largest market value of equity - 'me' - within a 'permco' for a given 'date'.
        dfcrsp_maxme = dfcrsp_full.groupby(['date', 'permco'])['me'].max().reset_index()

        # Join by ('date', 'permco', 'me') to find the permno w/ 'me'=='maxme', then drop 'me' columns.
        dfcrsp1 = dfcrsp_full.merge(right=dfcrsp_maxme, how='inner', on=['date', 'permco', 'me']).drop(columns=['me'])

        # Join w/ 'dfcrsp_aggme' to get the correct market value of equity value.
        dfcrsp2 = dfcrsp1.merge(right=dfcrsp_aggme, how='inner', on=['date', 'permco'])

        # Sort by 'permno' and 'date'; drop duplicates.
        dfcrsp2 = dfcrsp2.sort_values(by=['permno', 'date']).drop_duplicates()

        # Return cleaned 'dfcrsp2' pandas.DataFrame.
        dfcrsp2.insert(dfcrsp2.columns.get_loc('shrcd'), 'year', dfcrsp2['date'].dt.year)
        return dfcrsp2



    @utils.lru_cached_method(maxsize=32)
    def getMEDec(self, freq, dt_start, dt_end):
        """
        Construct market value of equity **me** for Decemeber of every year.

        Parameters
        ___________
        freq : str
            Observation frequency. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.

        Returns
        ________
        me_dec : pandas.DataFrame
            Dataset w/ December market value of equity **me** for all **permno** identifiers in CRSP.

        Note
        ____
        Following Fama and French (1992, 1993), portfolios for July of year `t` to June of year `t+1` include all NYSE, AMEX, and
        NASDAQ stocks for which we have market value of equity **me** for December of year `t-1` and June of year `t`.

        Note
        ____
        Following the Fama and French methodology, **me** from December of year `t-1` is used to construct ``BM`` breakpoints,
        which are then used to form portfolios from July of year `t` to June of year `t+1`.

        Note
        ____
        The approach followed here is similar to the one implemented in SAS found through `WRDS Research Applications
        <https://wrds-www.wharton.upenn.edu/pages/support/applications/risk-factors-and-industry-benchmarks/fama-french-factors/>`_.

        """
        dfaggme = self.aggregateME(freq, dt_start, dt_end)
        me_dec = dfaggme[(dfaggme['date'].dt.month == 12)]
        # If frequency is daily or weekly, then December 'me' corresponds to the last observed 'me' in December.
        if freq in ['D', 'W']:
            me_dec_eom = me_dec.groupby(['permno', 'year'])['date'].max().reset_index().rename(columns={'date': 'date_eom'})
            me_dec = me_dec.merge(right=me_dec_eom, how='left', on=['permno', 'year'])
            me_dec = me_dec[me_dec['date'] == me_dec['date_eom']]
            me_dec.loc[:, 'date'] = me_dec['date'] + MonthEnd(0)

            # Delete pandas.DataFrame no longer needed in memory.
            lst = [me_dec_eom]
            del me_dec_eom
            del lst
        me_dec = me_dec[['permno', 'date', 'year', 'me']].rename(columns={'me': 'me_dec'})
        return me_dec



    @utils.lru_cached_method(maxsize=32)
    def getFactorRegResults(self, ffmodel, boolRVar, scholeswilliams, roll_window, min_per, freq, dt_start, dt_end):
        """
        Estimate factor-based quantities of risk (specifically, market betas) as well as residuals using rolling regressions.
        Rolling regressions require a fixed rolling window w/ a minimum number of observations within each window.

        Parameters
        ___________
        ffmodel : str
            Possible choices include:

                * ``capm`` : Market (CAPM) model

                    :math:`R_{t}^{i} - R_{t}^{f} = \\alpha _{i} + \\beta^{Mkt}_{i}\\left(R_{t}^{M}-R_{t}^{f}\\right) +\\varepsilon _{t}^{i}`

                * ``ff3`` : Fama-French 3 factor model

                    :math:`R_{t}^{i} - R_{t}^{f} = \\alpha _{i} + \\beta^{Mkt}_{i}\\left(R_{t}^{M}-R_{t}^{f}\\right) + \\beta^{SMB}_{i}R_{t}^{SMB} + \\beta^{HML}_{i}R_{t}^{HML} + \\varepsilon _{t}^{i}`
        boolRvar: bool
            Flag for choosing whether to calculate the variance of residuals (``boolRvar = True``)
            or the market betas estimated from a specified factor model ``ffmode`` (``boolRvar = False``).
        scholeswilliams: bool
            Flag for choosing whether to implement the Dimson (1979) methodology - based on Scholes-Williams (1977) -
            for estimating betas in the presence of infrequent trading. The methodology used here as well as in Fama-French (1993)
            estimates betas by summing coefficient estimates pertaining to lagged and coincident market return variables
            adjusted for auto-correlation of the market return variables:

            .. math::

                \widehat{\\beta^{Mkt}}_{t, Dimson} = \\frac{\\left(\widehat{\\beta^{Mkt}}_{t} + \widehat{\\beta^{Mkt}}_{t-1}\\right)}{\\left(1 + 2\widehat{\\rho}\\right)}

            * :math:`\widehat{\\beta^{Mkt}}_{t}` : OLS beta with the contemporaneous return of the market portfolio
            * :math:`\widehat{\\beta^{Mkt}}_{t-1}` : OLS beta with the return on the market portfolio lagged one period
            * :math:`\widehat{\\rho}` : First-order autocorrelation coefficient of the return on the market.

            Otherwise, factor market betas are estimated in the usual sense using coincident market return variables.

        roll_window: int
            Fixed size of the rolling (moving) window.
            This is the number of observations used for calculating the factor betas or the residual variances from factor models.
        min_per: int
             Minimum number of observations in each window necessary to have an estimated value.
        freq : str
            Observation frequency. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.

        Returns
        ________
        dfresVar, dfbeta : pandas.DataFrame
            Dataset containing the panel of market betas OR residual variances estimated from rolling regressions.

        Note
        ______
        This routine uses `Numba <https://numba.pydata.org/numba-doc/dev/index.html>`_, an opens-source `just-in-time (JIT)` compiler that translates a subset of Python and NumPy
        into fast machine code using the LLVM compiler written in C++.
        Using `Numba <https://numba.pydata.org/numba-doc/dev/index.html>`_ a gives us C++/Fortran-like speed when estimating the rolling regressions.
        More details in source code utilizing `Numba <https://numba.pydata.org/numba-doc/dev/index.html>`_.

        Todo
        ______
        Extend the `Dimson (1979) <https://www.sciencedirect.com/science/article/abs/pii/0304405X79900138>`_
        methodology based on `Scholes and Williams (1977) <https://www.sciencedirect.com/science/article/abs/pii/0304405X77900411>`_ to other factor quantities of risk
        beyond the `market (CAPM)` beta (eg, `SMB` and `HML` quantities of risk)

        References
        __________
        *   Scholes, Myron and Williams, Joseph. (1977). `Estimating betas from nonsynchronous data`,
            Journal of Financial Economics, (5)3, pp.309-327

        *   Dimson, Elroy. (1979). `Risk measurement when shares are subject to infrequent trading`,
            Journal of Financial Economics, (7)2, pp.197-226

        *   Fama, Eugene F., and Kenneth R. French. (1992). `The Cross-section of Expected Stock Returns`,
            Journal of Finance, 47(2), pp.427-465
        
        """
        # Numba imports (+ supression of Numba warnings)
        from numba import njit, prange, types, f8, b1, i8
        import warnings
        warnings.filterwarnings('ignore')

        # Load local file if it exists (and dates can be found), else query from wrds-cloud.
        if freq in ['D', 'W']:
            freqTypeFull = 'daily'
        elif freq in ['M', 'Q', 'A']:
            freqTypeFull = 'monthly'
        else:
            raise ValueError('frequency is not a standard type.\n'
                             'Please specify one of the following: \'D\', \'W\', \'M\', \'Q\', or \'A\'')

        # Need to query AT A MINIMUM (minus) -'roll_window' days before 'dt_start' so we have a non-missing estimation for 'dt_start':
        dt_start = (dt_start - Day(roll_window)).date()

        crsp_ret_file = Path(self.pickled_dir + freqTypeFull + '/crspretFactorReg_' + freqTypeFull + '.pickle')
        if self.runEstimation is False and crsp_ret_file.is_file():
            file_to_pickle = open(crsp_ret_file, 'rb')
            dfcrsp_ret = pickle.load(file_to_pickle)
            file_to_pickle.close()
            date_min, date_max = dfcrsp_ret['date'].dt.date.min(), dfcrsp_ret['date'].dt.date.max()
            if (dt_start < date_min) | (date_max < dt_end):
                cprint('Factor Regressions: CRSP return (' + freqTypeFull + ') dataset for factor regressions currently NOT saved locally w/ required dates. '
                                                                         '\n                    Querying from wrds-cloud...', 'grey', 'on_white')

                # Query missing observations BEFORE 'date_min' and append to locally saved copy.
                if dt_start < date_min:
                    dfcrsp_ret_pre = self.aggregateME(freq, dt_start, date_min)[['permno', 'date', 'retadj']]
                    dfcrsp_ret_pre.insert(0, 'id', 0)

                    dfcrsp_ret = dfcrsp_ret[(dfcrsp_ret['date'].dt.date <= dt_end)]
                    dfcrsp_ret.insert(0, 'id', 1)

                    dfcrsp_ret = dfcrsp_ret_pre.append(dfcrsp_ret, ignore_index=True)
                    dfcrsp_ret = dfcrsp_ret.sort_values(by=['permno', 'date', 'id'], ascending=[1, 1, 1])
                    dfcrsp_ret = dfcrsp_ret.drop_duplicates(subset=['permno', 'date'], keep='first').reset_index(drop=True)
                    dfcrsp_ret = dfcrsp_ret.drop(columns=['id'])
                    file_to_pickle = open(crsp_ret_file, 'wb')
                    pickle.dump(dfcrsp_ret, file_to_pickle)
                    file_to_pickle.close()

                    # Delete pandas.DataFrame no longer needed in memory
                    lst = [dfcrsp_ret_pre]
                    del dfcrsp_ret_pre
                    del lst
                # Query missing observations AFTER 'date_max' and append to locally saved copy
                if date_max < dt_end:
                    dfcrsp_ret_post = self.aggregateME(freq, date_max, dt_end)[['permno', 'date', 'retadj']]
                    dfcrsp_ret_post.insert(0, 'id', 0)

                    dfcrsp_ret = dfcrsp_ret[(dt_start <= dfcrsp_ret['date'].dt.date)]
                    dfcrsp_ret.insert(0, 'id', 1)

                    dfcrsp_ret = dfcrsp_ret.append(dfcrsp_ret_post, ignore_index=True)
                    dfcrsp_ret = dfcrsp_ret.sort_values(by=['permno', 'date', 'id'], ascending=[1, 1, 1])
                    dfcrsp_ret = dfcrsp_ret.drop_duplicates(subset=['permno', 'date'], keep='last').reset_index(drop=True)
                    dfcrsp_ret = dfcrsp_ret.drop(columns=['id'])
                    file_to_pickle = open(crsp_ret_file, 'wb')
                    pickle.dump(dfcrsp_ret, file_to_pickle)
                    file_to_pickle.close()

                    # Delete pandas.DataFrame no longer needed in memory.
                    lst = [dfcrsp_ret_post]
                    del dfcrsp_ret_post
                    del lst
            else:
                cprint('Factor Regressions: CRSP return (' + freqTypeFull + ') dataset for factor regressions currently saved locally w/ required dates.', 'grey', 'on_cyan')
                dfcrsp_ret = dfcrsp_ret[(dt_start <= dfcrsp_ret['date'].dt.date) & (dfcrsp_ret['date'].dt.date <= dt_end)]
        else:
            cprint('Factor Regressions: CRSP return (' + freqTypeFull + ') dataset for factor regressions currently NOT saved locally w/ required dates. '
                                                                     '\n                    Querying from wrds-cloud...', 'grey', 'on_white')
            dfcrsp_ret = self.aggregateME(freq, dt_start, dt_end)[['permno', 'date', 'retadj']]
            file_to_pickle = open(crsp_ret_file, 'wb')
            pickle.dump(dfcrsp_ret, file_to_pickle)
            file_to_pickle.close()

        # Clean up 'dfcrsp_ret' and reshape so rows <--> 'date', columns <--> 'permno'.
        dfcrsp_ret = dfcrsp_ret.pivot(index='date', columns='permno', values='retadj')
        dfcrsp_ret.columns = dfcrsp_ret.columns.astype(str)

        # Load or query the Market premium or Fama-French 3 factors using the naming conventions for the
        # 'FamaFrench' class, else we estimate for the first time or re-estimate from wrds-cloud
        # i.e. (['MKT-RF'] or ['MKT-RF', 'SMB', 'HML']) & Risk-Free Rate ('RF').
        if ffmodel == 'capm':
            self.factorsIdtemp, nfactors = ['MKT-RF'], 1
        elif ffmodel == 'ff3':
            self.factorsIdtemp, nfactors = ['MKT-RF', 'SMB', 'HML'], 3
        else:
            raise TypeError('\'ffmodel\' should be the Market model (i.e. CAPM) or the Fama-French 3 model:\n use \'capm\' or \'ff3\'.')

        ff_file = Path(self.pickled_dir + freqTypeFull + '/' + ffmodel + 'factors_' + freqTypeFull + '.pickle')
        if self.runEstimation is False and ff_file.is_file():
            file_to_pickle = open(ff_file, 'rb')
            dfportSort_tableList = pickle.load(file_to_pickle)
            file_to_pickle.close()
            date_min, date_max = dfportSort_tableList['MKT'].index.min(), dfportSort_tableList['MKT'].index.max()
            if (dt_start < date_min) | (date_max < dt_end):
                cprint('Factor Regressions: ' + ffmodel + 'factors (' + freqTypeFull + ') dataset currently NOT saved locally w/ required dates. '
                                                                                    '\n                    Querying from wrds-cloud...', 'grey', 'on_white')

                # Query missing observations BEFORE 'date_min' and append to locally saved copy.
                if dt_start < date_min:
                    # Force an overlap of 'roll_window' days so estimations WITHIN 'roll_window' days of 'date_min' are not
                    # constructed using less than 'roll_window' days as a result of an artificially truncated sample.
                    date_min = (date_min + Day(roll_window)).date()
                    dfportSort_tableList_pre = self.getNyseThresholdsAndRet(self.factorsIdtemp, True, freq, dt_start, date_min)

                    for fffactor in list(dfportSort_tableList.keys()):
                        dfportSort_tableList[fffactor].to_pickle('dfportSort_tableList_' + fffactor)
                        dfportSort_tableList[fffactor] = dfportSort_tableList[fffactor][(dfportSort_tableList[fffactor].index <= dt_end)]
                        dfportSort_tableList_pre[fffactor].insert(0, 'id', 0)
                        dfportSort_tableList[fffactor].insert(0, 'id', 1)

                        dfportSort_tableList[fffactor] = dfportSort_tableList_pre[fffactor].append(dfportSort_tableList[fffactor], ignore_index=False)
                        dfportSort_tableList[fffactor] = dfportSort_tableList[fffactor].reset_index(drop=False)
                        dfportSort_tableList[fffactor] = dfportSort_tableList[fffactor].sort_values(by=[('date', ''), ('id', '')], ascending=[1, 1])
                        dfportSort_tableList[fffactor] = dfportSort_tableList[fffactor].drop_duplicates(subset=[('date', '')], keep='first').reset_index(drop=True)
                        dfportSort_tableList[fffactor] = dfportSort_tableList[fffactor].drop(columns=[('id', '')])
                        dfportSort_tableList[fffactor] = dfportSort_tableList[fffactor].set_index(('date', ''))
                        dfportSort_tableList[fffactor].index.name = 'date'
                    file_to_pickle = open(ff_file, 'wb')
                    pickle.dump(dfportSort_tableList, file_to_pickle)
                    file_to_pickle.close()

                    # Delete pandas.DataFrame no longer needed in memory.
                    lst = [dfportSort_tableList_pre]
                    del dfportSort_tableList_pre
                    del lst
                # Query missing observations AFTER 'date_max' and append to locally saved copy.
                if date_max < dt_end:
                    # Force an overlap of 'roll_window' days so estimations WITHIN 'roll_window' days of 'date_max' are not
                    # constructed using less than 'roll_window' days as a result of an artificially truncated sample.
                    date_max = (date_max - Day(2 * roll_window)).date()
                    dfportSort_tableList_post = self.getNyseThresholdsAndRet(self.factorsIdtemp, True, freq, date_max, dt_end)

                    for fffactor in list(dfportSort_tableList.keys()):
                        dfportSort_tableList[fffactor].to_pickle('dfportSort_tableList_' + fffactor)
                        dfportSort_tableList[fffactor] = dfportSort_tableList[fffactor][(dt_start <= dfportSort_tableList[fffactor].index)]
                        dfportSort_tableList_post[fffactor].insert(0, 'id', 0)
                        dfportSort_tableList[fffactor].insert(0, 'id', 1)

                        dfportSort_tableList[fffactor] = dfportSort_tableList[fffactor].append(dfportSort_tableList_post[fffactor], ignore_index=False)
                        dfportSort_tableList[fffactor] = dfportSort_tableList[fffactor].reset_index(drop=False)
                        dfportSort_tableList[fffactor] = dfportSort_tableList[fffactor].sort_values(by=[('date', ''), ('id', '')], ascending=[1, 1])
                        dfportSort_tableList[fffactor] = dfportSort_tableList[fffactor].drop_duplicates(subset=[('date', '')], keep='last').reset_index(drop=True)
                        dfportSort_tableList[fffactor] = dfportSort_tableList[fffactor].drop(columns=[('id', '')])
                        dfportSort_tableList[fffactor] = dfportSort_tableList[fffactor].set_index(('date', ''))
                        dfportSort_tableList[fffactor].index.name = 'date'
                    file_to_pickle = open(ff_file, 'wb')
                    pickle.dump(dfportSort_tableList, file_to_pickle)
                    file_to_pickle.close()

                    # Delete pandas.DataFrame no longer needed in memory.
                    lst = [dfportSort_tableList_post]
                    del dfportSort_tableList_post
                    del lst
            else:
                cprint('Factor Regressions: ' + ffmodel + 'factors (' + freqTypeFull + ') dataset currently saved locally w/ required dates.', 'grey', 'on_cyan')
                for fffactor in set(dfportSort_tableList.keys()):
                    dfportSort_tableList[fffactor] = dfportSort_tableList[fffactor][(dt_start <= dfportSort_tableList[fffactor].index) & (dfportSort_tableList[fffactor].index <= dt_end)]
        else:
            cprint('Factor Regressions: ' + ffmodel + 'factors (' + freqTypeFull + ') dataset currently NOT saved locally w/ required dates. '
                                                                                '\n                    Querying from wrds-cloud...', 'grey', 'on_white')
            dfportSort_tableList = self.getNyseThresholdsAndRet(self.factorsIdtemp, True, freq, dt_start, dt_end)
            file_to_pickle = open(ff_file, 'wb')
            pickle.dump(dfportSort_tableList, file_to_pickle)
            file_to_pickle.close()

        dfFactors = pd.DataFrame()
        dfFactors['mkt'] = dfportSort_tableList['MKT'].loc[:, ('Returns', 'mktport')]
        dfFactors = dfFactors.join(other=self.queryrf1m(freq, dt_start, dt_end), how='left')
        dfFactors['mkt-rf'] = dfFactors['mkt'] - dfFactors['rf']

        # Create the Fama-French "size" and "value/growth" factors in the traditional way:
        if ffmodel == 'ff3':
            dfFactors['smb'] = utils.portRetAvg(
                dfportSort_tableList['SMB'].loc[:, ('Returns', ('me0-50_bm70-100', 'me0-50_bm30-70', 'me0-50_bm0-30'))]) - \
                               utils.portRetAvg(dfportSort_tableList['SMB'].loc[:,('Returns', ('me50-100_bm70-100', 'me50-100_bm30-70', 'me50-100_bm0-30'))])
            dfFactors['hml'] = utils.portRetAvg(
                dfportSort_tableList['HML'].loc[:, ('Returns', ('me0-50_bm70-100', 'me50-100_bm70-100'))]) - \
                               utils.portRetAvg(dfportSort_tableList['HML'].loc[:, ('Returns', ('me0-50_bm0-30', 'me50-100_bm0-30'))])

        # Calculate Excess returns.
        dfxret = dfcrsp_ret.sub(other=dfFactors['rf'], axis='index')

        # Merge w/ Factors & Risk-Free Rate.
        dfxretTable = dfxret.join(other=dfFactors, how='left').reset_index()
        dfxretTable = dfxretTable.rename(columns={'index': 'date'})
        dfxretTable.loc[:, 'date'] = pd.to_datetime(dfxretTable['date']).dt.strftime('%Y%m%d').astype(float)

        @njit(types.Tuple((f8[:, :], f8[:, :], f8[:, :]))(f8[:, :], f8[:, :], f8[:, :], b1, b1, b1, types.unicode_type, i8, i8, i8), nogil=True, fastmath=True)
        def rolling_ols_sw(Y0, X0, l1X0, boolsw=True, addcon=True, boolRVar=False, cov_type='None', nfactors=1, window=60, min_periods=24):
            """
            Implement rolling OLS regressions for a specific CRSP permno using 'Numba' as described below:
                *   We implement Numba's "just-in-time" (JIT) compiler w/ the 'nopython=True' compilation mode
                    This mode produces much faster code, but is limited in that the native types of all values
                    in the function being called can be inferred (e.g. "object types" such as pandas.Series or
                    pandas.DataFrame can't be inferred, however, floats, int, numpy.ndarray's can be inferred).
                    To use the 'nopython=True' model, we can use the decorator 'jit(nopython=True)' or 'njit'.
                *   Setting 'nogil=True' disables the Python global interpreter lock (GIL).
                    This is useful for taking advantage of multi-core processors.
                *   Setting 'fastmath=True' relaxes the numerical rigour, which allows operations to be vectorized, as
                    floating-point reassociation is permitted, albeit at the expense of potentially unsafe
                    floating-point operations. For our purposes, we do not lose significant precision.

            Parameters
            ___________
            Y0 : numpy.array
                Dataset w/ panel of firm-level returns.
            X0 : numpy.array
                Dataset w/ panel of factors.
            l1X0 : numpy.array
                Dataset w/ panel of lagged factors.
            boolsw: bool, default True
                Flag for choosing whether to implement the Dimson (1979) methodology - based on Scholes-Williams (1977) - as noted earlier (`boolsw = True`).
                Otherwise, we implement the estimation using coincident market variables (`boolsw = False`).
            addcon: bool, default True
                Flag for choosing whether to add or not add a constant to OLS regressions.
            boolRVar: bool, default False
                Flag for choosing whether to calculate the variance of residuals (``boolRvar = True``)
                or the market betas estimated from a specified factor model ``ffmode`` (``boolRvar = False``).
            cov_type: str
                Type of covariance-variance sandwich matrix estimated for the OLS coefficients.
                Currently, must be one of 'nonrobust' or 'HC0' resembling :meth:`statsmodels.regression.linear_model.RegressionResults`.
            nfactors : int, default 1 [optional]
                 Number of factors. Need if `boolsw = True`.
            window : int, default 60
                Fixed size of the rolling (moving) window.
            min_periods: int, default 24
                 Minimum number of observations in each window necessary to have an estimated value.

            Returns
            ________
            params, se, residVar (depending on values of `cov_type` & `boolRVar`) : numpy.array or tuple, numpy.array
                numpy.array objects to be subsequently converted to pandas.DataFrame objects outside of this routine.
            """
            if addcon:
                T = Y0.shape[0]
                X = np.concatenate((np.expand_dims(X0[:, 0], axis=1), np.ones((T, 1)), X0[:, 1:]), axis=1)
                if boolsw:
                    l1X = np.concatenate((np.expand_dims(l1X0[:, 0], axis=1), np.ones((T, 1)), l1X0[:, 1:]), axis=1)

            N, K = Y0.shape[0], nfactors + 1
            params, se, residVar = X.copy(), X.copy(), Y0.copy()
            params[:, 1:], se[:, 1:], residVar[:, 1:] = np.nan, np.nan, np.nan
            if boolsw:
                autocorr, sw_adj = X[:, :nfactors + 1].copy(), X[:, :nfactors + 1].copy()
                autocorr[:, 1:], sw_adj[:, 1:] = np.nan, np.nan

            if Y0.size != 0:
                # Use 'prange(...)' instead of 'range(...)' w/ numba 'njit'
                for r in prange(min_periods - 1, N):
                    y = Y0[r - min(r, window - 1): r + 1, :]
                    x = X[r - min(r, window - 1): r + 1, :]
                    l1x = l1X[r - min(r, window - 1): r + 1, :]
                    sw_adj[r, 1:] = 1

                    # Beta coefficients
                    if boolsw:
                        params_sw_0 = np.linalg.lstsq(x[:, 1:], y[:, 1:])[0].reshape(K, )
                        params_sw_l1 = np.linalg.lstsq(l1x[:, 1:], y[:, 1:])[0].reshape(K, )
                        params[r, 1:] = params_sw_l1 + params_sw_0

                        if nfactors == 1:
                            # METHOD 1: Directly estimate acf(1) using formula:
                            # autocorr[r, 1:] = (np.cov(x[:, 2], l1x[:, 2])[0][1]) / (np.std(x[:, 2]) * np.std(l1x[:, 2]))

                            # METHOD 2: Directly estimate acf(1) using OLS regression for de-meaned process (i.e. can omit intercept)
                            autocorr[r, 1:] = np.linalg.lstsq((l1x[:, 2] - l1x[:, 2].mean()).reshape(l1x.shape[0], 1), (x[:, 2] - x[:, 2].mean()).reshape(x.shape[0], 1))[0].item()
                        else:
                            print('TODO: Apply Dimson (1997) method based on Scholes-Williams (1977) to other quantities of risk beyond the CAPM beta.')
                        # Construct the Scholes-Williams (1977) inspired market beta estimates.
                        sw_adj[r, 1:] = sw_adj[r, 1:] + 2 * autocorr[r, 1]
                        params[r, 2:] = params[r, 2:] / sw_adj[r, 1:]
                    else:
                        # Construct the traditional market beta estimates.
                        params[r, 1:] = np.linalg.lstsq(x[:, 1:], y[:, 1:])[0].reshape(K, )

                    if boolRVar:
                        # Residuals (and their unbiased sample variance): for-loops are much faster in 'njit' than 'np.dot'
                        yhat = np.empty((x[:, 1:].shape[0], 1))
                        for i in range(0, x[:, 1:].shape[0]):
                            sum = 0
                            for j in range(0, x[:, 1:].shape[1]):
                                sum += x[:, 1:][i][j] * params[r, 1:][j]
                            yhat[i] = sum
                        resid = y[:, 1:] - yhat
                        sse = np.sum(resid ** 2)
                        sigma2 = sse / (resid.shape[0] - K)
                        residVar[r, 1:] = sigma2

                        # Standard Errors (SEs):
                        if cov_type != 'None':
                            if cov_type in ['nonrobust', 'HC0']:
                                xx = np.zeros((x[:, 1:].shape[1], x[:, 1:].shape[1]))
                                for i in range(0, x[:, 1:].shape[1]):
                                    for j in range(0, x[:, 1:].shape[1]):
                                        xx[i, j] = 0
                                        for k in range(0, x[:, 1:].shape[0]):
                                            xx[i, j] += x[:, 1:].T[i][k] * x[:, 1:][k][j]
                                xx_inv = np.linalg.inv(xx)
                                if cov_type == 'nonrobust':
                                    Sinv = xx_inv * sigma2
                                else:
                                    Sinv = ((((xx_inv @ x[:, 1:].T) @ np.diag(np.diag(resid @ resid.T))) @ x[:, 1:]) @ xx_inv)
                                se_r = np.diag(Sinv) ** 0.5
                                se[r, 1:] = se_r
                            else:
                                raise ValueError('covariance-variance sandwich matrix type should be \'nonrobust\' or \'HC0\'.')
            return params, se, residVar

        # Separate independent and dependent variables for rolling regressions:
        # NOTE: pandas.DataFrame 'dfmktBeta' requires an ordering of elements in 'self.factorsIdtemp' that includes
        #       the market premium 'MKT-RF' as the first element in the list of strings, hence we set this ordering below.
        if ffmodel == 'capm':
            factorList, nfactors = ['mkt-rf'], 1
        elif ffmodel == 'ff3':
            factorList, nfactors = ['mkt-rf', 'smb', 'hml'], 3

        dfy0 = dfxretTable[dfxretTable.columns.difference(dfFactors.columns)]
        dfx0 = dfxretTable[['date'] + factorList].copy()
        dfl1x0 = dfx0.copy()
        if scholeswilliams:
            dfl1x0.iloc[:, 1:] = dfl1x0.iloc[:, 1:].shift(1)

        def get_rolling_ols(y0, x0, l1x0, permno, boolsw=True, addcon=True, boolRVar=False, cov_type='None', nfactors=1, window=60, min_periods=24):
            """
            Implement rolling OLS regressions for a given CRSP permno using `Numba`-based routine 'rolling_ols_sw()'
            Output is converted to pandas.DataFrame.
            
            Parameters
            ___________
            NOTE: Same parameters described in 'rolling_ols_sw()' w/ the exception of 'permno'.
            permno : str
                CRSP stock identifier.

            Returns
            ________
            dfmktBeta, dfse_mktBeta, dfresidVar (depending on values of `cov_type` & `boolRVar`)
                pandas.DataFrame, or tuple, pandas.DataFrame
            """
            # Drop any corresponding missing observations (i.e. missings in either regressand or regressors).
            nan_idx = y0.isnull().any(axis=1) | x0.isnull().any(axis=1) | l1x0.isnull().any(axis=1)
            Y0, X0, l1X0 = y0[~nan_idx].values, x0[~nan_idx].values, l1x0[~nan_idx].values

            if cov_type == 'None':
                if boolRVar:
                    _, _, residVar = rolling_ols_sw(Y0, X0, l1X0, boolsw, addcon, boolRVar, cov_type, nfactors, window,
                                                    min_periods)
                    if residVar.size != 0:
                        dfresidVar = pd.DataFrame(data=residVar[:, 1], index=residVar[:, 0], columns=[permno]).unstack().dropna()
                        return dfresidVar
                    else:
                        pass
                else:
                    params, _, _ = rolling_ols_sw(Y0, X0, l1X0, boolsw, addcon, boolRVar, cov_type, nfactors, window, min_periods)
                    if params.size != 0:
                        dfmktBeta = pd.DataFrame(data=params[:, 2], index=params[:, 0], columns=[permno]).unstack().dropna()
                        return dfmktBeta
                    else:
                        pass
            else:
                params, se, residVar = rolling_ols_sw(Y0, X0, l1X0, boolsw, addcon, boolRVar, cov_type, nfactors, window,
                                                      min_periods)
                if params.size != 0:
                    dfmktBeta = pd.DataFrame(data=params[:, 2], index=params[:, 0], columns=[permno]).unstack().dropna()
                    dfse_mktBeta = pd.DataFrame(data=se[:, 2], index=se[:, 0], columns=[permno]).unstack().dropna()
                    dfresidVar = pd.DataFrame(data=residVar[:, 1], index=residVar[:, 0], columns=[permno]).unstack().dropna()
                    return dfmktBeta, dfse_mktBeta, dfresidVar
                else:
                    pass

        # First, compile the 'Numba'-based function on a few observations
        # (use progress bar from 'tqdm' Python package - this doesn't add much overhead):
        if boolRVar:
            resVar = [get_rolling_ols(dfy0[['date', c]], dfx0, dfl1x0, permno=c, boolsw=False, boolRVar=True, cov_type='None', nfactors=nfactors, window=roll_window, min_periods=min_per)
                      for c in tqdm(dfy0.columns[1:][0:4], desc='Compiling Rolling OLS routine', position=0)]
        else:
            beta = [get_rolling_ols(dfy0[['date', c]], dfx0, dfl1x0, permno=c, boolsw=True, boolRVar=False, cov_type='None', nfactors=nfactors, window=roll_window, min_periods=min_per)
                    for c in tqdm(dfy0.columns[1:][0:4], desc='Compiling Rolling OLS routine', position=0)]

        # Second, run on the complete pandas.DataFrame following initial compilation
        # (again, use progress bar from 'tqdm' - this doesn't add much overhead):
        if boolRVar:
            resVar = [get_rolling_ols(dfy0[['date', c]], dfx0, dfl1x0, permno=c, boolsw=False, boolRVar=True, cov_type='None', nfactors=nfactors, window=roll_window, min_periods=min_per)
                      for c in tqdm(dfy0.columns[1:][0:-1], desc='Running Rolling OLS routine on all CRSP stocks', position=0)]
        else:
            beta = [get_rolling_ols(dfy0[['date', c]], dfx0, dfl1x0, permno=c, boolsw=True, boolRVar=False, cov_type='None', nfactors=nfactors, window=roll_window, min_periods=min_per)
                    for c in tqdm(dfy0.columns[1:][0:-1], desc='Running Rolling OLS routine on all CRSP stocks', position=0)]

        # Merge list of pandas.Series w/ rolling regressions estimated at 'permno'-level and stored in columns.
        # NOTE: List of pandas.Series can be cleared as we concatenate into them into pandas.DataFrames to save memory,
        #       albeit the effect is negligible. (For example, use 'mktBeta=None' after pd.concat(...)')
        if boolRVar is False:
            dfbeta = pd.concat(beta, axis=0).reset_index()
            dfbeta = dfbeta.rename(columns={'level_0': 'permno', 'level_1': 'date', 0: 'beta'})
            dfbeta.loc[:, 'permno'] = dfbeta['permno'].astype(int)
            dfbeta.loc[:, 'date'] = pd.to_datetime(dfbeta['date'].astype(str), format='%Y%m%d.0')
            return dfbeta
        else:
            dfresVar = pd.concat(resVar, axis=0).reset_index()
            dfresVar = dfresVar.rename(columns={'level_0': 'permno', 'level_1': 'date', 0: 'resvar'})
            dfresVar.loc[:, 'permno'] = dfresVar['permno'].astype(int)
            dfresVar.loc[:, 'date'] = pd.to_datetime(dfresVar['date'].astype(str), format='%Y%m%d.0')
            return dfresVar



    @utils.lru_cached_method(maxsize=32)
    def getMEJune(self, freq, dt_start, dt_end):
        """
        Construct market value of equity **me** for June of every year.

        Parameters
        ___________
        freq : str
            Observation frequency. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.

        Return
        ______
        None
            The pandas.DataFrames ``dfcrsp_june`` and ``dfcrsp3`` are returned as class attributes used in
            class methods :meth:`famafrench.FamaFrench.mergeCCM` and :meth:`famafrench.FamaFrench.getNyseThresholdsAndRet`, respectively.

        Note
        ____
        Following Fama and French (1992, 1993), portfolios for July of year `t` to June of year `t+1` include all NYSE, AMEX, and
        NASDAQ stocks for which we have market value of equity **me** for December of year `t-1` and June of year `t`.

        Note
        ____
        Following the Fama and French methodology, **me** from June of year `t` is used to construct **ME** breakpoints,
        which are then used to form portfolios from July of year `t` to June of year `t+1`.

        Note
        ____
        The approach followed here is similar to the one implemented in SAS found through `WRDS Research Applications
        <https://wrds-www.wharton.upenn.edu/pages/support/applications/risk-factors-and-industry-benchmarks/fama-french-factors/>`_.

        """
        # Query CRSP files w/ aggregated market value of equity - 'me'.
        dfcrsp2 = self.aggregateME(freq, dt_start, dt_end)
        me_dec = self.getMEDec(freq, dt_start, dt_end)

        # SPECIAL CASE: Check if 'dfcrsp2 was already created in an earlier instance, hence reference to it already exists
        #               This is specifically needed if 'BETA' or 'RESVAR' are anomaly characteristics used in the
        #               construction of portfolios.
        if 'ffdate' not in dfcrsp2.columns:
            dfcrsp2.insert(dfcrsp2.columns.get_loc('shrcd'), 'ffdate', dfcrsp2['date'] + MonthEnd(-6))
            dfcrsp2.insert(dfcrsp2.columns.get_loc('shrcd'), 'ffyear', dfcrsp2['ffdate'].dt.year)
            dfcrsp2.insert(dfcrsp2.columns.get_loc('shrcd'), 'ffmonth', dfcrsp2['ffdate'].dt.month)

            # Calculate 'cumretx' for each 'permno' from July of year {t} to June of year {t+1}.
            dfcrsp2.insert(dfcrsp2.columns.get_loc('retadj'), '1+retx', (1 + dfcrsp2['retx']))
            dfcrsp2.insert(dfcrsp2.columns.get_loc('retadj'), 'cumretx', dfcrsp2.groupby(['permno', 'ffyear'])['1+retx'].cumprod())

            # Get lag of 'cumretx' and lag of 'me'
            dfcrsp2.insert(dfcrsp2.columns.get_loc('cumretx'), 'lcumretx', dfcrsp2.groupby(['permno'])['cumretx'].shift(1))
            dfcrsp2.insert(dfcrsp2.columns.get_loc('me'), 'lme', dfcrsp2.groupby(['permno'])['me'].shift(1))

            # If first 'permno' observation then use 'me'/(1+retx) to replace the missing value.
            dfcrsp2['count'] = dfcrsp2.groupby(['permno']).cumcount()
            dfcrsp2['lme'] = np.where((dfcrsp2['count'] == 0), (dfcrsp2['me'] / dfcrsp2['1+retx']), dfcrsp2['lme'])

        cols_list = []
        if 'DP' in set(self.sortCharacsId).union(set(self.mainCharacsId)):
            # NOTE: 'dp' used to form portfolios in June of year {t} is the total dividends paid
            #        from July of year {t-1} to June of year {t} per dollar of equity in June of of year {t}
            #        To get total dividends, we need to extract them from monthly returns, which can be done by taking the
            #        difference between cum-dividend (delisted-adjusted) returns ('retadj')
            #        and ex-dividend (delisted-adjusted) returns ('retadjx') in CRSP.
            #
            #        Per Fama and French (2008, 2015), for each 'permno' we would need at least 7 monthly returns to compute the
            #        dividend yield 'dp'. We will also need market value of equity 'me' for June of year {t}.
            # NOTE: In a week: 5 trading days
            #       In a month: avg of 21 trading days
            #       In a quarter: avg of 63 trading days
            #       In a year: avg of 251/252 trading days
            if freq in ['D', 'W']:
                retCount_june_scale = 147  # = (7 months * 21 trading days/month)
                retCount_tradefreq = 251
            elif freq in ['M', 'Q', 'A']:
                retCount_june_scale = 7  # = (7 months = BASIS)
                retCount_tradefreq = 12
            else:
                raise ValueError('frequency is not a standard type.\n '
                                 'Please specify one of the following: \'D\', \'W\', \'M\', \'Q\',  or \'A\'')

            # NOTE: The portfolios for July of year {t} to June of {t+1} include NYSE, AMEX, and NASDAQ stocks for which we have
            #       ME for June of year {t}, and at least 7 monthly returns (to compute the dividend yield) from July of {t-1} to June of {t}.
            #       This is automatically tracked w/ a non-missing value for 'cumdiv_p'.
            dfcrsp2.insert(dfcrsp2.columns.get_loc('lme'), 'div', (dfcrsp2['retadj'] - dfcrsp2['retadjx']) * dfcrsp2.groupby(['permno'])['prc'].shift(1).abs())
            cumdiv_p = dfcrsp2.groupby('permno')['div'].rolling(min_periods=retCount_june_scale, window=retCount_tradefreq).sum().reset_index(level='permno')[['div']]
            cumdiv_p = cumdiv_p.rename(columns={'div': 'cumdiv'})
            dfcrsp2 = dfcrsp2.join(other=cumdiv_p, how='inner')
            dfcrsp2.insert(dfcrsp2.columns.get_loc('cumdiv') + 1, 'cumdiv_p', dfcrsp2['cumdiv'] / dfcrsp2['prc'].abs())
            dfcrsp2.insert(dfcrsp2.columns.get_loc('cumdiv') + 2, 'lcumdiv_p', dfcrsp2.groupby(['permno'])['cumdiv_p'].shift(1))
            dfcrsp2 = dfcrsp2.drop(columns=['cumdiv'])

            # Obtain 'lcumdiv_p' for month==June (which corresponds to 'ffmonth'==January).
            dp_june = dfcrsp2[(dfcrsp2['date'].dt.month == 7)]
            if freq in ['D', 'W']:
                dp_june_bom = dp_june.groupby(['permno', 'ffyear'])['date'].min().reset_index().rename(columns={'date': 'date_bom'})
                dp_june = dp_june.merge(right=dp_june_bom, how='left', on=['permno', 'ffyear'])
                dp_june = dp_june[(dp_june['date'] == dp_june['date_bom'])]

                # Delete pandas.DataFrame no longer needed in memory.
                lst = [dp_june_bom]
                del dp_june_bom
                del lst
            dp_june = dp_june[['permno', 'ffyear', 'lcumdiv_p']].rename(columns={'lcumdiv_p': 'cumdiv_p_june'})
            dp_june['cumdiv_p_june'] = np.where(~dp_june['cumdiv_p_june'].isnull(), dp_june['cumdiv_p_june'], np.nan)

        # List containing all anomaly characteristics w/ 'PRIOR' in their name (+ the two parameters that are needed).
        re_prior = compile('PRIOR_' + r'[0-9]+' + '_' + r'[0-9]+')
        prior_list = list(filter(re_prior.search, set(self.sortCharacsId).union(set(self.mainCharacsId))))
        if len(prior_list) != 0 or utils.any_in(['MOM', 'ST_Rev', 'LT_Rev'], self.factorsId):
            df_prior = dfcrsp2[['permno', 'date', 'retadj']].sort_values(by=['permno', 'date']).set_index(['date'])
            df_prior['1+retadj'] = df_prior['retadj'] + 1

            # Add 'PRIOR_2_12' if 'MOM' is in 'factorsId' and not already in 'prior_list'.
            if ('MOM' in self.factorsId) and ('PRIOR_2_12' not in prior_list):
                prior_list.append('PRIOR_2_12')
            # Add 'PRIOR_1_1' if 'ST_Rev' is in 'factorsId' and not already in 'prior_list'.
            if ('ST_Rev' in self.factorsId) and ('PRIOR_1_1' not in prior_list):
                prior_list.append('PRIOR_1_1')
            # Add 'PRIOR_13_60' if 'LT_Rev' is in 'factorsId' and not already in 'prior_list'.
            if ('LT_Rev' in self.factorsId) and ('PRIOR_13_60' not in prior_list):
                prior_list.append('PRIOR_13_60')

            for c in prior_list:
                # Using the terminology in...
                # (1) Fama, Eugene F., and Kenneth R. French. (2008). "Dissecting Anomalies",
                #     Journal of Finance, 48(4), pp.1653-1678;
                # (2) Fama, Eugene F., and Kenneth R. French. (2016). "Dissecting Anomalies w/ a Five-Factor Model",
                #     The Review of Financial Studies, 29(1), pp.69-103
                # we consider a portfolio of stocks w/ returns for period {t-k} to {t-j}, w/ j<=k.
                # Example 1 (MONTHLY): the portfolio of stocks formed on prior returns denoted "prior (2-12)"
                #                      is composed of the 11-month cumulative return from month {t-13} to month {t-2}
                # Example 2 (MONTHLY): the portfolio of stocks formed on prior returns denoted "prior (1-1)"
                #                      is composed of the 1-month cumulative return from month {t-2} to {t-1}
                # Example 3 (MONTHLY): the portfolio of stocks formed on prior returns denoted "prior (13-60)"
                #                      is composed of the 48-month cumulative return from month {t-61} to month {t-13}
                # NOTE: French's online library provides data ONLY at the "monthly" and "daily" frequency.
                j_month, k_month = c.split('_')[1], c.split('_')[2]
                j_per, k_per = utils.priormonthToDay(freq, j_month, k_month)

                if 'l' + j_per + '_retadj' not in df_prior.columns:
                    df_prior['l' + j_per + '_retadj'] = df_prior.groupby(['permno'])['retadj'].shift(int(j_per))
                if int(k_per) > 1:
                    if 'l' + k_per + '_retadj' not in df_prior.columns:
                        df_prior['l' + k_per + '_retadj'] = df_prior.groupby(['permno'])['retadj'].shift(int(k_per))

                # If int(k_per) > 1 we calculate prior (j-k) return (w/ dividends) by using pandas.rolling()
                # Else if int(k_per) == 1, we just lag returns accordingly:
                if int(k_per) == 1:
                    df_prior['prior_' + j_month + '_' + k_month] = df_prior.groupby(['permno'])['retadj'].shift(int(j_per))
                else:
                    df_prior['prior_' + j_month + '_' + k_month] = np.exp(np.log(df_prior.groupby(['permno'])['1+retadj'].shift(int(j_per))).rolling(window=(int(k_per) - int(j_per) + 1)).sum()) - 1
                df_prior['prior_' + j_month + '_' + k_month] = np.where(~df_prior['prior_' + j_month + '_' + k_month].isnull(), df_prior['prior_' + j_month + '_' + k_month], np.nan)

            df_prior = df_prior.drop(columns=['retadj', '1+retadj'])
            dfcrsp2 = dfcrsp2.merge(right=df_prior.reset_index(), how='left', on=['permno', 'date'])

        if 'VAR' in set(self.sortCharacsId).union(set(self.mainCharacsId)):
            # Variance of daily returns estimated using 60 (w/ a minimum 20) days of lagged daily returns.
            df_rollvar = self.getCrspDailyRollVar(roll_window=60, min_periods=20, freq=self.freqType, dt_start=dt_start, dt_end=dt_end)

            # Since portfolios for month {t} (day {t}) are formed at the end of month {t-1} (end of day {t-1}),
            # we lag the variance estimate by one month to make future merges easier.
            df_rollvar['lvar'] = df_rollvar.groupby(['permno'])['var'].shift(1)
            df_rollvar = df_rollvar.drop(columns=['var']).rename(columns={'lvar': 'var'})
            df_rollvar['var'] = np.where(~df_rollvar['var'].isnull(), df_rollvar['var'] * 10000, np.nan)  # decimals --> % in returns

            # Merge 'dfcrsp2' w/ 'df_rollvar'.
            dfcrsp2 = dfcrsp2.merge(right=df_rollvar.reset_index(), how='left', on=['permno', 'date'])

        if 'RESVAR' in set(self.sortCharacsId).union(set(self.mainCharacsId)) and self.runFactorReg:
            # Variance of DAILY residuals from FF3-model estimated using 60 (w/ a minimum 20) days of lagged daily returns.
            self.runFactorReg = False

            # Load local file if it exists (and dates can be found), else we re-estimate.
            if freq in ['D', 'W']:
                freqTypeFull = 'daily'
            else:
                freqTypeFull = 'monthly'

            resvar_file = Path(self.pickled_dir + freqTypeFull + '/crspff3resvar_' + freqTypeFull + '.pickle')
            if self.runEstimation is False and resvar_file.is_file():
                file_to_pickle = open(resvar_file, 'rb')
                dfresvarff3 = pickle.load(file_to_pickle)
                file_to_pickle.close()
                date_min, date_max = dfresvarff3['date'].dt.date.min(), dfresvarff3['date'].dt.date.max()
                print('RESVAR period', dt_start, date_min, ' ', date_max, dt_end)
                if (dt_start < date_min) | (date_max < dt_end):
                    cprint('FF3-model daily residuals dataset currently NOT saved locally w/ required dates. Estimating...', 'grey', 'on_white')

                    # Query missing observations BEFORE 'date_min' and append to locally saved copy
                    if dt_start < date_min:
                        dfresvarff3_pre = self.getFactorRegResults(ffmodel='ff3', boolRVar=True, scholeswilliams=False,
                                                                   roll_window=60, min_per=20, freq='D', dt_start=dt_start, dt_end=date_min)
                        dfresvarff3_pre.insert(0, 'id', 0)

                        dfresvarff3 = dfresvarff3[(dfresvarff3['date'].dt.date <= dt_end)]
                        dfresvarff3.insert(0, 'id', 1)

                        dfresvarff3 = dfresvarff3_pre.append(dfresvarff3, ignore_index=True)
                        dfresvarff3 = dfresvarff3.sort_values(by=['permno', 'date', 'id'], ascending=[1, 1, 1])
                        dfresvarff3 = dfresvarff3.drop_duplicates(subset=['permno', 'date'], keep='first').reset_index(drop=True)
                        dfresvarff3 = dfresvarff3.drop(columns=['id'])
                        file_to_pickle = open(resvar_file, 'wb')
                        pickle.dump(dfresvarff3, file_to_pickle)
                        file_to_pickle.close()

                        # Delete pandas.DataFrame no longer needed in memory.
                        lst = [dfresvarff3_pre]
                        del dfresvarff3_pre
                        del lst
                    # Query missing observations AFTER 'date_max' and append to locally saved copy.
                    if date_max < dt_end:
                        dfresvarff3_post = self.getFactorRegResults(ffmodel='ff3', boolRVar=True, scholeswilliams=False,
                                                                    roll_window=60, min_per=20, freq='D', dt_start=date_max, dt_end=dt_end)
                        dfresvarff3_post.insert(0, 'id', 0)

                        dfresvarff3 = dfresvarff3[(dt_start <= dfresvarff3['date'].dt.date)]
                        dfresvarff3.insert(0, 'id', 1)

                        dfresvarff3 = dfresvarff3.append(dfresvarff3_post, ignore_index=True)
                        dfresvarff3 = dfresvarff3.sort_values(by=['permno', 'date', 'id'], ascending=[1, 1, 1])
                        dfresvarff3 = dfresvarff3.drop_duplicates(subset=['permno', 'date'], keep='last').reset_index(drop=True)
                        dfresvarff3 = dfresvarff3.drop(columns=['id'])
                        file_to_pickle = open(resvar_file, 'wb')
                        pickle.dump(dfresvarff3, file_to_pickle)
                        file_to_pickle.close()

                        # Delete pandas.DataFrame no longer needed in memory.
                        lst = [dfresvarff3_post]
                        del dfresvarff3_post
                        del lst
                else:
                    cprint('FF3-model daily residuals dataset currently saved locally w/ required dates.', 'grey', 'on_cyan')
                    dfresvarff3 = dfresvarff3[(dt_start <= dfresvarff3['date'].dt.date) & (dfresvarff3['date'].dt.date <= dt_end)]
            else:
                cprint('FF3-model daily residuals dataset currently NOT saved locally w/ required dates. Estimating...', 'grey', 'on_white')
                dfresvarff3 = self.getFactorRegResults(ffmodel='ff3', boolRVar=True, scholeswilliams=False, roll_window=60,
                                                       min_per=20, freq='D', dt_start=dt_start, dt_end=dt_end)

                file_to_pickle = open(resvar_file, 'wb')
                pickle.dump(dfresvarff3, file_to_pickle)
                file_to_pickle.close()

                # If portfolio returns are NOT 'daily', then we need to get end-of-period values...
                if freq in ['M', 'Q', 'A']:
                    dfresvarff3.insert(dfresvarff3.columns.get_loc('resvar'), 'year', dfresvarff3['date'].dt.year)
                    dfresvarff3.insert(dfresvarff3.columns.get_loc('year'), 'month', dfresvarff3['date'].dt.month)
                    dfresvarff3_eom = dfresvarff3.groupby(['permno', 'year', 'month'])['date'].max().reset_index().rename(columns={'date': 'date_eom'})
                    dfresvarff3 = dfresvarff3.merge(right=dfresvarff3_eom, how='left', on=['permno', 'year', 'month'])

                    dfresvarff3 = dfresvarff3[dfresvarff3['date'] == dfresvarff3['date_eom']]
                    dfresvarff3.loc[:, 'date'] = dfresvarff3['date'] + MonthEnd(0)
                    dfresvarff3 = dfresvarff3[['permno', 'date', 'resvar']]

            # Since portfolios for month {t} (or day {t}) are formed at the end of month {t-1} (or end of day {t-1}),
            # we lag the residual variance estimate by one month to make future merges easier.
            dfresvarff3['lresvar'] = dfresvarff3.groupby(['permno'])['resvar'].shift(1)
            dfresvarff3 = dfresvarff3.drop(columns=['resvar']).rename(columns={'lresvar': 'resvar'})
            dfresvarff3['resvar'] = np.where(~dfresvarff3['resvar'].isnull(), dfresvarff3['resvar'] * 10000, np.nan)  # decimals --> % in returns

            # Merge 'dfcrsp2' w/ 'dfresvarff3'.
            dfcrsp2 = dfcrsp2.merge(right=dfresvarff3, how='left', on=['permno', 'date'])

        if 'BETA' in set(self.sortCharacsId).union(set(self.mainCharacsId)) and self.runFactorReg:
            # (Market) beta's estimated using 60 (w/ a minimum 24) months of lagged monthly returns.
            self.runFactorReg = False

            # Load local file if it exists (and dates can be found), else re-estimate.
            if freq in ['D', 'W']:
                freqTypeFull, freqtmp = 'daily', 'D'
            else:
                freqTypeFull, freqtmp = 'monthly', 'M'

            beta_file = Path(self.pickled_dir + freqTypeFull + '/beta_' + freqTypeFull + '.pickle')
            if self.runEstimation is False and beta_file.is_file():
                file_to_pickle = open(beta_file, 'rb')
                dfbeta = pickle.load(file_to_pickle)
                file_to_pickle.close()
                cprint('Market beta (' + freqTypeFull + ') dataset currently saved locally w/ required dates.', 'grey', 'on_cyan')
                date_min, date_max = dfbeta['date'].dt.date.min(), dfbeta['date'].dt.date.max()
                print('BETA period', dt_start, date_min, ' ', date_max, dt_end)
                if (dt_start < date_min) | (date_max < dt_end):
                    cprint('Market beta (' + freqTypeFull + ') dataset currently NOT saved locally w/ required dates. Estimating...', 'grey', 'on_white')

                    # Query missing observations BEFORE 'date_min' and append to locally saved copy.
                    if dt_start < date_min:
                        dfbeta_pre = self.getFactorRegResults(ffmodel='capm', boolRVar=False, scholeswilliams=True,
                                                              roll_window=60, min_per=24, freq=freqtmp, dt_start=dt_start, dt_end=date_min)
                        dfbeta_pre.insert(0, 'id', 0)

                        dfbeta = dfbeta[(dfbeta['date'].dt.date <= dt_end)]
                        dfbeta.insert(0, 'id', 1)

                        dfbeta = dfbeta_pre.append(dfbeta, ignore_index=True)
                        dfbeta = dfbeta.sort_values(by=['permno', 'date', 'id'], ascending=[1, 1, 1])
                        dfbeta = dfbeta.drop_duplicates(subset=['permno', 'date'], keep='first').reset_index(drop=True)
                        dfbeta = dfbeta.drop(columns=['id'])
                        file_to_pickle = open(beta_file, 'wb')
                        pickle.dump(dfbeta, file_to_pickle)
                        file_to_pickle.close()

                        # Delete pandas.DataFrame no longer needed in memory.
                        lst = [dfbeta_pre]
                        del dfbeta_pre
                        del lst
                    # Query missing observations AFTER 'date_max' and append to locally saved copy.
                    if date_max < dt_end:
                        dfbeta_post = self.getFactorRegResults(ffmodel='capm', boolRVar=False, scholeswilliams=True,
                                                               roll_window=60, min_per=24, freq=freqtmp, dt_start=date_max, dt_end=dt_end)
                        dfbeta_post.insert(0, 'id', 0)

                        dfbeta = dfbeta[(dt_start <= dfbeta['date'].dt.date)]
                        dfbeta.insert(0, 'id', 1)

                        dfbeta = dfbeta.append(dfbeta_post, ignore_index=True)
                        dfbeta = dfbeta.sort_values(by=['permno', 'date', 'id'], ascending=[1, 1, 1])
                        dfbeta = dfbeta.drop_duplicates(subset=['permno', 'date'], keep='last').reset_index(drop=True)
                        dfbeta = dfbeta.drop(columns=['id'])
                        file_to_pickle = open(beta_file, 'wb')
                        pickle.dump(dfbeta, file_to_pickle)
                        file_to_pickle.close()

                        # Delete pandas.DataFrame no longer needed in memory.
                        lst = [dfbeta_post]
                        del dfbeta_post
                        del lst
                else:
                    cprint('Market beta (' + freqTypeFull + ') dataset currently saved locally w/ required dates.', 'grey', 'on_cyan')
                    dfbeta = dfbeta[(dt_start <= dfbeta['date'].dt.date) & (dfbeta['date'].dt.date <= dt_end)]
            else:
                cprint('Market beta (' + freqTypeFull + ') dataset currently NOT saved locally w/ required dates. Estimating...', 'grey', 'on_white')
                dfbeta = self.getFactorRegResults(ffmodel='capm', boolRVar=False, scholeswilliams=True,
                                                  roll_window=60, min_per=24, freq=freqtmp, dt_start=dt_start, dt_end=dt_end)
                file_to_pickle = open(beta_file, 'wb')
                pickle.dump(dfbeta, file_to_pickle)
                file_to_pickle.close()

            # Since portfolios for month {t} are formed at the end of June {t}, we lag the estimated betas by one month to make future merges easier.
            dfbeta['lbeta'] = dfbeta.groupby(['permno'])['beta'].shift(1)
            dfbeta = dfbeta.drop(columns=['beta'])

            # Merge 'dfcrsp2' w/ 'dfbeta'
            dfcrsp2 = dfcrsp2.merge(right=dfbeta, how='left', on=['permno', 'date'])

            # Obtain 'lbeta' & 'lme' for month==June (which corresponds to 'ffmonth'==January).
            me_june = dfcrsp2[(dfcrsp2['date'].dt.month == 7)]
            beta_june = dfcrsp2[(dfcrsp2['date'].dt.month == 7)]
            if freq in ['D', 'W']:
                me_june_bom = me_june.groupby(['permno', 'ffyear'])['date'].min().reset_index().rename(columns={'date': 'date_bom'})
                me_june = me_june.merge(right=me_june_bom, how='left', on=['permno', 'ffyear'])
                me_june = me_june[(me_june['date'] == me_june['date_bom'])]
                me_june = me_june[['permno', 'date_bom', 'ffyear', 'lme']].rename(columns={'lme': 'me_june'})

                # Delete pandas.DataFrame no longer needed in memory.
                lst = [me_june_bom]
                del me_june_bom
                del lst

                beta_june_bom = beta_june.groupby(['permno', 'ffyear'])['date'].min().reset_index().rename(columns={'date': 'date_bom'})
                beta_june = beta_june.merge(right=beta_june_bom, how='left', on=['permno', 'ffyear'])
                beta_june = beta_june[(beta_june['date'] == beta_june['date_bom'])]

                # Delete pandas.DataFrame no longer needed in memory.
                lst = [beta_june_bom]
                del beta_june_bom
                del lst
            else:
                me_june = me_june[['permno', 'ffyear', 'lme']].rename(columns={'lme': 'me_june'})

            beta_june = beta_june[['permno', 'ffyear', 'lbeta']].rename(columns={'lbeta': 'beta'})
            beta_june['beta'] = np.where(~beta_june['beta'].isnull(), beta_june['beta'], np.nan)

            # Merge 'june' results back together.
            self.dfcrsp3 = dfcrsp2.merge(right=me_june, how='left', on=['permno', 'ffyear'])
            self.dfcrsp3 = self.dfcrsp3.merge(right=beta_june, how='left', on=['permno', 'ffyear'])
            cols_list = cols_list + ['lbeta', 'beta']

        else:
            # Obtain 'lme' for month==July (which corresponds to 'ffmonth'==January).
            me_june = dfcrsp2[(dfcrsp2['date'].dt.month == 7)]
            if freq in ['D', 'W']:
                me_june_bom = me_june.groupby(['permno', 'ffyear'])['date'].min().reset_index().rename(columns={'date': 'date_bom'})
                me_june = me_june.merge(right=me_june_bom, how='left', on=['permno', 'ffyear'])
                me_june = me_june[(me_june['date'] == me_june['date_bom'])]
                me_june = me_june[['permno', 'date_bom', 'ffyear', 'lme']].rename(columns={'lme': 'me_june'})

                # Delete pandas.DataFrame no longer needed in memory.
                lst = [me_june_bom]
                del me_june_bom
                del lst
            else:
                me_june = me_june[['permno', 'ffyear', 'lme']].rename(columns={'lme': 'me_june'})

            # Merge 'june' results back together.
            self.dfcrsp3 = dfcrsp2.merge(right=me_june, how='left', on=['permno', 'ffyear'])

        # Given 'me' in June of year of {t}, then portfolio weight from July of year {t} to June of year {t+1} is fixed,
        # using 'me_june' as the portfolio allocation for each 'permno'.
        if freq in ['D', 'W']:
            self.dfcrsp3['port_weight'] = np.where((self.dfcrsp3['date'] == self.dfcrsp3['date_bom']), self.dfcrsp3['lme'], self.dfcrsp3['me_june'] * self.dfcrsp3['lcumretx'])
            self.dfcrsp3 = self.dfcrsp3.drop(columns=['date_bom'])
        else:
            self.dfcrsp3['port_weight'] = np.where((self.dfcrsp3['date'].dt.month == 7), self.dfcrsp3['lme'], self.dfcrsp3['me_june'] * self.dfcrsp3['lcumretx'])

        if 'DP' in set(self.sortCharacsId).union(set(self.mainCharacsId)):
            # Get "dividend yield":
            self.dfcrsp3 = self.dfcrsp3.merge(right=dp_june, how='left', on=['permno', 'ffyear'])
            cols_list = cols_list + ['cumdiv_p', 'cumdiv_p_june']

        me_dec.loc[:, 'year'] = me_dec['year'] + 1
        me_dec = me_dec[['permno', 'year', 'me_dec']]

        # Get 'me' (and 'beta', if applicable) as of June of year {t}, as well as 'me' for December of year {t-1} (i.e. 'me_dec').
        self.dfcrsp_june = self.dfcrsp3[(self.dfcrsp3['date'].dt.month == 6)]
        if freq in ['D', 'W']:
            dfcrsp_june_eom = self.dfcrsp_june.groupby(['permno', 'year'])['date'].max().reset_index().rename(columns={'date': 'date_eom'})
            self.dfcrsp_june = self.dfcrsp_june.merge(right=dfcrsp_june_eom, how='left', on=['permno', 'year'])
            self.dfcrsp_june = self.dfcrsp_june[(self.dfcrsp_june['date'] == self.dfcrsp_june['date_eom'])]
            self.dfcrsp_june = self.dfcrsp_june.drop(columns=['date_eom'])
            self.dfcrsp_june.loc[:, 'date'] = self.dfcrsp_june['date'] + MonthEnd(0)

            # Delete pandas.DataFrame no longer needed in memory
            lst = [dfcrsp_june_eom]
            del dfcrsp_june_eom
            del lst

        self.dfcrsp_june = self.dfcrsp_june.merge(right=me_dec, how='inner', on=['permno', 'year'])
        self.dfcrsp_june = self.dfcrsp_june[['permno', 'date', 'shrcd', 'exchcd', 'retadj', 'lme', 'me', 'port_weight', 'me_june', 'me_dec'] + cols_list]
        self.dfcrsp_june = self.dfcrsp_june.sort_values(by=['permno', 'date']).drop_duplicates()

        # Get current month 'me' as 'me_t':
        self.dfcrsp3 = self.dfcrsp3.rename(columns={'me': 'me_t'})
        return None



    @utils.lru_cached_method(maxsize=32)
    def mergeCCM(self, freq, dt_start, dt_end):
        """
        Query the CRSP/Compustat (CCM) Merged Linking Table needed to merge CRSP securities to
        Compustat companies on (**permno**, **gvkey**) identifier pairs.

        Parameters
        ___________
        freq : str
            Observation frequency. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.

        Returns
        _______
        None
             The pandas.DataFrame ``dfccm_june`` is returned as a class attribute used in the
             class method :meth:`famafrench.FamaFrench.getNyseThresholdsAndRet`.

        Note
        ______
        List of (CCM) Merged Linking Table variables:

            - **gvkey**     : Unique permanent identifier assigned by Compustat at the company-level
            - **lpermno**   : Historical CRSP `permno` Link to Compustat Record
            - **linktype**  : Link Type Code
            - **linkprim**  : Primary Link Marker
            - **linkdt**    : First Effective Date of Link
            - **linkenddt** : Last Effective Date of Link

        Note
        ____
        The approach followed here is similar to the one implemented in SAS found through `WRDS Research Applications
        <https://wrds-www.wharton.upenn.edu/pages/support/applications/risk-factors-and-industry-benchmarks/fama-french-factors/>`_.

        """
        if self.factorsId != 'MKT-RF':
            self.getMEJune(freq, dt_start, dt_end)
        dfcomp, dfcomp_list = self.queryComp(dt_start, dt_end)

        ccm_sqlQuery = """
                        SELECT gvkey, lpermno as permno, linktype, linkprim, linkdt, linkenddt
                            FROM crsp.ccmxpf_linktable
                            WHERE substr(linktype,1,1)='L'
                            AND (linkprim ='C' or linkprim='P')
                       """

        # Load local file if it exists, else query from wrds-cloud.
        ccm_file = Path(self.pickled_dir + 'ccm.pickle')
        if self.runQuery is False and ccm_file.is_file():
            file_to_pickle = open(ccm_file, 'rb')
            dfccm = pickle.load(file_to_pickle)
            file_to_pickle.close()
        else:
            cprint('CRSP-Compustat merged linktable currently NOT saved locally. Querying from wrds-cloud...', 'grey', 'on_white')
            dfccm = wrdsConn.raw_sql(sqlquery=ccm_sqlQuery)
            file_to_pickle = open(ccm_file, 'wb')
            pickle.dump(dfccm, file_to_pickle)
            file_to_pickle.close()

        # Get datetime objects...
        dfccm['linkdt'] = pd.to_datetime(dfccm['linkdt'])
        dfccm['linkenddt'] = pd.to_datetime(dfccm['linkenddt'])

        # If 'linkenddt' is missing, then set to today's date, 'today'.
        dfccm['linkenddt'] = dfccm['linkenddt'].fillna(pd.to_datetime('today'))
        dfccm1 = dfcomp[['gvkey', 'datadate', 'count'] + dfcomp_list].merge(right=dfccm, how='left', on=['gvkey'])

        if len(dfcomp_list) == 0:
            dfccm1.insert(dfccm1.columns.get_loc('count'), 'yearend', dfccm1['datadate'] + YearEnd(0))
            dfccm1.insert(dfccm1.columns.get_loc('count'), 'date', dfccm1['yearend'] + MonthEnd(6))
        else:
            dfccm1.insert(dfccm1.columns.get_loc(dfcomp_list[0]), 'yearend', dfccm1['datadate'] + YearEnd(0))
            dfccm1.insert(dfccm1.columns.get_loc(dfcomp_list[0]), 'date', dfccm1['yearend'] + MonthEnd(6))

        # Set the CCM link date bounds.
        dfccm2 = dfccm1[(dfccm1['date'] >= dfccm1['linkdt']) & (dfccm1['date'] <= dfccm1['linkenddt'])]
        dfccm2 = dfccm2[['gvkey', 'permno', 'datadate', 'yearend', 'date', 'count'] + dfcomp_list]

        # Link CRSP w/ Compustat.
        if self.factorsId != 'MKT-RF':
            self.dfccm_june = self.dfcrsp_june.merge(right=dfccm2, how='inner', on=['permno', 'date'])
        else:
            self.dfccm_june = dfccm2

        if (utils.any_in(['BE', 'BM', 'OP', 'AC'], set(self.sortCharacsId).union(set(self.mainCharacsId))) or
                utils.any_in(['SMB', 'HML', 'RMW', 'CMA'], set(self.factorsId).union(set(self.factorsIdtemp)))):
            # Original 'be' is in USD thousands, need it in USD millions since 'me_dec' is in USD millions
            # NOTE: 'bm' uses book equity 'be' at the end of fiscal year {t-1} (i.e. previous June of year {t-1} to current May of year {t})
            #        and the market value of equity 'me_dec' at the end of December of year {t}.
            self.dfccm_june['me_dec_nonzero'] = np.where((self.dfccm_june['me_dec'].isnull()) | (self.dfccm_june['me_dec'] <= 0), np.nan, self.dfccm_june['me_dec'])
            self.dfccm_june['bm'] = (self.dfccm_june['be'] * 1000) / self.dfccm_june['me_dec_nonzero']
            self.dfccm_june['be'] = np.where(~self.dfccm_june['be'].isnull(), self.dfccm_june['be'], np.nan)
            self.dfccm_june = self.dfccm_june.drop(columns=['me_dec_nonzero'])

        if 'EP' in set(self.sortCharacsId).union(set(self.mainCharacsId)):
            # Original 'ib' is in USD thousands, need it in USD millions since 'me_dec' is in USD millions
            # NOTE: 'ep' uses "income before extraordinary items" 'ib' at the end of fiscal year {t-1}
            #       (i.e. previous June of year {t-1} to current May of year {t})
            #        and the market value of equity 'me_dec' at the end of December of year {t}.
            self.dfccm_june['ep'] = (self.dfccm_june['ib'] * 1000) / self.dfccm_june['me_dec']
            self.dfccm_june['ep'] = np.where(~self.dfccm_june['ep'].isnull(), self.dfccm_june['ep'], np.nan)

        if 'CFP' in set(self.sortCharacsId).union(set(self.mainCharacsId)):
            # Original 'cf' is in USD thousands, need it in USD millions since 'me_dec' is in USD millions
            # NOTE: 'cfp' uses "income before extraordinary items" 'ib' & "deferred taxes and investment tax credit"
            #        at the end of fiscal year {t-1} (i.e. previous June of year {t-1} to current May of year {t})
            #        and the market value of equity 'me_dec' at the end of December of year {t}.
            self.dfccm_june['cfp'] = (self.dfccm_june['cf'] * 1000) / self.dfccm_june['me_dec']
            self.dfccm_june['cfp'] = np.where(~self.dfccm_june['cfp'].isnull(), self.dfccm_june['cfp'], np.nan)

        if 'DP' in set(self.sortCharacsId).union(set(self.mainCharacsId)):
            # Dividend yield a la Fama and French (see French's online documentation for construction details).
            self.dfccm_june = self.dfccm_june.rename(columns={'cumdiv_p_june': 'dp'})
            self.dfccm_june['dp'] = np.where((self.dfccm_june['dp'].isnull()) | (self.dfccm_june['dp'] <= 0), np.nan, self.dfccm_june['dp'])

        if 'AC' in set(self.sortCharacsId).union(set(self.mainCharacsId)):
            # Accruals a la Fama and French (see French's online documentation for construction details).
            self.dfccm_june['ac'] = self.dfccm_june['d_owcap_adj'] / (self.dfccm_june['be'] / self.dfccm_june['csho_adj'])
            self.dfccm_june['ac'] = np.where(~self.dfccm_june['ac'].isnull(), self.dfccm_june['ac'], np.nan)

            # NOTE: Compustat data yields gross outliers in 'ac' for June of each year {t} w/ ratios as low as '-200' and as large as '200'.
            #       To be consistent w/ summary statistics for characteristics provided by Ken French's online library,
            #       values for 'ac' less than '-200' and values for 'ac' larger than '200' are set to missing.
            self.dfccm_june['ac'] = np.where((-200 <= self.dfccm_june['ac']), self.dfccm_june['ac'], np.nan)
            self.dfccm_june['ac'] = np.where((self.dfccm_june['ac'] <= 200), self.dfccm_june['ac'], np.nan)
        return None



    def getNyseThresholdsAndRet(self, idList, factorsBool, freq, dt_start, dt_end, *args):
        """
        Select NYSE stocks used in the construction of breakpoints (ie thresholds) for portfolio sorting.
        Selection occurs at a given frequency and for a given sample period.

        Parameters
        ___________
        idList : list, str
            List of factors or list of anomaly portfolio characteristics whose
            naming convention is consistent w/ earlier described conventions.
        factorsBool : bool
            Flag for choosing whether to construct Fama-French factors or not.
            If `False`, then ``dim`` (w/ or w/out a value for ``retType``) must be passed as additional argument(s),
            otherwise these additional arguments are not passed.
        freq : str
            Observation frequency of the portfolios. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.
        dim : list, int, [optional]
            Dimensions for sorting on each element in the list ``idList``.
            For example, if ``idList = ['ME', 'BM']`` and ``dim = [5, 5]``, then the portfolio sorting strategy
            is characterized by a bivariate quintile sort on both `size` and `book-to-market`.
        retType : str, [optional]
            Weighting-scheme for portfolios. Possible choices are:

                * ``vw`` : value-weights
                * ``ew`` : equal-weights

        Returns
        ________
        dfportSort_tableList : pandas.DataFrame, or dict, pandas.DataFrame
            Dataset(s) providing one of the following:

                1. Time-series of Fama-French-style factors.
                2. Panel data consisting of portfolios sorted on specific anomaly characteristics w/ the corresponding:

                    * portfolio returns
                    * number of firms in each portfolio

            Observation frequency is given by ``freq``. Sample period is from ``dt_start`` to ``dt_end``.
            Rows index time periods, columns index the factors or portfolios.

        dfportSort_characs : pandas.DataFrame, or dict, pandas.DataFrame
            Dataset providing `average` anomaly characteristics for each portfolio
            sorted on a specific set anomaly characteristics. The anomaly characteristics used to sort portfolios
            `NEED NOT` coincide w/ the  `average` anomaly characteristics calculated for each portfolio.
            Observation frequency is given by ``freq``. Sample period is from ``dt_start`` to ``dt_end``.
            Rows index time periods, columns index the portfolios.

        """
        if factorsBool:
            dim, retType = [2, 3], 'vw'
        else:
            if len(args) == 1:
                if type(args[0]) is list:
                    dim, retType = args[0], 'vw'
                else:
                    raise TypeError('\'dim\' is not a list w/ the dimensions for each sort.')
            elif len(args) == 2:
                if (type(args[0]) is list) and (type(args[1]) is str):
                    dim, retType = args[0], args[1]
                else:
                    raise TypeError('\'dim\' is not a list w/ the dimensions for each sort.\n'
                                    '\'retType\' is not a string w/ weighting scheme for portfolio returns.')
            else:
                raise ValueError('len(args) exceeds 2!')


        def get_nyse_characs(df0, idx, dim_for_sorts):
            """
            Construct NYSE breakpoints for an arbitrary dimension of the portfolio sorts.

            Parameters
            ___________
            df0 : pandas.DataFrame
                Dataset w/ NYSE stock returns and characteristics.
            idx : str
                Anomaly characteristic used to sort portfolios.
            dim_for)sort : int
                Num of portfolios constructed on anomaly characteristic `idx`.

            Returns
            ________
            nyse_charac : pandas.DataFrame
                Dataset w/ NYSE breakpoints.

            """
            if dim_for_sorts == 2:
                nyse_charac = df0.groupby(['date'])[idx].median().to_frame().reset_index().rename(columns={idx: idx + '_50'})
                return nyse_charac
            elif dim_for_sorts == 3:
                ptiles = [0.3, 0.7]
                nyse_charac = df0.groupby(['date'])[idx].describe(percentiles=ptiles).reset_index()
                nyse_charac = nyse_charac[['date', '30%', '70%']].rename(columns={'30%': idx + '_30', '70%': idx + '_70'})
                return nyse_charac
            elif dim_for_sorts in [4, 5, 6, 8, 10, 20, 25, 50, 100]:
                ptiles = list(np.around(np.arange(0, 1, round(1/dim_for_sorts, 2)), 2))[1:]
                nyse_charac = df0.groupby(['date'])[idx].describe(percentiles=ptiles).reset_index()
                nyse_charac.columns = [c.strip().replace('.0%', '%') for c in nyse_charac.columns]
                df_cols = {p: idx + '_' + p.strip('%') for p in nyse_charac.columns if '%' in p}
                nyse_charac = nyse_charac[['date'] + [p for p in nyse_charac.columns if '%' in p]].rename(columns=df_cols)
                return nyse_charac
            else:
                raise ValueError('\'dim_for_sorts\' is not a standard type:\n' 
                                 'Choose a value in {2, 3, 4, 5, 6, 8, 10, 20, 25, 50, 100}.')

        def univariateSort(df, id1, dim_sort):
            """
            Construct NYSE breakpoints based on univariate portfolio sorts.

            Parameters
            ___________
            df : pandas.DataFrame
                Dataset w/ NYSE stock returns and characteristics.
            id1 : str
                Anomaly characteristic used to sort portfolios.
            dim_sort : list w/ int
                Num of portfolios constructed on anomaly characteristic `id1`.

            Returns
            ________
            df_breaks : pandas.DataFrame
                Dataset w/ univariate NYSE breakpoints.
            """
            df_breaks = get_nyse_characs(df, id1, dim_sort[0])
            return df_breaks

        def bivariateSort(df, id1, id2, dim_sort):
            """
            Construct NYSE breakpoints based on bivariate portfolio sorts.

            Parameters
            ___________
            df : pandas.DataFrame
                Dataset w/ NYSE stock returns and characteristics.
            id1 : str
                First anomaly characteristic used to sort portfolios.
            id2 : str
                Second anomaly characteristic used to sort portfolios.
            dim_sort : list, int
                Given characteristics `id1` and `id2`, `dim_sort` contains dimensions for sorting on both `id1` and `id2`.
                For example, if ``id1 = ME`` and ``id2 = BM`` w/ ``dim_sort = [5, 5]``, then our sorting strategy
                will consist of a bivariate, quintile sort on `size` and `book-to-market`.

            Returns
            ________
            df_breaks : pandas.DataFrame
                Dataset w/ bivariate NYSE breakpoints.
            """
            nyse_charac1 = get_nyse_characs(df, id1, dim_sort[0])  # Construct NYSE breakpoints for 1st dimension.
            nyse_charac2 = get_nyse_characs(df, id2, dim_sort[1])  # Construct NYSE breakpoints for 2nd dimension.
            df_breaks = nyse_charac1.merge(right=nyse_charac2, how='inner', on=['date'])
            return df_breaks

        def trivariateSort(df, id1, id2, id3, dim_sort):
            """
            Construct NYSE breakpoints based on trivariate portfolio sorts.

            Parameters
            ___________
            df : pandas.DataFrame
                Dataset w/ NYSE stock returns and characteristics.
            id1 : str
                First anomaly characteristic used to sort portfolios.
            id2 : str
                Second anomaly characteristic used to sort portfolios.
            id3 : str
                Third anomaly characteristic used to sort portfolios.
            dim_sort : list, int
                Given characteristics `id1`, `id2`, and `id3`, `dim_sort` contains dimensions for sorting on `id1`, `id2`, and `id3`.
                For example, if ``id1 = ME``, ``id2 = BM``, and ``id3 = OP`` w/ ``dim_sort = [2, 4, 4,]``, then our sorting strategy
                will consist of a trivariate sort on `size`, `book-to-market`, and `operating profitability`  w/:
                 1. `size` split at the median,
                 2. `book-to-market` split into quartiles, and
                 3. `operating profitability` split into quartiles

            Returns
            ________
            df_breaks : pandas.DataFrame
                 Dataset w/ trivariate NYSE breakpoints.
            """
            nyse_charac1 = get_nyse_characs(df, id1, dim_sort[0])  # Construct NYSE breakpoints for 1st dimension.
            nyse_charac2 = get_nyse_characs(df, id2, dim_sort[1])  # Construct NYSE breakpoints for 2nd dimension.
            nyse_charac3 = get_nyse_characs(df, id3, dim_sort[2])  # Construct NYSE breakpoints for 3rd dimension.
            df_breaks = nyse_charac1.merge(right=nyse_charac2, how='inner', on=['date'])
            df_breaks = df_breaks.merge(right=nyse_charac3, how='inner', on=['date'])
            return df_breaks


        def getPortfolioBins(df, id_col, idBool, port_num):
            """
            Given NYSE breakpoints, stocks are allocated into the appropriate portfolio bins.

            Parameters
            ___________
            df : pandas.DataFrame
                Dataset w/ firm variables used in the portfolio allocation process.
            id_col : str
                Column label for the anomaly portfolio characteristic used to allocate stocks into portfolios.
            idBool : str
                Column label for boolean variable determining whether a stock is included or not in a portfolio bin.
            port_num : int
                Num of portfolios constructed using anomaly portfolio characteristic `id_col`.
                `port_num` is one of the following: 2, 3, 4, 5, 6, 8, 10, 20, 25, or 100.

            Returns
            ________
            df : pandas.DataFrame
                Updated `df` w/ additional columns containing portfolio bin identifiers.
            """
            if id_col in ['me', 'be', 'bm', 'dp', 'ni', 'var', 'resvar']:
                df['lbound'] = 0
            else:
                df['lbound'] = -np.inf
            df['ubound'] = np.inf

            if port_num in [2, 3, 4, 5, 6, 8, 10, 20, 25, 100]:
                if port_num == 2:
                    bcond1 = (df[idBool] == True) & (df['lbound'] < df[id_col]) & (df[id_col] <= df[id_col + '_50'])
                    bcond2 = (df[idBool] == True) & (df[id_col + '_50'] < df[id_col]) & (df[id_col] < df['ubound'])
                    binconds = [bcond1, bcond2]
                    bvals = [id_col + '0-50', id_col + '50-100']
                elif port_num == 3:
                    bcond1 = (df[idBool] == True) & (df['lbound'] < df[id_col]) & (df[id_col] <= df[id_col + '_30'])
                    bcond2 = (df[idBool] == True) & (df[id_col + '_30'] < df[id_col]) & (df[id_col] <= df[id_col + '_70'])
                    bcond3 = (df[idBool] == True) & (df[id_col + '_70'] < df[id_col]) & (df[id_col] < df['ubound'])
                    binconds = [bcond1, bcond2, bcond3]
                    bvals = [id_col + '0-30', id_col + '30-70', id_col + '70-100']
                elif port_num in [4, 5, 6, 8, 10, 20, 25, 50, 100]:
                    binconds, bvals = [], []
                    ptiles = list(np.around(np.arange(0, 1, round(1/port_num, 2)), 2))[1:]
                    p_cols = ['_' + c.split('%')[0] for c in [str(int(p*100))+'%' for p in ptiles]]
                    for bin in range(0, port_num):
                        if bin == 0:
                            bcond = (df[idBool] == True) & (df['lbound'] < df[id_col]) & (df[id_col] <= df[id_col + p_cols[bin]])
                            binconds.append(bcond)
                            bvals.append(id_col + '0-'+p_cols[bin].split('_')[1])
                        elif bin == port_num-1:
                            bcond = (df[idBool] == True) & (df[id_col + p_cols[bin-1]] < df[id_col]) & (df[id_col] < df['ubound'])
                            binconds.append(bcond)
                            bvals.append(id_col + p_cols[bin-1].split('_')[1] + '-100')
                        else:
                            bcond = (df[idBool] == True) & (df[id_col + p_cols[bin-1]] < df[id_col]) & (df[id_col] <= df[id_col + p_cols[bin]])
                            binconds.append(bcond)
                            bvals.append(id_col + p_cols[bin-1].split('_')[1] + '-' + p_cols[bin].split('_')[1])

                df[id_col + '_port'] = np.select(binconds, bvals, default='')
                df = df.drop(columns=['lbound', 'ubound'])
                return df
            else:
                raise ValueError('\'port_num\' is not a standard type!')


        def _getNyseThresholds(df1, dfcrsp, fidList, fBool, freq, pDim, *args_):
            """
            Construct dataset(s) w/ factors, portfolio returns, number of firms in portfolios,
            or average anomaly portfolio characteristics observed at a given frequency and over a given sample period
            for a given portfolio sorting strategy.

            Parameters
            ___________
            df1 : pandas.DataFrame
                Dataset w/ anomaly characteristics (used in constructing portfolios at the end of each June)
                obtained from merged Compustat/CRSP datafiles.
            dfcrsp : pandas.DataFrame
                Dataset w/ firm variables observed at frequency `freq` (defined below).
            fidList : list, str
                Contains the factor or list of anomaly portfolio characteristics
                whose naming convention is consistent w/ earlier-described conventions.
            fBool : bool
                Flag for choosing whether to construct a Fama-French factor or not.
                If `True`, then `fidType` (defined below) must be passed as an additional argument and
                `pRetType` = `vw` is the default. Otherwise, `pRetType` must be passed as an additional argument.
            freq : str
                Observation frequency of the portfolios. Possible choices are:
                * ``D`` for daily
                * ``W`` for weekly
                * ``M' for monthly
                * ``Q`` for quarterly (3-months)
                * ``A`` for annual
            pDim : list, int
                Dimensions for sorting on each element in the list ``idList``.
                For example, if ``idList = ['ME', 'BM']`` and ``dim = [2, 3]``, then the portfolio sorting strategy
                is characterized by a bivariate quintile sort on both `size` and `book-to-market` in which
                `size` is split at the median, `book-to-market` is split into three buckets using 30th and 70th percentiles.
            fidType : str, [optional]
                Identifer marking which set of Fama-French factors (between traditional 3-factors and the more recent 5-factors)
                are to be constructed for the purposes of forming ``SMB``. Possible choices are:
                    * ``ff3`` : Fama-French 3 factors
                    * ``ff5`` : Fama-French 5 factors
            pRetType : str, [optional]
                Weighting-scheme for portfolios. Possible choices are:
                    * ``vw`` : value-weights
                    * ``ew`` : equal-weights

            Returns
            ________
            dfportSort_table : pandas.DataFrame or dict, pandas.DataFrames
                Dataset(s) w/ Fama-French factors, portfolio returns, number of firms in each portfolio,
                or average anomaly portfolio characteristics observed at frequency `freq` for a
                given portfolio sorting strategy.
            """
            if fBool:
                fidType = args_[0]
                pRetType = 'vw'
            else:
                pRetType = args_[0]

            # List containing all anomaly characteristics w/ 'PRIOR' in their name (+ the two additional parameters that are required).
            re_prior = compile('PRIOR_' + r'[0-9]+' + '_' + r'[0-9]+')
            prior_list = list(filter(re_prior.search, fidList))

            # Common Boolean Condition #1, sBool1: (exchcd == 1) & shrcd in (10,11)
            # Common Boolean Condition #2, sBool2:  (at least 2 years in 'comp'), & (positive 'me')
            sBool1 = (df1['exchcd'] == 1) & (df1['shrcd'].isin([10, 11]))
            sBool2 = (df1['count'] >= 2) & (df1['me'] > 0)
            if fBool:
                if fidList == 'MKT-RF':
                    ffcharac_list = ['me']
                    # MKT-RF (premium): Require
                    #                   (1) NYSE, AMEX, and Nasdaq stocks,
                    #                   (2) positive lagged 'me,
                    #                   (3) non-missing adjusted returns
                    dfcrsp['sBoolMkt'] = (dfcrsp['exchcd'].isin([1, 2, 3])) & (dfcrsp['shrcd'].isin([10, 11])) & (dfcrsp['lme'] > 0) & (~dfcrsp['retadj'].isnull())
                elif fidList == 'SMB':
                    ffcharac_list = ['me', 'bm']
                    if fidType == 'ff3':
                        df1['sBool'] = sBool1 & sBool2 & (df1['be'] > 0) & (~df1['bm'].isnull())
                    else:
                        df1['sBool'] = sBool1 & sBool2 & (df1['be'] > 0) & (~df1['bm'].isnull()) & (~df1['revt'].isnull()) & (~df1['xp_allnan']) & (~df1['inv'].isnull())
                elif fidList == 'HML':
                    ffcharac_list = ['me', 'bm']
                    df1['sBool'] = sBool1 & sBool2 & (df1['be'] > 0) & (~df1['bm'].isnull())
                elif fidList == 'RMW':
                    ffcharac_list = ['me', 'op']
                    df1['sBool'] = sBool1 & sBool2 & (df1['be'] > 0) & (~df1['bm'].isnull()) & (~df1['revt'].isnull()) & (~df1['xp_allnan'])
                elif fidList == 'CMA':
                    ffcharac_list = ['me', 'inv']
                    df1['sBool'] = sBool1 & sBool2 & (~df1['inv'].isnull())
                elif fidList in ['MOM', 'ST_Rev', 'LT_Rev']:
                    # NOTE: As a reference, see comments inside function 'getMEJune(...)':
                    if fidList == 'MOM':
                        j_month, k_month = '2', '12'
                    elif fidList == 'ST_Rev':
                        j_month, k_month = '1', '1'
                    else:
                        j_month, k_month = '13', '60'
                    j_per, k_per = utils.priormonthToDay(freq, j_month, k_month)
                    ffcharac_list = ['me', 'prior_' + j_month + '_' + k_month]
                    df1['sBool'] = sBool1 & sBool2
                    dfcrsp['sBoolcrsp'] = (dfcrsp['exchcd'] == 1) & (dfcrsp['shrcd'].isin([10, 11])) & \
                                          (~dfcrsp['prior_' + j_month + '_' + k_month].isnull()) & (~dfcrsp['l' + j_per + '_retadj'].isnull())
                    if int(k_per) > 1:
                        dfcrsp['sBoolcrsp'] = dfcrsp['sBoolcrsp'] & (~dfcrsp['l' + k_per + '_retadj'].isnull())
                else:
                    raise ValueError('Unknown factor.')

            else:
                # Initialize boolean for 'df1' w/ any generic column that has all rows set to 'True':
                df1['sBool'] = (df1['exchcd'] == df1['exchcd'])
                ffcharac_list = []
                if 'ME' in fidList:
                    ffcharac_list.append('me')
                    df1['sBool'] = sBool1 & sBool2
                if 'BE' in fidList:
                    ffcharac_list.append('be')
                    df1['sBool'] = df1['sBool'] & sBool1 & (df1['count'] >= 2) & (df1['be'] > 0)
                if 'BM' in fidList:
                    ffcharac_list.append('bm')
                    df1['sBool'] = df1['sBool'] & sBool1 & sBool2 & (df1['be'] > 0) & (~df1['bm'].isnull())
                if 'OP' in fidList:
                    ffcharac_list.append('op')
                    df1['sBool'] = df1['sBool'] & sBool1 & sBool2 & (df1['be'] > 0) & (~df1['revt'].isnull()) & (~df1['xp_allnan'])
                if 'INV' in fidList:
                    ffcharac_list.append('inv')
                    df1['sBool'] = df1['sBool'] & sBool1 & sBool2 & (~df1['inv'].isnull())
                if 'EP' in fidList:
                    ffcharac_list.append('ep')
                    df1['sBool'] = df1['sBool'] & sBool1 & sBool2 & (~df1['me'].isnull()) & (df1['ib'] >= 0)
                if 'CFP' in fidList:
                    ffcharac_list.append('cfp')
                    df1['sBool'] = df1['sBool'] & sBool1 & sBool2 & (~df1['me'].isnull()) & (df1['cf'] >= 0)
                if 'DP' in fidList:
                    ffcharac_list.append('dp')
                    df1['sBool'] = df1['sBool'] & sBool1 & (~df1['me'].isnull()) & (df1['dp'] > 0)
                if 'AC' in fidList:
                    ffcharac_list.append('ac')
                    df1['sBool'] = df1['sBool'] & sBool1 & sBool2 & (df1['be'] > 0) & (~df1['d_owcap_adj'].isnull())
                if 'NI' in fidList:
                    ffcharac_list.append('ni')
                    df1['sBool'] = df1['sBool'] & sBool1 & sBool2 & (df1['ni'] > 0)
                if len(prior_list) != 0:
                    # NOTE: As a reference, see comments inside function 'getMEJune(...)':
                    for c in prior_list:
                        j_month, k_month = c.split('_')[1], c.split('_')[2]
                        j_per, k_per = utils.priormonthToDay(freq, j_month, k_month)
                        ffcharac_list.append('prior_' + j_month + '_' + k_month)

                        df1['sBool'] = df1['sBool'] & sBool1 & (df1['count'] >= 2)
                        dfcrsp['sBoolcrsp'] = (dfcrsp['exchcd'] == 1) & (dfcrsp['shrcd'].isin([10, 11])) & \
                                              (~dfcrsp['prior_' + j_month + '_' + k_month].isnull()) & (~dfcrsp['l' + j_per + '_retadj'].isnull())
                        if int(k_per) > 1:
                            dfcrsp['sBoolcrsp'] = dfcrsp['sBoolcrsp'] & (~dfcrsp['l' + k_per + '_retadj'].isnull())

                if ('BETA' in fidList) and (self.runFactorReg is False):
                    ffcharac_list.append('beta')
                    df1['sBool'] = df1['sBool'] & sBool1 & (df1['me'] > 0) & (~df1['beta'].isnull())

                if ('VAR' in fidList) or (('RESVAR' in fidList) and (self.runFactorReg is False)):
                    if 'VAR' in fidList:
                        vartype = 'var'
                    else:
                        vartype = 'resvar'
                    ffcharac_list.append(vartype)
                    df1['sBool'] = df1['sBool'] & sBool1 & (df1['count'] >= 2)
                    dfcrsp['sBoolcrsp'] = (dfcrsp['exchcd'] == 1) & (dfcrsp['shrcd'].isin([10, 11])) & (dfcrsp['lme'] > 0) & (~dfcrsp[vartype].isnull())

            if fBool and (fidList == 'MKT-RF'):
                # Construct value-weighted market return 'MKT' which includes all CRSP firms incorporated in the US and listed
                # on the NYSE, AMEX, and Nasdaq firms that have CRSP share code 10 or 11 at beginning of period {t},
                # shares and price data at beginning of period {t}, and returns from period {t-1} to period {t}.
                # NOTE: The period here is at the same frequency of the portfolio sorts and/or factors, NOT the period
                #       used to construct NYSE breakpoints for characteristic-based portfolio sorts.
                dfcrsp = dfcrsp[dfcrsp['sBoolMkt']][['date', 'shrcd', 'exchcd', 'retadj', 'lme']]
                dfportSort_ret = utils.grouped_vwAvg(dfcrsp, 'retadj', 'lme', 'date').to_frame().reset_index().rename(columns={'retadj': 'mktport'})

                # Get the total firm count 'num_firms':
                dfportSort_nfirms = dfcrsp.groupby(['date']).size().reset_index().rename(columns={0: 'num_firms'})

                # Remove the following:
                #   (1) Days landing on Saturday/Sunday which are treated as trading days
                #   (2) Fridays that are holidays, but included as trading days
                if freq in ['D', 'W']:
                    dfportSort_ret = dfportSort_ret[(dfportSort_ret['date'].dt.weekday < 5)]
                    dfportSort_nfirms = dfportSort_nfirms[(dfportSort_nfirms['date'].dt.weekday < 5)]

                # Having formed market portfolio a la Fama and French:
                # (1) portfolio returns are then compounded to the proper horizon:
                #     we use exp(sum(ln(1+r_{t}, ..., ln(1+r_{t+H})) - 1 where H corresponds to the horizon.
                # (2) number of firms per portfolio is averaged to the proper horizon
                if freq in ['W', 'Q', 'A']:
                    dfportSort_ret = dfportSort_ret.rename(columns={'date': 'date_crsp'})
                    dfportSort_nfirms = dfportSort_nfirms.rename(columns={'date': 'date_crsp'})
                    if freq == 'W':
                        dfportSort_ret.insert(dfportSort_ret.columns.get_loc('date_crsp') + 1, 'date',
                                              dfportSort_ret['date_crsp'] - pd.to_timedelta((dfportSort_ret['date_crsp'].dt.weekday - 4) % - 7, unit='d'))
                        dfportSort_nfirms.insert(dfportSort_nfirms.columns.get_loc('date_crsp') + 1, 'date',
                                                 dfportSort_nfirms['date_crsp'] - pd.to_timedelta((dfportSort_ret['date_crsp'].dt.weekday - 4) % - 7, unit='d'))

                        # Filter for non-trading NYSE holidays:
                        dfportSort_ret_eow = dfportSort_ret.groupby(['date'])['date_crsp'].max().reset_index().rename(columns={'date_crsp': 'date_eow'})
                        dfportSort_ret = dfportSort_ret.merge(right=dfportSort_ret_eow, how='left', on=['date'])
                        dfportSort_ret = dfportSort_ret.drop(columns=['date']).rename(columns={'date_eow': 'date'})

                        # Delete pandas.DataFrame no longer needed in memory.
                        lst = [dfportSort_ret_eow]
                        del dfportSort_ret_eow
                        del lst

                        dfportSort_nfirms_eow = dfportSort_nfirms.groupby(['date'])['date_crsp'].max().reset_index().rename(columns={'date_crsp': 'date_eow'})
                        dfportSort_nfirms = dfportSort_nfirms.merge(right=dfportSort_nfirms_eow, how='left', on=['date'])
                        dfportSort_nfirms = dfportSort_nfirms.drop(columns=['date']).rename(columns={'date_eow': 'date'})

                        # Delete pandas.DataFrame no longer needed in memory.
                        lst = [dfportSort_nfirms_eow]
                        del dfportSort_nfirms_eow
                        del lst

                    elif freq == 'Q':
                        dfportSort_ret.insert(dfportSort_ret.columns.get_loc('date_crsp') + 1, 'date', dfportSort_ret['date_crsp'] + QuarterEnd(0))
                        dfportSort_nfirms.insert(dfportSort_nfirms.columns.get_loc('date_crsp') + 1, 'date', dfportSort_nfirms['date_crsp'] + QuarterEnd(0))
                    else:
                        dfportSort_ret.insert(dfportSort_ret.columns.get_loc('date_crsp') + 1, 'date', dfportSort_ret['date_crsp'] + YearEnd(0))
                        dfportSort_nfirms.insert(dfportSort_nfirms.columns.get_loc('date_crsp') + 1, 'date', dfportSort_nfirms['date_crsp'] + YearEnd(0))

                        # Since annual data should be for each full calendar year, we exclude data that may be incomplete in a final year.
                        dfportSort_ret = dfportSort_ret[dfportSort_ret['date'].dt.date <= dt_end]
                        dfportSort_nfirms = dfportSort_nfirms[dfportSort_nfirms['date'].dt.date <= dt_end]

                    # Compound returns.
                    dfportSort_ret.insert(dfportSort_ret.columns.get_loc('mktport') + 1, 'ln(1+mktport)', np.log(dfportSort_ret['mktport'] + 1))
                    dfportSort_ret.loc[:, 'mktport'] = np.exp(dfportSort_ret.groupby(['date'])['ln(1+mktport)'].transform(np.sum)) - 1
                    dfportSort_ret = dfportSort_ret.drop_duplicates(subset=['date'], keep='last').drop(columns=['date_crsp', 'ln(1+mktport)'])

                    # Average # of firms within each portfolio.
                    dfportSort_nfirms.loc[:, 'num_firms'] = dfportSort_nfirms.groupby(['date'])['num_firms'].transform(np.mean)
                    dfportSort_nfirms = dfportSort_nfirms.drop_duplicates(subset=['date'], keep='last').drop(columns=['date_crsp'])

                dfportSort_ret.loc[:, 'date'] = dfportSort_ret['date'].dt.date
                dfportSort_nfirms.loc[:, 'date'] = dfportSort_nfirms['date'].dt.date
                dfportSort_ret.set_index('date', inplace=True)
                dfportSort_nfirms.set_index('date', inplace=True)

                # Join 'dfportSort_nfirms' w/ 'dfportSort_ret' into one dataframe table w/ a multiindex.
                dfportSort_ret.columns = pd.MultiIndex.from_product([['Returns'], dfportSort_ret.columns.to_list()])
                dfportSort_nfirms.columns = pd.MultiIndex.from_product([['NumFirms'], dfportSort_nfirms.columns.to_list()])
                dfportSort_table = dfportSort_ret.join(other=dfportSort_nfirms, how='left')
                return dfportSort_table

            else:
                if (len(prior_list) != 0) or (fBool and (fidList in ['MOM', 'ST_Rev', 'LT_Rev'])):
                    # Construct (1) six value-weighted portfolios formed on size and prior returns (2-12, 1-1, or 13-60), OR...
                    #           (2) ten value-weighted portfolios formed on prior returns (2-12, 1-1, or 13-60)
                    # Prior 2-12 returns are used for the momentum factor
                    # Prior 1-1 returns are used for the short-term reversal factor
                    # Prior 13-60 returns are used for the long-term reversal factor.
                    # NOTE: Factors are long winners and short losers, given portfolios sorted on prior (j-k) returns.
                    # NOTE: size (i.e. 'me') is formed each June of year {t}, while prior returns are formed every month {t}
                    #        or every day {t}

                    # Filter annual Compustat data for June of year {t} variables ('me' in df1 is market value of equity for June of year {t})
                    if fBool:
                        cols0 = []
                    else:
                        crsplist = ['me', 'var', 'resvar'] + list(map(str.lower, prior_list))
                        cols0 = [c for c in list(map(str.lower, self.mainCharacsId)) if c not in crsplist]
                    dfcomp_me = df1[['date', 'permno', 'me', 'sBool'] + cols0]
                    dfcomp_me.insert(dfcomp_me.columns.get_loc('permno'), 'ffyear', dfcomp_me['date'].dt.year)
                    dfcomp_me = dfcomp_me.drop(columns=['date'])
                    dfcomp_me_nyse = dfcomp_me[dfcomp_me['sBool']]
                    dfcomp_me_nyse = dfcomp_me_nyse.drop(columns=['sBool'])

                    crsplist = list(set(['var', 'resvar']).intersection(set(list(map(str.lower, self.mainCharacsId)))))
                    # Filter monthly CRSP data for prior (j-k) return characteristics.
                    if int(k_per) > 1:
                        cols_prior = ['l' + str(j_per) + '_retadj', 'l' + str(k_per) + '_retadj', 'prior_' + j_month + '_' + k_month]
                    else:
                        cols_prior = ['l' + str(j_per) + '_retadj', 'prior_' + j_month + '_' + k_month]

                    dfcrsp_prior = dfcrsp[['date', 'permno', 'ffyear', 'shrcd', 'exchcd', 'retadj', 'port_weight', 'me_t',
                                           'sBoolcrsp'] + cols_prior + crsplist]
                    dfcrsp_prior_nyse = dfcrsp_prior[dfcrsp_prior['sBoolcrsp']]
                    dfcrsp_prior_nyse = dfcrsp_prior_nyse.drop(columns=['sBoolcrsp'])

                    # NYSE breakpoints: Merge 'dfcomp_me_nyse' w/ 'dfcrsp_prior_nyse':
                    dfnyse = dfcrsp_prior_nyse.merge(right=dfcomp_me_nyse, how='left', on=['permno', 'ffyear'])

                    # NYSE, AMEX, Nasdaq: Merge 'dfcomp_me' w/ 'dfcrsp_prior':
                    dfccm = dfcrsp_prior.merge(right=dfcomp_me, how='left', on=['permno', 'ffyear'])

                    if fBool:
                        # Construct bivariate buckets corresponding to Fama and French factor portfolio sorts:
                        # 'me' sorts constructed every year (June of year {t})
                        # 'prior (j-k) return' sorts constructed every month {t} (or day {t}).
                        dfnyse_breaks = bivariateSort(df=dfnyse, id1=ffcharac_list[0], id2=ffcharac_list[1], dim_sort=[2, 3])
                    else:
                        if len(pDim) == 1:
                            # Construct univariate bucket corresponding to
                            # 'prior (j-k) return' sorts constructed every month {t} (or day {t}).
                            dfnyse_breaks = univariateSort(df=dfnyse, id1=ffcharac_list[0], dim_sort=pDim)
                        elif len(pDim) == 2:
                            # Construct bivariate buckets corresponding to Fama and French portfolio sorts:
                            # 'me' sorts constructed every year (June of year {t})
                            # 'prior (j-k) return' sorts constructed every month {t} (or day {t}).
                            dfnyse_breaks = bivariateSort(df=dfnyse, id1=ffcharac_list[0], id2=ffcharac_list[1], dim_sort=pDim)
                        else:
                            raise ValueError('len(pDim) exceeds 2!')

                    # NYSE, AMEX, Nasdaq: Merge 'dfnyse_breaks' w/ 'dfccm'
                    df2 = dfccm.merge(right=dfnyse_breaks, how='left', on=['date'])

                elif ('VAR' in fidList) or (('RESVAR' in fidList) and (self.runFactorReg is False)):
                    # We construct either:
                    # (1) Porftolios formed on
                    #     i.  monthly variance of daily returns ('ret_rollover'), or
                    #     ii. monthly variance of daily residuals from FF3 model ('resvar')
                    # OR...
                    # (2) Portfolios formed on
                    #     i.  monthly size ('lme') and variance of daily returns ('ret_rollover'), or
                    #     ii. monthly size ('lme') and variance of daily residuals from FF3 model ('resvar')
                    # NOTE: Both are formed at the end of month {t-1}, hence we use "lagged" size ('lme')
                    # Filter annual Compustat data for June of year {t} variables
                    if fBool:
                        cols0 = []
                    else:
                        crsplist = list(set(['me', 'var', 'resvar']).intersection(set(list(map(str.lower, self.mainCharacsId)))))
                        cols0 = [c for c in list(map(str.lower, self.mainCharacsId)) if c in df1.columns and c not in crsplist]
                    dfcomp_me = df1[['date', 'permno', 'sBool'] + cols0]
                    dfcomp_me.insert(dfcomp_me.columns.get_loc('permno'), 'ffyear', dfcomp_me['date'].dt.year)
                    dfcomp_me = dfcomp_me.drop(columns=['date'])
                    dfcomp_me_nyse = dfcomp_me[dfcomp_me['sBool']]
                    dfcomp_me_nyse = dfcomp_me_nyse.drop(columns=['sBool'])

                    crsplist = list(set(['var', 'resvar']).intersection(set(list(map(str.lower, self.mainCharacsId)))))
                    dfcrsp_var = dfcrsp[['date', 'permno', 'ffyear', 'shrcd', 'exchcd', 'retadj', 'lme', 'me_t', 'sBoolcrsp'] + crsplist]
                    dfcrsp_var = dfcrsp_var.rename(columns={'lme': 'me'})
                    dfcrsp_var_nyse = dfcrsp_var[dfcrsp_var['sBoolcrsp']]
                    dfcrsp_var_nyse = dfcrsp_var_nyse.drop(columns=['sBoolcrsp'])

                    # NYSE breakpoints: Merge 'dfcomp_me_nyse' w/ 'dfcrsp_var_nyse':
                    dfnyse = dfcrsp_var_nyse.merge(right=dfcomp_me_nyse, how='left', on=['permno', 'ffyear'])

                    # NYSE, AMEX, Nasdaq: Merge 'dfcomp_me' w/ 'dfcrsp_prior':
                    dfccm = dfcrsp_var.merge(right=dfcomp_me, how='left', on=['permno', 'ffyear'])

                    if len(pDim) == 1:
                        # Construct univariate bucket corresponding to
                        # "daily variance"/"monthly residual variance" sorts constructed every month {t}.
                        dfnyse_breaks = univariateSort(df=dfnyse, id1=ffcharac_list[0], dim_sort=pDim)
                    elif len(pDim) == 2:
                        # Construct bivariate buckets corresponding to Fama and French portfolio sorts:
                        # 'me' sorts constructed every month {t}
                        # "daily variance"/"monthly residual variance" sorts constructed every month {t}.
                        dfnyse_breaks = bivariateSort(df=dfnyse, id1=ffcharac_list[0], id2=ffcharac_list[1], dim_sort=pDim)
                    else:
                        raise ValueError('len(pDim) exceeds 2!')

                    # NYSE, AMEX, Nasdaq: Merge 'dfccm' w/ 'dfnyse_breaks'.
                    df2 = dfccm.merge(right=dfnyse_breaks, how='left', on=['date'])

                else:
                    # NYSE breakpoints:
                    dfnyse = df1[df1['sBool']]
                    dfnyse = dfnyse.drop(columns=['sBool'])

                    if fBool:
                        # Construct bivariate buckets corresponding to Fama French factor portfolio sorts.
                        dfnyse_breaks = bivariateSort(df=dfnyse, id1=ffcharac_list[0], id2=ffcharac_list[1], dim_sort=[2, 3])
                    else:
                        if len(pDim) == 1:
                            # Construct univariate buckets.
                            dfnyse_breaks = univariateSort(df=dfnyse, id1=ffcharac_list[0], dim_sort=pDim)
                        elif len(pDim) == 2:
                            # Construct bivariate buckets.
                            dfnyse_breaks = bivariateSort(df=dfnyse, id1=ffcharac_list[0], id2=ffcharac_list[1], dim_sort=pDim)
                        elif len(pDim) == 3:
                            # Construct trivariate buckets.
                            dfnyse_breaks = trivariateSort(df=dfnyse, id1=ffcharac_list[0], id2=ffcharac_list[1], id3=ffcharac_list[2], dim_sort=pDim)
                        else:
                            raise ValueError('len(pDim) exceeds 3!')

                    # NYSE, AMEX, Nasdaq: Merge 'dfnyse_breaks' w/ 'df1'.
                    df2 = df1.merge(right=dfnyse_breaks, how='left', on=['date'])

                # Re-define Boolean Condition for 'df2' (includes NYSE, AMEX, and Nasdaq stocks).
                if fBool:
                    if fidList == 'SMB':
                        if fidType == 'ff3':
                            df2['sBool'] = (df2['me'] > 0) & (df2['be'] > 0) & (~df2['bm'].isnull())
                        else:
                            df2['sBool'] = (df2['me'] > 0) & (df2['be'] > 0) & (~df2['bm'].isnull()) & \
                                           (~df2['revt'].isnull()) & (~df2['xp_allnan']) & (~df2['inv'].isnull())
                    elif fidList == 'HML':
                        df2['sBool'] = (df2['me'] > 0) & (df2['be'] > 0) & (~df2['bm'].isnull())
                    elif fidList == 'RMW':
                        df2['sBool'] = (df2['me'] > 0) & (df2['be'] > 0) & (~df2['bm'].isnull()) & (~df2['revt'].isnull()) & (
                            ~df2['xp_allnan'])
                    elif fidList == 'CMA':
                        df2['sBool'] = (df2['me'] > 0) & (~df2['inv'].isnull())
                    elif fidList in ['MOM', 'ST_Rev', 'LT_Rev']:
                        df2['sBool'] = (df2['me'] > 0) & (~df2['prior_' + j_month + '_' + k_month].isnull()) & \
                                       (~df2['l' + j_per + '_retadj'].isnull())
                        if int(k_per) > 1:
                            df2['sBool'] = df2['sBool'] & (~df2['l' + k_per + '_retadj'].isnull())
                    else:
                        raise ValueError('Unknown factor.')
                else:
                    # Initialize boolean for 'df2' w/ any generic column that has all rows set to 'True':
                    df2['sBool'] = (df2['exchcd'] == df2['exchcd'])
                    if 'ME' in fidList:
                        df2['sBool'] = (df2['me'] > 0)
                    if 'BE' in fidList:
                        df2['sBool'] = df2['sBool'] & (df2['be'] > 0)
                    if 'BM' in fidList:
                        df2['sBool'] = df2['sBool'] & (df2['me'] > 0) & (df2['be'] > 0) & (~df2['bm'].isnull())
                    if 'OP' in fidList:
                        df2['sBool'] = df2['sBool'] & (df2['me'] > 0) & (df2['be'] > 0) & (~df2['revt'].isnull()) & (~df2['xp_allnan'])
                    if 'INV' in fidList:
                        df2['sBool'] = df2['sBool'] & (df2['me'] > 0) & (~df2['inv'].isnull())
                    if 'EP' in fidList:
                        df2['sBool'] = df2['sBool'] & (~df2['me'].isnull()) & (df2['ib'] >= 0)
                    if 'CFP' in fidList:
                        df2['sBool'] = df2['sBool'] & (~df2['me'].isnull()) & (df2['cf'] >= 0)
                    if 'DP' in fidList:
                        df2['sBool'] = df2['sBool'] & (~df2['me'].isnull()) & (df2['dp'] > 0)
                    if 'AC' in fidList:
                        df2['sBool'] = df2['sBool'] & (df2['me'] > 0) & (df2['be'] > 0) & (~df2['d_owcap_adj'].isnull())
                    if 'NI' in fidList:
                        df2['sBool'] = df2['sBool'] & (df2['me'] > 0) & (df2['ni'] > 0)
                    if len(prior_list) != 0:
                        # NOTE: As a reference, see comments inside function getMEJune(...):
                        for c in prior_list:
                            j_month, k_month = c.split('_')[1], c.split('_')[2]
                            j_per, k_per = utils.priormonthToDay(freq, j_month, k_month)

                            df2['sBool'] = df2['sBool'] & (~df2['prior_' + j_month + '_' + k_month].isnull()) & (~df2['l' + j_per + '_retadj'].isnull())
                            if int(k_per) > 1:
                                df2['sBool'] = df2['sBool'] & (~df2['l' + k_per + '_retadj'].isnull())

                    if ('BETA' in fidList) and (self.runFactorReg is False):
                        df2['sBool'] = df2['sBool'] & (df2['me'] > 0) & (~df2['beta'].isnull())

                    if ('VAR' in fidList) or (('RESVAR' in fidList) and (self.runFactorReg is False)):
                        df2['sBool'] = df2['sBool'] & (df2['me'] > 0) & (~df2[vartype].isnull())

                df2.loc[:, 'sBool'] = np.where(~df2['sBool'].isnull(), df2['sBool'], False)
                # Get the portfolio bins on the basis of the NYSE thresholds
                for ffcharac in ffcharac_list:
                    idx = ffcharac_list.index(ffcharac)
                    df2 = getPortfolioBins(df2, ffcharac, 'sBool', pDim[idx])

                if fBool:
                    cols0 = []
                else:
                    cols0 = [c for c in list(map(str.lower, self.mainCharacsId))]
                if (len(prior_list) != 0) or (fBool and (fidList in ['MOM', 'ST_Rev', 'LT_Rev'])):
                    # Store portfolio assignments as of June of year {t} (for the period from July of year {t} to June of year {t+1}).
                    df4 = df2[['date', 'permno', 'ffyear', 'shrcd', 'exchcd', 'retadj', 'port_weight', 'me_t', 'sBool'] + \
                              [ffcharac + '_port' for ffcharac in ffcharac_list] + cols0]

                elif ('VAR' in fidList) or (('RESVAR' in fidList) and (self.runFactorReg is False)):
                    cols0 = [x for x in cols0 if x not in ['me', vartype]]
                    df4 = df2[['date', 'permno', 'shrcd', 'exchcd', 'retadj', 'me', 'me_t', vartype, 'sBool'] + \
                              [ffcharac + '_port' for ffcharac in ffcharac_list] + cols0]
                else:
                    # Store portfolio assignments as of June of year {t} (for the period from July of year {t} to June of year {t+1}).
                    cols1 = ['permno', 'date', 'sBool'] + [ffcharac + '_port' for ffcharac in ffcharac_list] + cols0
                    cols2 = ['permno', 'ffyear', 'sBool'] + [ffcharac + '_port' for ffcharac in ffcharac_list] + cols0

                    df3 = df2[cols1]
                    df3.insert(df3.columns.get_loc(cols1[-1]), 'ffyear', df3['date'].dt.year)
                    dfcrsp = dfcrsp[['date', 'permno', 'ffyear', 'shrcd', 'exchcd', 'retadj', 'port_weight', 'me_t']]

                    # 'df4' contains all observations in addition to those from June of year {t}
                    df4 = dfcrsp.merge(right=df3[cols2], how='left', on=['permno', 'ffyear'])

                if ('VAR' in fidList) or (('RESVAR' in fidList) and (self.runFactorReg is False)):
                    port_weight = 'me'
                else:
                    port_weight = 'port_weight'

                # Keep only records that meet the following criteria:
                #   (1) portfolio weights: 'port_weight' (or 'me') > 0
                #   (2) NYSE, AMEX, and NASDAQ firms: 'shrcd' in [10, 11]
                #   (3) value of portfolio's formed on 'sortCharacsId' are non-missing.
                sBool = (df4['sBool'] == True) & (df4[port_weight] > 0) & (df4['shrcd'].isin([10, 11]))
                for ffcharac in ffcharac_list:
                    sBool = sBool & (df4[ffcharac + '_port'] != '') & (~df4[ffcharac + '_port'].isnull())
                df5 = df4[sBool]
                df4, df5 = df4.drop(columns=['sBool']), df5.drop(columns=['sBool'])

                cols1 = ['date'] + [ffcharac + '_port' for ffcharac in ffcharac_list]
                cols_port = '_'.join(ffcharac_list) + '_port'

                if pRetType == 'vw':
                    dfport_ret = utils.grouped_vwAvg(df5, 'retadj', port_weight, cols1).to_frame().reset_index().rename(columns={'retadj': 'vwret'})
                elif pRetType == 'ew':
                    dfport_ret = df5.groupby(cols1)['retadj'].mean().to_frame().reset_index().rename(columns={'retadj': 'ewret'})
                else:
                    raise ValueError('\'pRetType\' is not one of \'wv\' or \'ew\'!')
                dfport_ret[cols_port] = dfport_ret.filter(regex='_port$').apply(lambda x: x.add('_')).sum(axis=1).str.rstrip('_')

                # Average (value-weighted) anomaly characteristics within each portfolio.
                if (fBool is False) and (len(self.mainCharacsId) != 0):
                    def create_pivot_table(df0, charac, weights, groupby_cols, portname):
                        """
                        For each anomaly portfolio characteristic,
                        implement 'pd.pivot()' method in order to spread "rows" into "columns"
                        This routine is executed in a dictionary comprehension.
                        """
                        if charac == 'me':
                            weightType = 'ewavg'
                            dfgroupwavg = df0.groupby(groupby_cols)[charac].mean().to_frame().reset_index().rename(columns={charac: weightType + '_' + charac})
                        else:
                            weightType = 'vwavg'
                            dfgroupwavg = utils.grouped_vwAvg(df0, charac, weights, groupby_cols).to_frame().reset_index().rename(columns={charac: weightType + '_' + charac})
                        dfgroupwavg[portname] = dfgroupwavg.filter(regex='_port$').apply(lambda x: x.add('_')).sum(axis=1).str.rstrip('_')

                        # Remove the following:
                        #   (1) Days landing on Saturday or Sunday which are treated as trading days,
                        #   (2) Fridays that are holidays, but included as trading days
                        if freq in ['D', 'W']:
                            dfgroupwavg = dfgroupwavg[(dfgroupwavg['date'].dt.weekday < 5)]
                        # Having formed portfolios a la Fama and French, collapse monthly value-weighted (vw) or equal-weighted (ew)
                        # characteristics to lower frequency time-averages if freq in ['W', 'Q', 'A'].
                        # NOTE: For the following anomaly characteristics: 'BM', 'OP', 'INV', 'EP', 'CFP', 'DP', 'AC', 'BETA', 'NI',
                        #       annual ('A') vw or ew-average characteristics are defined as vw or ew-average formation-period characteristics
                        #       for each portfolio as of the portfolio formation date in June of year {t}.
                        #       Example: For portfolio "X", the vw or ew-average 'BM' for 1998 is taken to
                        #                be the vw or ew-average 'BM' as of June 1998.
                        # NOTE: For anomaly characteristics: 'PRIOR_1_1', 'PRIOR_2_12', 'PRIOR_13_60', annual ('A') anomaly
                        #       characteristics are average vw or ew-average characteristics within each year {t}.
                        if freq in ['W', 'Q', 'A']:
                            dfgroupwavg = dfgroupwavg.rename(columns={'date': 'date_crsp'})
                            if freq == 'W':
                                # Apply similar procedure when going from daily to weekly equal-weighted 'me', when applicable.
                                dfgroupwavg.insert(dfgroupwavg.columns.get_loc('date_crsp') + 1, 'date',
                                                   dfgroupwavg['date_crsp'] - pd.to_timedelta((dfgroupwavg['date_crsp'].dt.weekday - 4) % - 7, unit='d'))

                                # Collapse days to end of week frequencies.
                                dfgroupwavg_eow = dfgroupwavg.groupby(['date'])['date_crsp'].max().reset_index().rename(columns={'date_crsp': 'date_eow'})
                                dfgroupwavg = dfgroupwavg.merge(right=dfgroupwavg_eow, how='left', on=['date'])
                                dfgroupwavg = dfgroupwavg.drop(columns=['date']).rename(columns={'date_eow': 'date'})

                                # Delete pandas.DataFrame no longer needed in memory.
                                lst = [dfgroupwavg_eow]
                                del dfgroupwavg_eow
                                del lst

                            elif freq == 'Q':
                                dfgroupwavg.insert(dfgroupwavg.columns.get_loc('date_crsp') + 1, 'date', dfgroupwavg['date_crsp'] + QuarterEnd(0))
                            else:
                                dfgroupwavg.insert(dfgroupwavg.columns.get_loc('date_crsp') + 1, 'date', dfgroupwavg['date_crsp'] + YearEnd(0))

                            # NOTE: Annual characteristics are constructed according a la Fama and French:
                            #       (i.e. using the portfolio formation month July within each year {t}).
                            if freq in ['W', 'Q']:
                                # Average value-weighted returns within each year {t}
                                dfgroupwavg = dfgroupwavg.groupby([cols_port, 'date']).mean().reset_index()
                            else:
                                if 'prior' not in charac:
                                    # Keep portfolio-formation period vw or ew-average characteristics (July of each year {t}).
                                    dfgroupwavg = dfgroupwavg[(dfgroupwavg['date_crsp'].dt.month == 7)].sort_values(by=[cols_port, 'date']).reset_index(drop=True)
                                    dfgroupwavg = dfgroupwavg[[cols_port, 'date', weightType + '_' + charac]]
                                else:
                                    # Average value-weighted returns within each year {t}.
                                    dfgroupwavg = dfgroupwavg.groupby([cols_port, 'date']).mean().reset_index()

                                    # Since annual data should be for each full calendar year, we exclude data that may be incomplete in a final year.
                                    dfgroupwavg = dfgroupwavg[dfgroupwavg['date'].dt.date <= dt_end]

                        dfgroupwavgTable = dfgroupwavg.pivot(index='date', columns=cols_port, values=weightType + '_' + charac).reset_index()
                        dfgroupwavgTable.loc[:, 'date'] = dfgroupwavgTable['date'].dt.date
                        dfgroupwavgTable.set_index('date', inplace=True)
                        if charac == 'me':
                            dfgroupwavgTable = dfgroupwavgTable.div(1000)  # USD millions --> USD billions
                        return dfgroupwavgTable

                    # For each value-weighted average anomaly characteristic, 'pd.pivot()' method is used to spread "rows" into "columns"
                    dfportSort_characs = {charac: create_pivot_table(df5, charac.lower(), 'me_t', cols1, cols_port) for charac in set(list(self.mainCharacsId))}

                # Get the total firm count 'num_firms':
                dfport_nfirms = df5.groupby(cols1).size().reset_index().rename(columns={0: 'num_firms'})
                dfport_nfirms[cols_port] = dfport_nfirms.filter(regex='_port$').apply(lambda x: x.add('_')).sum(axis=1).str.rstrip('_')

                # Remove the following:
                #   (1) Days landing on Saturday or Sunday which are treated as trading days,
                #   (2) Fridays that are holidays, but included as trading days
                if freq in ['D', 'W']:
                    dfport_ret = dfport_ret[(dfport_ret['date'].dt.weekday < 5)]
                    dfport_nfirms = dfport_nfirms[(dfport_nfirms['date'].dt.weekday < 5)]

                # Having formed portfolios a la Fama and French:
                #   (1) portfolio returns are then compounded to the proper horizon:
                #       we use exp(sum(ln(1+r_{t}, ..., ln(1+r_{t+H})) - 1 where H corresponds to the horizon.
                #   (2) number of firms per portfolio is averaged to the proper horizon
                if freq in ['W', 'Q', 'A']:
                    dfport_ret = dfport_ret.rename(columns={'date': 'date_crsp'})
                    dfport_nfirms = dfport_nfirms.rename(columns={'date': 'date_crsp'})
                    if freq == 'W':
                        dfport_ret.insert(dfport_ret.columns.get_loc('date_crsp') + 1, 'date',
                                          dfport_ret['date_crsp'] - pd.to_timedelta((dfport_ret['date_crsp'].dt.weekday - 4) % - 7, unit='d'))
                        dfport_nfirms.insert(dfport_nfirms.columns.get_loc('date_crsp') + 1, 'date',
                                             dfport_nfirms['date_crsp'] - pd.to_timedelta((dfport_ret['date_crsp'].dt.weekday - 4) % - 7, unit='d'))

                        # Collapse days to end of week frequencies.
                        dfport_ret_eow = dfport_ret.groupby(['date'])['date_crsp'].max().reset_index().rename(columns={'date_crsp': 'date_eow'})
                        dfport_ret = dfport_ret.merge(right=dfport_ret_eow, how='left', on=['date'])
                        dfport_ret = dfport_ret.drop(columns=['date']).rename(columns={'date_eow': 'date'})

                        # Delete pandas.DataFrame no longer needed in memory.
                        lst = [dfport_ret_eow]
                        del dfport_ret_eow
                        del lst

                        dfport_nfirms_eow = dfport_nfirms.groupby(['date'])['date_crsp'].max().reset_index().rename(columns={'date_crsp': 'date_eow'})
                        dfport_nfirms = dfport_nfirms.merge(right=dfport_nfirms_eow, how='left', on=['date'])
                        dfport_nfirms = dfport_nfirms.drop(columns=['date']).rename(columns={'date_eow': 'date'})

                        # Delete pandas.DataFrame no longer needed in memory.
                        lst = [dfport_nfirms_eow]
                        del dfport_nfirms_eow
                        del lst

                    elif freq == 'Q':
                        dfport_ret.insert(dfport_ret.columns.get_loc('date_crsp') + 1, 'date', dfport_ret['date_crsp'] + QuarterEnd(0))
                        dfport_nfirms.insert(dfport_nfirms.columns.get_loc('date_crsp') + 1, 'date', dfport_nfirms['date_crsp'] + QuarterEnd(0))
                    else:
                        dfport_ret.insert(dfport_ret.columns.get_loc('date_crsp') + 1, 'date', dfport_ret['date_crsp'] + YearEnd(0))
                        dfport_nfirms.insert(dfport_nfirms.columns.get_loc('date_crsp') + 1, 'date', dfport_nfirms['date_crsp'] + YearEnd(0))

                        # Since annual data should be for each full calendar year, we exclude data that may be incomplete in a final year.
                        dfport_ret = dfport_ret[dfport_ret['date'].dt.date <= dt_end]
                        dfport_nfirms = dfport_nfirms[dfport_nfirms['date'].dt.date <= dt_end]

                    # Compound returns.
                    dfport_ret.insert(dfport_ret.columns.get_loc('vwret') + 1, 'ln(1+vwret)', np.log(dfport_ret['vwret'] + 1))
                    dfport_ret.loc[:, 'vwret'] = np.exp(dfport_ret.groupby([cols_port, 'date'])['ln(1+vwret)'].transform(np.sum)) - 1
                    dfport_ret = dfport_ret.drop_duplicates(subset=[cols_port, 'date'], keep='last').drop(columns=['date_crsp', 'ln(1+vwret)'])

                    # Average # of firms within each portfolio.
                    dfport_nfirms.loc[:, 'num_firms'] = dfport_nfirms.groupby([cols_port, 'date'])['num_firms'].transform(np.mean)
                    dfport_nfirms = dfport_nfirms.drop_duplicates(subset=[cols_port, 'date'], keep='last').drop(columns=['date_crsp'])

                # Spread "rows" into "columns" using 'pd.pivot()' method.
                dfportSort_ret = dfport_ret.pivot(index='date', columns=cols_port, values='vwret').reset_index()
                dfportSort_nfirms = dfport_nfirms.pivot(index='date', columns=cols_port, values='num_firms').reset_index()

                dfportSort_ret.loc[:, 'date'] = dfportSort_ret['date'].dt.date
                dfportSort_nfirms.loc[:, 'date'] = dfportSort_nfirms['date'].dt.date
                dfportSort_ret.set_index('date', inplace=True)
                dfportSort_nfirms.set_index('date', inplace=True)

                # Join 'dfportSort_nfirms' w/ 'dfportSort_ret' into one dataframe table w/ a multiindex.
                dfportSort_ret.columns = pd.MultiIndex.from_product([['Returns'], dfportSort_ret.columns.to_list()])
                dfportSort_nfirms.columns = pd.MultiIndex.from_product([['NumFirms'], dfportSort_nfirms.columns.to_list()])
                dfportSort_table = dfportSort_ret.join(other=dfportSort_nfirms, how='left')

                if fBool:
                    return dfportSort_table
                else:
                    return dfportSort_table, dfportSort_characs

        # Market value of equity as of June of year {t}.
        self.mergeCCM(freq, dt_start, dt_end)

        # TODO: Per Fama and French (see Ken French's online documentation):
        # ..."In May 2015, we made two changes in the way we compute daily portfolio returns so the process is
        #     closer to the way we compute monthly portfolio returns. In daily files produced in May 2015 or thereafter,
        #     stocks are dropped from a portfolio immediately after their CRSP delist date;
        #     in files produced before May 2015, those stocks are held until the portfolio is reconstituted, at the end of June.
        #     Also, in daily files produced before May 2015 we exclude a stock from portfolios during any period in which it is
        #     missing prices for more than 10 consecutive trading days; in daily files produced in May 2015 and thereafter,
        #     we exclude a stock if there is no price for more than 200 consecutive trading days."

        if factorsBool:
            if utils.any_in(['CMA', 'RMW'], idList):
                dfportSort_tableList = {
                    fffactor: _getNyseThresholds(self.dfccm_june, self.dfcrsp3, fffactor, True, freq, [2, 3], 'ff5')
                        for fffactor in tqdm(set(idList), desc='Constructing Fama-French return factor(s)', position=0)}

            else:
                # If both 'SMB' & 'HML' are in 'idList', then we don't need to construct the same set of 6 (2x3) portfolios twice!
                if all((f in idList) for f in ['SMB', 'HML']):
                    idList.remove('HML')
                    dfportSort_tableList = {fffactor: _getNyseThresholds(self.dfccm_june, self.dfcrsp3, fffactor, True, freq, [2, 3], 'ff3')
                        for fffactor in tqdm(set(idList), desc='Constructing Fama-French return factor(s)', position=0)}
                    dfportSort_tableList['HML'] = dfportSort_tableList['SMB']
                    idList.append('HML')
                else:
                    dfportSort_tableList = {fffactor: _getNyseThresholds(self.dfccm_june, self.dfcrsp3, fffactor, True, freq, [2, 3], 'ff3')
                        for fffactor in tqdm(set(idList), desc='Constructing Fama-French return factor(s)', position=0)}
            if 'MKT-RF' in idList:
                dfportSort_tableList['MKT'] = dfportSort_tableList.pop('MKT-RF')

            return dfportSort_tableList
        else:
            dfportSort_tableList, dfportSort_characs = _getNyseThresholds(self.dfccm_june, self.dfcrsp3, idList, False, freq, dim, retType)
            return dfportSort_tableList, dfportSort_characs



    def getPortfolios(self, portLevel, factorsBool, freq, dt_start, dt_end, *args):
        """
        Generalized routine used to construct datasets containing portfolio returns (which may include factor returns),
        number of firms in each portfolio, or `average` anomaly portfolio characteristics
        at a given frequency and for a given sample period.  See subroutines for more details.

        Parameters
        ___________
        portLevel : str
            Dataset type to construct. Possible choices are:

                * ``Returns``
                * ``NumFirms``
                * ``Characs``
        factorsBool : bool
            Flag for choosing whether to construct Fama-French factors or not.
            If `True`, then ``portLevel`` must be one of the following: ``Returns``, ``NumFirms``.
            Otherwise, it must be one of the following:

                * ``Returns``
                * ``NumFirms``
                * ``Characs``
        freq : str
            Observation frequency of the portfolios. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start: datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end: datetime.date
            Ending date for the dataset queried or locally retrieved.
        dim : list, int, [optional]
            Dimensions for sorting on each element in the list ``idList``.
            For example, if ``idList = ['ME', 'BM']`` and ``dim = [5, 5]``, then the portfolio sorting strategy
            is characterized by a bivariate quintile sort on both `size` and `book-to-market`.
        retType : str, [optional]
            Weighting-scheme for portfolios. Possible choices are:

                * ``vw`` : value-weights
                * ``ew`` : equal-weights

        Returns
        ________
        portTable : pandas.DataFrame, or dict, pandas.DataFrame
            Dataset(s) w/ portfolio returns (which may include factor returns), number of firms in each portfolio,
            or `average` anomaly portfolio characteristics observed at frequency ``freq``
            over sample period from ``dt_start`` to ``dt_end`` for a given portfolio sorting strategy.
        
        """
        def reorder_columns(df, cols_list):
            cati = pd.CategoricalIndex(df.columns.levels[1], categories=cols_list, ordered=True)
            df.columns.set_levels(cati, level=1, inplace=True)
            df.sort_index(1)
            return df

        if factorsBool:
            if portLevel in ['Returns', 'NumFirms']:
                if self.runFactorReg is False:
                    self.factorsIdtemp = copy.deepcopy(self.factorsId)
                    if ('RMW' in self.factorsId) and ('CMA' not in self.factorsId):
                        self.factorsIdtemp.append('CMA')
                    if ('RMW' not in self.factorsId) and ('CMA' in self.factorsId):
                        self.factorsIdtemp.append('RMW')
                dfportSort_tableList = self.getNyseThresholdsAndRet(self.factorsIdtemp, True, freq, dt_start, dt_end)
                portTable = {}

                if 'MKT-RF' in self.factorsIdtemp:
                    mkt_portTable = dfportSort_tableList['MKT']
                    portTable['MKT'] = mkt_portTable.loc[:, portLevel]

                if utils.any_in(['SMB', 'HML'], self.factorsIdtemp):
                    cols_dict = {'me0-50_bm70-100': 'SMALL LOBM',
                                 'me0-50_bm30-70': 'ME1 BM2',
                                 'me0-50_bm0-30': 'SMALL HIBM',
                                 'me50-100_bm70-100': 'BIG LOBM',
                                 'me50-100_bm30-70': 'ME2 BM2',
                                 'me50-100_bm0-30': 'BIG HIBM'}
                    cols_order = ['SMALL HIBM', 'ME1 BM2', 'SMALL LOBM',
                                  'BIG HIBM', 'ME2 BM2', 'BIG LOBM']
                    if 'SMB' in self.factorsIdtemp:
                        smb_portTable = dfportSort_tableList['SMB']
                        smb_portTable = smb_portTable.rename(columns=cols_dict, level=1)
                        portTable['SMB'] = reorder_columns(smb_portTable, cols_order).loc[:, portLevel]

                    if 'HML' in self.factorsIdtemp:
                        hml_portTable = dfportSort_tableList['HML']
                        hml_portTable = hml_portTable.rename(columns=cols_dict, level=1)
                        portTable['HML'] = reorder_columns(hml_portTable, cols_order).loc[:, portLevel]

                for f in ['RMW', 'CMA', 'MOM', 'ST_Rev', 'LT_Rev']:
                    if f in self.factorsId:
                        if f == 'RMW':
                            flist = ['me', 'op']
                        elif f == 'CMA':
                            flist = ['me', 'inv']
                        elif f == 'MOM':
                            flist = ['me', 'prior_2_12']
                        elif f == 'ST_Rev':
                            flist = ['me', 'prior_1_1']
                        else:
                            flist = ['me', 'prior_13_60']

                        if f in ['CMA', 'ST_Rev', 'LT_Rev']:
                            cols_dict = {'me0-50_' + flist[1] + '0-30': 'SMALL LO' + flist[1].upper(),
                                         'me0-50_' + flist[1] + '30-70': 'ME1 ' + flist[1].upper() + '2',
                                         'me0-50_' + flist[1] + '70-100': 'SMALL HI' + flist[1].upper(),
                                         'me50-100_' + flist[1] + '0-30': 'BIG LO' + flist[1].upper(),
                                         'me50-100_' + flist[1] + '30-70': 'ME2 ' + flist[1].upper() + '2',
                                         'me50-100_' + flist[1] + '70-100': 'BIG HI' + flist[1].upper()}
                            cols_order = ['SMALL LO' + flist[1].upper(), 'ME1 ' + flist[1].upper() + '2',
                                          'SMALL HI' + flist[1].upper(),
                                          'BIG LO' + flist[1].upper(), 'ME2 ' + flist[1].upper() + '2',
                                          'BIG HI' + flist[1].upper()]
                            fportTable = dfportSort_tableList['CMA']
                            fportTable = fportTable.rename(columns=cols_dict, level=1)
                            portTable['CMA'] = reorder_columns(fportTable, cols_order).loc[:, portLevel]

                        else:
                            cols_dict = {'me0-50_' + flist[1] + '70-100': 'SMALL HI' + flist[1].upper(),
                                         'me0-50_' + flist[1] + '30-70': 'ME1 ' + flist[1].upper() + '2',
                                         'me0-50_' + flist[1] + '0-30': 'SMALL LO' + flist[1].upper(),
                                         'me50-100_' + flist[1] + '70-100': 'BIG HI' + flist[1].upper(),
                                         'me50-100_' + flist[1] + '30-70': 'ME2 ' + flist[1].upper() + '2',
                                         'me50-100_' + flist[1] + '0-30': 'BIG LO' + flist[1].upper()}
                            cols_order = ['SMALL HI' + flist[1].upper(), 'ME1 ' + flist[1].upper() + '2',
                                          'SMALL LO' + flist[1].upper(),
                                          'BIG HI' + flist[1].upper(), 'ME2 ' + flist[1].upper() + '2',
                                          'BIG LO' + flist[1].upper()]
                            fportTable = dfportSort_tableList[f]
                            fportTable = fportTable.rename(columns=cols_dict, level=1)
                            portTable[f] = reorder_columns(fportTable, cols_order).loc[:, portLevel]
                return portTable

            else:
                raise ValueError('\'portLevel\' is not one of \'Returns\' or \'NumFirms\'.')
        else:
            if portLevel == 'Returns':
                if (type(args[0]) is list) and (type(args[1]) is str):
                    dim, retType = args[0], args[1]
                    dfportSort_tableList, _ = self.getNyseThresholdsAndRet(self.sortCharacsId, False, freq, dt_start, dt_end, dim, retType)
                    portTable = dfportSort_tableList.loc[:, 'Returns']
                    return portTable
                else:
                    raise TypeError('\'dim\' is not a list w/ the dimensions for each sort.\n'
                                    '\'retType\' is not a string w/ weighting scheme for portfolio returns.')

            elif portLevel == 'NumFirms':
                if type(args[0]) is list:
                    dim = args[0]
                    dfportSort_tableList, _ = self.getNyseThresholdsAndRet(self.sortCharacsId, False, freq, dt_start, dt_end, dim)
                    portTable = dfportSort_tableList.loc[:, 'NumFirms']
                    return portTable
                else:
                    raise TypeError('\'dim\' is not a list w/ the dimensions for each sort.')

            elif portLevel == 'Characs':
                if type(args[0]) is list:
                    dim = args[0]
                    _, dfportSort_characs = self.getNyseThresholdsAndRet(self.sortCharacsId, False, freq, dt_start, dt_end, dim)
                    portTable = dfportSort_characs
                    return portTable
                else:
                    raise TypeError('\'dim\' is not a list w/ the dimensions for each sort.')
            else:
                raise ValueError('\'portLevel\' is not one of \'Returns\', \'NumFirms\', or \'Characs\'.')



    def getPortfolioReturns(self, factorsBool, dt_start, dt_end, *args):
        """
        Construct dataset w/ portfolio returns (which may include factor returns)
        at a given frequency and for a given sample period.

        Parameters
        ___________
        factorsBool : bool
            Flag for choosing whether to construct Fama-French-style factor returns or not.
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.
        pDim : list, int, [optional]
            Dimensions for sorting on each element in the list ``self.sortCharacsId``.
        pRetType : str, [optional]
            Weighting-scheme for portfolios. Possible choices are:

                * ``vw`` : value-weights
                * ``ew`` : equal-weights

        Returns
        ________
        portRetTable: pandas.DataFrame
            Dataset w/ portfolio returns observed at frequency ``self.freqType``
            over sample period from ``dt_start`` to ``dt_end`` for a given portfolio sorting strategy.
        
        Note
        _____
        Portfolios require anomaly characteristics from the last fiscal year.
        To get non-missing observations starting on date ``dt_start``, we construct portfolios using a startdate that is two/three years prior to ``dt_start``.
        We then slice the resulting pandas.DataFrames starting w/ ``dt_start``.
        """
        # Check if 'dt_start' and/or 'dt_end' are trading dates:
        # If they are, leave as is, else, get the trading date after 'dt_start' and/or the trading date before 'dt_end'
        check_start = nyse_cal.schedule(start_date=dt_start, end_date=dt_start)
        check_end = nyse_cal.schedule(start_date=dt_end, end_date=dt_end)
        if len(check_start) == 0:
            dt_start = (dt_start + BDay(1)).date()
        if len(check_end) == 0:
            dt_end = (dt_end - BDay(1)).date()

        if factorsBool:
            portRetTable = self.getPortfolios('Returns', True, self.freqType, dt_start - relativedelta(years=3), dt_end)
            portRetTable = portRetTable.loc[dt_start:]
            return portRetTable
        else:
            if (type(args[0]) is list) and (type(args[1]) is str):
                pDim, pRetType = args[0], args[1]
                if len(pDim) != len(self.sortCharacsId):
                    raise Error('Need # of elements in \'pDim\' to match the # of elements in \'sortCharacsId \'!')
                else:
                    portRetTable = self.getPortfolios('Returns', False, self.freqType, dt_start - relativedelta(years=3), dt_end, pDim, pRetType)
                    portRetTable = portRetTable.loc[dt_start:]
                    return portRetTable
            else:
                raise TypeError('\'pDim\' is not a list w/ the dimensions for each sort.\n'
                                '\'pRetType\' is not a string w/ weighting scheme for portfolio returns.')



    def getNumFirms(self, factorsBool, dt_start, dt_end, *args):
        """
        Construct dataset w/ number of firms in each portfolio at a given frequency and for a given sample period.

        Parameters
        ___________
        factorsBool : bool
            Flag for choosing whether to construct Fama-French-style factors or not.
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.
        pDim : list, int, [optional]
            Dimensions for sorting on each element in the list ``self.sortCharacsId``.

        Returns
        ________
        portNFirmsTable : pandas.DataFrame
             Dataset w/ number of firms in each portfolio observed at frequency ``self.freqType``
             over sample period from ``dt_start`` to ``dt_end`` for a given portfolio sorting strategy.

        Note
        ____
        If ``factorsBool = True``, then the number of firms for the following anomaly/risk-based factors is defined as follows:

            * ``MKT`` : total number of firms (each period) in the market portfolio.
            * ``SMB``, ``HML``, ``RMW``, ``RMWc``, ``CMA``, ``MOM``, ``ST_Rev``, ``LT_Rev`` : total number of firms (each period) in all portfolios used to construct the factors.

        Note
        _____
        Portfolios require anomaly characteristics from the last fiscal year.
        To get non-missing observations starting on date ``dt_start``, we construct portfolios using a startdate that is two/three years prior to ``dt_start``.
        We then slice the resulting pandas.DataFrames starting w/ ``dt_start``.
        """
        # Check if 'dt_start' and/or 'dt_end' are trading dates:
        # If they are, leave as is, else, get the trading date after 'dt_start' and/or the trading date before 'dt_end'
        check_start = nyse_cal.schedule(start_date=dt_start, end_date=dt_start)
        check_end = nyse_cal.schedule(start_date=dt_end, end_date=dt_end)
        if len(check_start) == 0:
            dt_start = (dt_start + BDay(1)).date()
        if len(check_end) == 0:
            dt_end = (dt_end - BDay(1)).date()

        if factorsBool:
            portNFirmsTable = self.getPortfolios('NumFirms', True, self.freqType, dt_start - relativedelta(years=3), dt_end)
            portNFirmsTable = portNFirmsTable.loc[dt_start:]
            return portNFirmsTable
        else:
            if type(args[0]) is list:
                pDim = args[0]
                if len(pDim) != len(self.sortCharacsId):
                    raise Error('Need # of elements in \'pDim\' to match the # of elements in \'sortCharacsId \'!')
                else:
                    portNFirmsTable = self.getPortfolios('NumFirms', False, self.freqType, dt_start - relativedelta(years=3), dt_end, pDim)
                    portNFirmsTable = portNFirmsTable.loc[dt_start:]
                    return portNFirmsTable
            else:
                raise TypeError('\'pDim\' is not a list w/ the dimensions for each sort.')


    def getCharacs(self, factorsBool, dt_start, dt_end, *args):
        """
        Construct `average` anomaly portfolio characteristics at a given frequency and for a given sample period.

        Parameters
        ___________
        factorsBool : bool
            Flag for choosing whether to construct Fama-French-style factors or not.
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.
        pDim : list, int, [optional]
            Dimensions for sorting on each element in the list ``self.sortCharacsId``.

        Returns
        ________
        portCharacsTable: pandas.DataFrame or dict, pandas.DataFrame
            Dataset w/ `average` portfolio characteristics observed at frequency ``self.freqType``
            over sample period from ``dt_start`` to ``dt_end`` for a given portfolio sorting strategy.

        Note
        _____
        Portfolios require anomaly characteristics from the last fiscal year.
        To get non-missing observations starting on date ``dt_start``, we construct portfolios using a startdate that is two/three years prior to ``dt_start``.
        We then slice the resulting pandas.DataFrames starting w/ ``dt_start``.
        """
        # Check if 'dt_start' and/or 'dt_end' are trading dates:
        # If they are, leave as is, else, get the trading date after 'dt_start' and/or the trading date before 'dt_end'
        check_start = nyse_cal.schedule(start_date=dt_start, end_date=dt_start)
        check_end = nyse_cal.schedule(start_date=dt_end, end_date=dt_end)
        if len(check_start) == 0:
            dt_start = (dt_start + BDay(1)).date()
        if len(check_end) == 0:
            dt_end = (dt_end - BDay(1)).date()

        if factorsBool:
            raise ValueError('Value-weighted average characteristics can\'t be obtained when \'factorsBool\' is True.')
        else:
            if type(args[0]) is list:
                pDim = args[0]
                if len(pDim) != len(self.sortCharacsId):
                    raise Error('Need # of elements in \'pDim\' to match the # of elements in \'sortCharacsId \'!')
                else:
                    portCharacsTable = self.getPortfolios('Characs', False, self.freqType, dt_start - relativedelta(years=3), dt_end, pDim)
                    for charac in list(self.mainCharacsId):
                        portCharacsTable[charac] = portCharacsTable[charac].loc[dt_start:]
                    return portCharacsTable
            else:
                raise TypeError('\'pDim\' is not a list w/ the dimensions for each sort.')



    def getFFfactors(self, dt_start, dt_end):
        """
        Construct dataset w/  Fama-French-style factors at a given frequency and for a given sample period.

        Parameters
        ___________
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.

        Returns
        ________
        ffFactorsTable: pandas.DataFrame
            Dataset with set of Fama-French-style factors observed at frequency ``self.freqType``
            over sample period from ``dt_start`` to ``dt_end``.

        Note
        _____
        Portfolios require anomaly characteristics from the last fiscal year.
        To get non-missing observations starting on date ``dt_start``, we construct portfolios using a startdate that is two/three years prior to ``dt_start``.
        We then slice the resulting pandas.DataFrames starting w/ ``dt_start``.
        """
        # Check if 'dt_start' and/or 'dt_end' are trading dates:
        # If they are, leave as is, else, get the trading date after 'dt_start' and/or the trading date before 'dt_end'
        check_start = nyse_cal.schedule(start_date=dt_start, end_date=dt_start)
        check_end = nyse_cal.schedule(start_date=dt_end, end_date=dt_end)
        if len(check_start) == 0:
            dt_start = (dt_start + BDay(1)).date()
        if len(check_end) == 0:
            dt_end = (dt_end - BDay(1)).date()

        self.factorsIdtemp = copy.deepcopy(self.factorsId)
        if ('RMW' in self.factorsId) & ('CMA' not in self.factorsId):
            self.factorsIdtemp.append('CMA')
        if ('RMW' not in self.factorsId) & ('CMA' in self.factorsId):
            self.factorsIdtemp.append('RMW')
        dfportSort_tableList = self.getNyseThresholdsAndRet(self.factorsIdtemp, True, self.freqType, dt_start - relativedelta(years=3), dt_end)
        ffFactorsTable = pd.DataFrame()

        if 'MKT-RF' in self.factorsId:
            ffFactorsTable['mkt'] = dfportSort_tableList['MKT'].loc[:, ('Returns', 'mktport')]
            ffFactorsTable = ffFactorsTable.join(other=self.queryrf1m(self.freqType, dt_start - relativedelta(years=3), dt_end), how='left')
            ffFactorsTable['mkt-rf'] = ffFactorsTable['mkt'] - ffFactorsTable['rf']
            ffFactorsTable = ffFactorsTable.drop(columns=['rf'])

        if (utils.any_in(['CMA', 'RMW'], self.factorsId) is False) and ('SMB' in self.factorsId):
            ffFactorsTable['smb'] = utils.portRetAvg(dfportSort_tableList['SMB'].loc[:, ('Returns', ('me0-50_bm70-100', 'me0-50_bm30-70', 'me0-50_bm0-30'))]) - \
                                    utils.portRetAvg(dfportSort_tableList['SMB'].loc[:, ('Returns', ('me50-100_bm70-100', 'me50-100_bm30-70', 'me50-100_bm0-30'))])
        else:
            if 'SMB' in self.factorsId:
                ffFactorsTable['SMB_bm'] = utils.portRetAvg(dfportSort_tableList['SMB'].loc[:, ('Returns', ('me0-50_bm70-100', 'me0-50_bm30-70', 'me0-50_bm0-30'))]) - \
                                           utils.portRetAvg(dfportSort_tableList['SMB'].loc[:, ('Returns', ('me50-100_bm70-100', 'me50-100_bm30-70', 'me50-100_bm0-30'))])
                ffFactorsTable['SMB_op'] = utils.portRetAvg(dfportSort_tableList['RMW'].loc[:, ('Returns', ('me0-50_op70-100', 'me0-50_op30-70', 'me0-50_op0-30'))]) - \
                                           utils.portRetAvg(dfportSort_tableList['RMW'].loc[:, ('Returns', ('me50-100_op70-100', 'me50-100_op30-70', 'me50-100_op0-30'))])
                ffFactorsTable['SMB_inv'] = utils.portRetAvg(dfportSort_tableList['CMA'].loc[:, ('Returns', ('me0-50_inv0-30', 'me0-50_inv30-70', 'me0-50_inv70-100'))]) - \
                                            utils.portRetAvg(dfportSort_tableList['CMA'].loc[:, ('Returns', ('me50-100_inv0-30', 'me50-100_inv30-70', 'me50-100_inv70-100'))])
                ffFactorsTable['smb'] = utils.portRetAvg(ffFactorsTable.loc[:, ['SMB_bm', 'SMB_op', 'SMB_inv']])
                ffFactorsTable = ffFactorsTable.drop(columns=['SMB_bm', 'SMB_op', 'SMB_inv'])

        for f in ['HML', 'RMW', 'CMA', 'MOM', 'ST_Rev', 'LT_Rev']:
            if f in self.factorsId:
                if f == 'HML':
                    flist = ['me', 'bm']
                elif f == 'RMW':
                    flist = ['me', 'op']
                elif f == 'CMA':
                    flist = ['me', 'inv']
                elif f == 'MOM':
                    flist = ['me', 'prior_2_12']
                elif f == 'ST_Rev':
                    flist = ['me', 'prior_1_1']
                else:
                    flist = ['me', 'prior_13_60']

                if f in ['CMA', 'ST_Rev', 'LT_Rev']:
                    ffFactorsTable[f.lower()] = utils.portRetAvg(dfportSort_tableList[f].loc[:, ('Returns', (flist[0] + '0-50_' + flist[1] + '0-30', flist[0] + '50-100_' + flist[1] + '0-30'))]) - \
                                                utils.portRetAvg(dfportSort_tableList[f].loc[:, ('Returns', (flist[0] + '0-50_' + flist[1] + '70-100', flist[0] + '50-100_' + flist[1] + '70-100'))])
                else:
                    ffFactorsTable[f.lower()] = utils.portRetAvg(dfportSort_tableList[f].loc[:, ('Returns', (flist[0] + '0-50_' + flist[1] + '70-100', flist[0] + '50-100_' + flist[1] + '70-100'))]) - \
                                                utils.portRetAvg(dfportSort_tableList[f].loc[:, ('Returns', (flist[0] + '0-50_' + flist[1] + '0-30', flist[0] + '50-100_' + flist[1] + '0-30'))])

        ffFactorsTable = ffFactorsTable.loc[dt_start:]
        return ffFactorsTable



    def getFamaFrenchStats(self, dataType, dataFreq, dt_start, dt_end, *args):
        """
        Detailed summary statistics tables of portfolio returns (which may include factor returns),
        number of firms in each portfolio, or `average` anomaly portfolio characteristics
        at a given frequency and for a given sample period.

        Parameters
        ___________
        dataType : str
            Dataset type to construct. Possible choices are:

                * ``Returns``
                * ``Factors``
                * ``NumFirms``
                * ``Characs``
        dataFreq : str
            Observation frequency of the portfolios. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start: datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end: datetime.date
            Ending date for the dataset queried or locally retrieved.
        pDim : list, int, [optional]
            Dimensions for sorting on each element in the list ``idList``.
            For example, if ``idList = ['ME', 'BM']`` and ``dim = [5, 5]``, then the portfolio sorting strategy
            is characterized by a bivariate quintile sort on both `size` and `book-to-market`.
        pRetType : str, [optional]
            Weighting-scheme for portfolios. Possible choices are:

                * ``vw`` : value-weights
                * ``ew`` : equal-weights

        Returns
        ________
        None

        Note
        _____
        Currently, this method **only** prints out a table w/ detailed summary statistics. Future versions of the package will
        provide more in-depth statistical analysis and their outputs.

        Note
        _____
        Portfolios require anomaly characteristics from the last fiscal year.
        To get non-missing observations starting on date ``dt_start``, we construct portfolios using a startdate that is two/three years prior to ``dt_start``.
        We then slice the resulting pandas.DataFrames starting w/ ``dt_start``.
        """
        # Check if 'dt_start' and/or 'dt_end' are trading dates:
        # If they are, leave as is, else, get the trading date after 'dt_start' and/or the trading date before 'dt_end'
        check_start = nyse_cal.schedule(start_date=dt_start, end_date=dt_start)
        check_end = nyse_cal.schedule(start_date=dt_end, end_date=dt_end)
        if len(check_start) == 0:
            dt_start = (dt_start + BDay(1)).date()
        if len(check_end) == 0:
            dt_end = (dt_end - BDay(1)).date()

        if dataType == 'Factors':
            factorsTable = self.getFFfactors(dt_start - relativedelta(years=3), dt_end) * 100
            factorsTable = factorsTable.loc[dt_start:]
            print('*********************************** Summary Statistics: Fama-French Factors ***********************************')
            _ = utils.get_statsTable(dataType, dataFreq, factorsTable)
        elif dataType in ['Returns', 'NumFirms', 'Characs']:
            if dataType in ['NumFirms', 'Characs']:
                pDim, pRetType = args[0], None
            else:
                pDim, pRetType = args[0], args[1]

            if dataType == 'Returns':
                returnsTable = self.getPortfolioReturns(False, dt_start - relativedelta(years=3), dt_end, pDim, pRetType)
                returnsTable = returnsTable.loc[dt_start:]
                print('*********************************** Summary Statistics: Portfolio Returns ***********************************')
                print('          *********************************** ' + ' x '.join(self.sortCharacsId) + ' (' + ' x '.join(str(d) for d in pDim) + ') ************************************\n')
                _ = utils.get_statsTable(dataType, dataFreq, returnsTable)
            elif dataType == 'NumFirms':
                firmsTable = self.getNumFirms(False, dt_start - relativedelta(years=3), dt_end, pDim)
                firmsTable = firmsTable.loc[dt_start:]
                print('*********************************** Summary Statistics: Number of Firms ***********************************')
                print('          *********************************** ' + ' x '.join(self.sortCharacsId) + ' (' + ' x '.join(str(d) for d in pDim) + ') ************************************\n')
                _ = utils.get_statsTable(dataType, dataFreq, firmsTable)
            else:
                characsTable = self.getCharacs(False, dt_start - relativedelta(years=3), dt_end, pDim)
                print('*********************************** Summary Statistics: Firm Characteristics ***********************************')
                print('          *********************************** ' + ' x '.join(self.sortCharacsId) + ' (' + ' x '.join(str(d) for d in pDim) + ') ************************************\n')
                for c in list(self.mainCharacsId):
                    print('   ************************** (Characteristic: ' + c + ') ***************************')
                    characsTable[c] = characsTable[c].loc[dt_start:]
                    _ = utils.get_statsTable(dataType, dataFreq, characsTable[c])
        else:
            raise ValueError('\'dataType\' is not one of \'Returns\', \'Factors\', \'NumFirms\', or \'Characs\'.')
        return None



    def kfLibrary(self, kfType, kfFreq, dt_start, dt_end, *args, printkfName=False):
        """
        Generalized routine used to query datasets from Ken French's online library
        at a given frequency and for a given sample period. See subroutines for more details.

        Parameters
        ___________
        kfType : str
            Dataset type to query. Possible choices are:

                * ``Returns``
                * ``Factors``
                * ``NumFirms``
                * ``Characs``
        kfFreq : str
            Observation frequency of the portfolios. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.
        kfDim : list, int, [optional]
            Dimensions for sorting on each element in the list ``self.sortCharacsId``.
        kfRetType : str, [optional]
            Weighting-scheme for portfolios. Possible choices are:

                * ``vw`` : value-weights
                * ``ew`` : equal-weights
        printkfName : bool
            Flag for choosing whether to print or not print the specific name of Ken French's data filename.


        Returns
        ________
        dfkf : pandas.DataFrame
            Cleaned dataset queried from Ken French's online library containing Fama-French-style factors,
            portfolio returns, number of firms in each portfolio, or `average` anomaly portfolio characteristics
            observed at frequency ``kfFreq`` over sample period from ``dt_start`` to ``dt_end``
            for a given portfolio sorting strategy.
        """

        def capitalize_nth(s, n):
            return s[:n].lower() + s[n:].capitalize()

        # Map 'kfFreq' to appropriate string in the online library file names.
        if kfType in ['Returns', 'Factors', 'NumFirms', 'Characs']:
            if kfFreq == 'D':
                freq_kf = '_daily'
            elif kfFreq == 'W':
                freq_kf = '_weekly'
            elif kfFreq in ['M', 'A']:
                freq_kf = ''
            else:
                raise ValueError('Ken French library: \'kfFreq\' is not a standard type.\n '
                                 'Please specify one of the following: \'D\', \'W\', \'M\', or \'A\'')
        else:
            raise ValueError('Ken French library: \'kfType\' is not one of \'Returns\', \'Factors\', \'NumFirms\', or \'Characs\'.')

        if kfType == 'Factors':
            if utils.any_in(['CMA', 'RMW'], self.factorsId) is False:
                kfDataset = 'F-F_Research_Data_Factors' + freq_kf
                dfkf_dict = web.DataReader(kfDataset, 'famafrench', dt_start)
                if kfFreq == 'A':
                    dfkf = (dfkf_dict[1].replace(-99.99, np.nan)) / 100  # % --> decimals
                else:
                    dfkf = (dfkf_dict[0].replace(-99.99, np.nan)) / 100  # % --> decimals
            else:
                kfDataset = 'F-F_Research_Data_5_Factors_2x3' + freq_kf
                dfkf_dict = web.DataReader(kfDataset, 'famafrench', dt_start)
                if kfFreq == 'A':
                    dfkf = (dfkf_dict[1].replace(-99.99, np.nan)) / 100  # % --> decimals
                else:
                    dfkf = (dfkf_dict[0].replace(-99.99, np.nan)) / 100  # % --> decimals

            if 'MKT-RF' in self.factorsId:
                dfkf['MKT'] = dfkf['Mkt-RF'] + dfkf['RF']
                dfkf['MKT-RF'] = dfkf['Mkt-RF']

            if 'MOM' in self.factorsId:
                # Need try-except block since pandas-datareader.web has had issues in the past
                # pulling certain datasets from Ken French's online data library.
                # TODO: Verify if this issue has been resolved by pandas-datareader (see github)
                from dateutil.parser._parser import ParserError
                kfDataset = 'F-F_Momentum_Factor' + freq_kf
                try:
                    dfkf_dict = web.DataReader(kfDataset, 'famafrench', dt_start)
                    if kfFreq == 'A':
                        dfkf['MOM'] = (dfkf_dict[1].replace(-99.99, np.nan)) / 100  # % --> decimals
                    else:
                        dfkf['MOM'] = (dfkf_dict[0].replace(-99.99, np.nan)) / 100  # % --> decimals
                except (TypeError, ParserError):
                    dfkf['MOM'] = utils.get_kfpriorfactors_directly(kfDataset, kfFreq, 'MOM') / 100  # % --> decimals

            if 'ST_Rev' in self.factorsId:
                # Need try-except block since pandas-datareader.web has had issues in the past
                # pulling certain datasets from Ken French's online data library.
                # TODO: Verify if this issue has been resolved by pandas-datareader (see github)
                from dateutil.parser._parser import ParserError
                kfDataset = 'F-F_ST_Reversal_Factor' + freq_kf
                try:
                    dfkf_dict = web.DataReader(kfDataset, 'famafrench', dt_start)
                    if kfFreq == 'A':
                        dfkf['ST_Rev'] = (dfkf_dict[1].replace(-99.99, np.nan)) / 100  # % --> decimals
                    else:
                        dfkf['ST_Rev'] = (dfkf_dict[0].replace(-99.99, np.nan)) / 100  # % --> decimals
                except (TypeError, ParserError):
                    dfkf['ST_Rev'] = utils.get_kfpriorfactors_directly(kfDataset, kfFreq, 'ST_Rev') / 100  # % --> decimals

            if 'LT_Rev' in self.factorsId:
                # Need try-except block since pandas-datareader.web has had issues in the past
                # pulling certain datasets from Ken French's online data library.
                # TODO: Verify if this issue has been resolved by pandas-datareader (see github)
                from dateutil.parser._parser import ParserError
                kfDataset = 'F-F_LT_Reversal_Factor' + freq_kf
                try:
                    dfkf_dict = web.DataReader(kfDataset, 'famafrench', dt_start)
                    if kfFreq == 'A':
                        dfkf['LT_Rev'] = (dfkf_dict[1].replace(-99.99, np.nan)) / 100  # % --> decimals
                    else:
                        dfkf['LT_Rev'] = (dfkf_dict[0].replace(-99.99, np.nan)) / 100  # % --> decimals
                except (TypeError, ParserError):
                    dfkf['LT_Rev'] = utils.get_kfpriorfactors_directly(kfDataset, kfFreq, 'LT_Rev') / 100  # % --> decimals

            if 'MKT-RF' in self.factorsId:
                dfkf = dfkf[['MKT'] + self.factorsId]
            else:
                dfkf = dfkf[self.factorsId]

            # Adjust index if frequency is daily or weekly.
            if kfFreq in ['D', 'W']:
                if kfFreq == 'W':
                    # NOTE: Ken French's weekly datasets provide incorrect dates for some weeks prior to 1953.
                    #       Specifically, some weeks end on a Saturday, instead of the correct trading weekday.
                    #       An adjustment is made to correct for the error, assuming the only mistake is in the
                    #       the weekly dates provided by Ken French and not how the daily returns are cumulated
                    #       for the aforementioned weeks.
                    dfkf.index = np.where(dfkf.index.day_name().isin(['Saturday', 'Sunday']), dfkf.index - BDay(1), dfkf.index)

                    # NYSE trading day holiday calendar
                    nyse_holidays = pd.DataFrame(nyse_cal.holidays().holidays, columns=['nyse_date'])
                    nyse_holidays = nyse_holidays[(dt_start <= nyse_holidays['nyse_date'].dt.date) & (dt_end >= nyse_holidays['nyse_date'].dt.date)]['nyse_date'].dt.date.tolist()
                    dfkf.index = np.where(dfkf.index.isin(nyse_holidays), dfkf.index - BDay(1), dfkf.index)
                dfkf.index = pd.to_datetime(dfkf.index).date
            else:
                dfkf.index = dfkf.index.to_timestamp(kfFreq).date
            dfkf.columns = dfkf.columns.str.lower()
            dfkf = dfkf.loc[dt_start:dt_end]
            return dfkf

        else:
            if kfType == 'Returns':
                kfDim, kfRetType = args[0], args[1]
            else:
                kfDim, kfRetType = args[0], None

            if len(kfDim) != len(self.sortCharacsId):
                raise Error('Ken French library: Need # of elements in \'kfDim\' to match the # of elements in \'sortCharacsId \'!')
            else:
                self.sortCharacsIdtmp = copy.deepcopy(self.sortCharacsId)
                if len(self.sortCharacsIdtmp) == 1:
                    if self.sortCharacsIdtmp == ['BM']:
                        kfDataset = 'Portfolios_Formed_on_BE-ME' + capitalize_nth(freq_kf, 1)
                    elif self.sortCharacsIdtmp == ['PRIOR_2_12']:
                        kfDataset = str(np.prod(kfDim)) + '_Portfolios_Prior_12_2' + capitalize_nth(freq_kf, 1)
                    elif self.sortCharacsIdtmp == ['PRIOR_1_1']:
                        kfDataset = str(np.prod(kfDim)) + '_Portfolios_Prior_1_0' + capitalize_nth(freq_kf, 1)
                    elif self.sortCharacsIdtmp == ['PRIOR_13_60']:
                        kfDataset = str(np.prod(kfDim)) + '_Portfolios_Prior_60_13' + capitalize_nth(freq_kf, 1)
                    elif self.sortCharacsIdtmp == ['EP']:
                        kfDataset = 'Portfolios_Formed_on_E-P' + capitalize_nth(freq_kf, 1)
                    elif self.sortCharacsIdtmp == ['CFP']:
                        kfDataset = 'Portfolios_Formed_on_CF-P' + capitalize_nth(freq_kf, 1)
                    elif self.sortCharacsIdtmp == ['DP']:
                        kfDataset = 'Portfolios_Formed_on_D-P' + capitalize_nth(freq_kf, 1)
                    else:
                        kfDataset = 'Portfolios_Formed_on_' + self.sortCharacsIdtmp[0] + capitalize_nth(freq_kf, 1)

                    dfkf_dict = web.DataReader(kfDataset, 'famafrench', dt_start)
                    if kfDim == [3]:
                        cols_idx = ['Lo 30', 'Med 40', 'Hi 30']
                    elif kfDim == [5]:
                        cols_idx = ['Lo 20', 'Qnt 2', 'Qnt 3', 'Qnt 4', 'Hi 20']
                    elif kfDim == [10]:
                        if any('PRIOR' in x for x in self.sortCharacsIdtmp):
                            cols_idx = ['Lo PRIOR'] + ['PRIOR ' + str(pnum) for pnum in range(2, 10)] + ['Hi PRIOR']
                        else:
                            cols_idx = ['Lo 10', 'Dec 2', 'Dec 3', 'Dec 4', 'Dec 5', 'Dec 6', 'Dec 7', 'Dec 8', 'Dec 9', 'Hi 10']
                    else:
                        raise ValueError('\'kfDim\' is not a standard type!')

                elif len(self.sortCharacsIdtmp) >= 2:
                    if (len(self.sortCharacsIdtmp) == 2) and (self.sortCharacsIdtmp == ['ME', 'BM']):
                        try:
                            kfDataset = str(np.prod(kfDim)) + '_Portfolios_' + str(kfDim[0]) + 'x' + str(kfDim[1]) + freq_kf
                            dfkf_dict = web.DataReader(kfDataset, 'famafrench', dt_start)
                        except RemoteDataError:
                            try:
                                kfDataset = str(np.prod(kfDim)) + '_Portfolios_' + str(kfDim[0]) + 'x' + str(kfDim[1]) + capitalize_nth(freq_kf, 1)
                                dfkf_dict = web.DataReader(kfDataset, 'famafrench', dt_start)
                            except RemoteDataError:
                                raise Error('Dataset does not exist in Ken French\'s online library!')

                    elif len(self.sortCharacsIdtmp) == 2 and self.sortCharacsIdtmp != ['ME', 'BM']:
                        if 'BM' in self.sortCharacsIdtmp:
                            self.sortCharacsIdtmp[self.sortCharacsIdtmp.index('BM')] = 'BEME'
                        if any('PRIOR' in x for x in self.sortCharacsIdtmp):
                            idx = [pos for pos, s in enumerate(self.sortCharacsIdtmp) if 'PRIOR' in s][0]
                            self.sortCharacsIdtmp[idx] = self.sortCharacsIdtmp[idx].title()
                            j_month, k_month = self.sortCharacsIdtmp[idx].split('_')[1], self.sortCharacsIdtmp[idx].split('_')[2]
                            if 'Prior_' + k_month + '_' + j_month == 'Prior_1_1':
                                self.sortCharacsIdtmp[idx] = 'Prior_1_0'
                            else:
                                self.sortCharacsIdtmp[idx] = 'Prior_' + k_month + '_' + j_month

                        try:
                            kfDataset = str(np.prod(kfDim)) + '_Portfolios_' + self.sortCharacsIdtmp[0] + '_' + self.sortCharacsIdtmp[1] + capitalize_nth(freq_kf, 1)
                            dfkf_dict = web.DataReader(kfDataset, 'famafrench', dt_start)
                        except RemoteDataError:
                            try:
                                kfDataset = str(np.prod(kfDim)) + '_Portfolios_' + self.sortCharacsIdtmp[0] + '_' + self.sortCharacsIdtmp[1] + '_' + str(kfDim[0]) + 'x' + str(kfDim[1]) + freq_kf
                                dfkf_dict = web.DataReader(kfDataset, 'famafrench', dt_start)
                            except RemoteDataError:
                                try:
                                    kfDataset = str(np.prod(kfDim)) + '_Portfolios_' + self.sortCharacsIdtmp[0] + '_' + \
                                                self.sortCharacsIdtmp[1] + '_' + str(kfDim[0]) + 'x' + str(kfDim[1]) + capitalize_nth(freq_kf, 1)
                                    dfkf_dict = web.DataReader(kfDataset, 'famafrench', dt_start)
                                except RemoteDataError:
                                    raise Error('Dataset does not exist in Ken French\'s online library!')

                    elif len(self.sortCharacsIdtmp) == 3:
                        if 'BM' in self.sortCharacsIdtmp:
                            self.sortCharacsIdtmp[self.sortCharacsIdtmp.index('BM')] = 'BEME'
                        try:
                            kfDataset = str(np.prod(kfDim)) + '_Portfolios_' + self.sortCharacsIdtmp[0] + '_' + \
                                        self.sortCharacsIdtmp[1] + '_' + self.sortCharacsIdtmp[2] + '_' + str(kfDim[0]) + 'x' + str(kfDim[1]) + 'x' + str(kfDim[2]) + freq_kf
                            dfkf_dict = web.DataReader(kfDataset, 'famafrench', dt_start)
                        except RemoteDataError:
                            try:
                                kfDataset = str(np.prod(kfDim)) + '_Portfolios_' + self.sortCharacsIdtmp[0] + '_' + \
                                            self.sortCharacsIdtmp[1] + '_' + self.sortCharacsIdtmp[2] + \
                                            '_' + str(kfDim[0]) + 'x' + str(kfDim[1]) + 'x' + str(kfDim[2]) + capitalize_nth(freq_kf, 1)
                                dfkf_dict = web.DataReader(kfDataset, 'famafrench', dt_start)
                            except RemoteDataError:
                                raise Error('Dataset does not exist in Ken French\'s online library!')
                    else:
                        raise Error('Dataset does not exist in Ken French\'s online library!')

                dfkf = {}
                if kfType == 'Returns':
                    if kfFreq in ['D', 'W', 'M']:
                        if kfRetType == 'vw':
                            if len(self.sortCharacsIdtmp) == 1:
                                dfkf = (dfkf_dict[0][cols_idx].replace(-99.99, np.nan)) / 100  # % --> decimals
                            else:
                                dfkf = (dfkf_dict[0].replace(-99.99, np.nan)) / 100  # % --> decimals
                        else:
                            if len(self.sortCharacsIdtmp) == 1:
                                dfkf = (dfkf_dict[1][cols_idx].replace(-99.99, np.nan)) / 100  # % --> decimals
                            else:
                                dfkf = (dfkf_dict[1].replace(-99.99, np.nan)) / 100  # % --> decimals
                    else:
                        if kfRetType == 'vw':
                            if len(self.sortCharacsIdtmp) == 1:
                                dfkf = (dfkf_dict[2][cols_idx].replace(-99.99, np.nan)) / 100  # % --> decimals
                            else:
                                dfkf = (dfkf_dict[2].replace(-99.99, np.nan)) / 100  # % --> decimals
                        else:
                            if len(self.sortCharacsIdtmp) == 1:
                                dfkf = (dfkf_dict[3][cols_idx].replace(-99.99, np.nan)) / 100  # % --> decimals
                            else:
                                dfkf = (dfkf_dict[3].replace(-99.99, np.nan)) / 100  # % --> decimals

                elif kfType == 'NumFirms':
                    if kfFreq in ['D', 'W']:
                        try:
                            if len(self.sortCharacsIdtmp) == 1:
                                dfkf = dfkf_dict[2][cols_idx]
                            else:
                                dfkf = dfkf_dict[2]
                        except KeyError:
                            # print('Dataset does not exist in Ken French\'s online library.')
                            pass
                    elif kfFreq == 'M':
                        if len(self.sortCharacsIdtmp) == 1:
                            dfkf = dfkf_dict[4][cols_idx]
                        else:
                            dfkf = dfkf_dict[4]
                    else:
                        # print('Dataset does not exist in Ken French\'s online library.')
                        pass

                elif kfType == 'Characs':
                    re_prior = compile('PRIOR_' + r'[0-9]+' + '_' + r'[0-9]+')
                    prior_list = list(filter(re_prior.search, self.mainCharacsId))

                    for c in set(self.mainCharacsId).difference(set(prior_list + ['AC', 'BETA', 'NI'] + ['VAR', 'RESVAR'])):
                        if kfFreq in ['D', 'W']:
                            if c == 'ME':
                                if len(self.sortCharacsIdtmp) == 1:
                                    # Remove strange white space in front of potential column 'Med 40':
                                    dfkf_dict[3].columns = dfkf_dict[3].columns.str.lstrip()
                                    dfkf['ME'] = dfkf_dict[3][cols_idx].replace(-99.99, np.nan)
                                else:
                                    dfkf['ME'] = dfkf_dict[3].replace(-99.99, np.nan)
                            else:
                                pass
                        # if kfFreq in ['M', 'Q', 'A']
                        else:
                            if c == 'ME':
                                try:
                                    if len(self.sortCharacsIdtmp) == 1:
                                        if kfFreq == 'A':
                                            pass
                                        else:
                                            # Remove strange white space in front of potential column 'Med 40':
                                            dfkf_dict[5].columns = dfkf_dict[5].columns.str.lstrip()
                                            dfkf['ME'] = dfkf_dict[5][cols_idx].replace(-99.99, np.nan)
                                    else:
                                        if kfFreq == 'A':
                                            pass
                                        else:
                                            dfkf['ME'] = dfkf_dict[5].replace(-99.99, np.nan)
                                except KeyError:
                                    pass
                            if c == 'BM':
                                try:
                                    if len(self.sortCharacsIdtmp) == 1:
                                        if 'BM' in self.sortCharacsIdtmp and kfFreq == 'A':
                                            # Remove strange white space in front of potential column 'Med 40':
                                            dfkf_dict[7].columns = dfkf_dict[7].columns.str.lstrip()
                                            dfkf['BM'] = dfkf_dict[7][cols_idx].replace(-99.99, np.nan)
                                        else:
                                            pass
                                    else:
                                        if kfFreq == 'M':
                                            dfkf['BM'] = dfkf_dict[6].replace(-99.99, np.nan)
                                        else:
                                            pass
                                except KeyError:
                                    pass
                            if c == 'OP':
                                try:
                                    if len(self.sortCharacsIdtmp) == 1:
                                        if 'OP' in self.sortCharacsIdtmp and kfFreq == 'A':
                                            # Remove strange white space in front of potential column 'Med 40':
                                            dfkf_dict[6].columns = dfkf_dict[6].columns.str.lstrip()
                                            dfkf['OP'] = dfkf_dict[6][cols_idx].replace(-99.99, np.nan)
                                        else:
                                            pass
                                    else:
                                        if kfFreq == 'M':
                                            if utils.any_in(['VAR', 'RESVAR', 'BETA'], self.sortCharacsIdtmp):
                                                dfkf['OP'] = dfkf_dict[9].replace(-99.99, np.nan)
                                            elif utils.any_in(['AC', 'NI'], self.sortCharacsIdtmp):
                                                dfkf['OP'] = dfkf_dict[10].replace(-99.99, np.nan)
                                            else:
                                                dfkf['OP'] = dfkf_dict[8].replace(-99.99, np.nan)
                                        else:
                                            pass
                                except KeyError:
                                    pass
                            if c == 'INV':
                                try:
                                    if len(self.sortCharacsIdtmp) == 1:
                                        if 'INV' in self.sortCharacsIdtmp and kfFreq == 'A':
                                            # Remove strange white space in front of potential column 'Med 40':
                                            dfkf_dict[6].columns = dfkf_dict[6].columns.str.lstrip()
                                            dfkf['INV'] = dfkf_dict[6][cols_idx].replace(-99.99, np.nan)
                                        else:
                                            pass
                                    else:
                                        if kfFreq == 'M':
                                            if utils.any_in(['VAR', 'RESVAR', 'BETA'], self.sortCharacsIdtmp):
                                                dfkf['INV'] = dfkf_dict[10].replace(-99.99, np.nan)
                                            elif utils.any_in(['AC', 'NI'], self.sortCharacsIdtmp):
                                                dfkf['INV'] = dfkf_dict[11].replace(-99.99, np.nan)
                                            else:
                                                dfkf['INV'] = dfkf_dict[9].replace(-99.99, np.nan)
                                        else:
                                            pass
                                except KeyError:
                                    pass
                            if c == 'EP':
                                try:
                                    if kfFreq == 'A':
                                        if len(self.sortCharacsIdtmp) == 1:
                                            if 'EP' in self.sortCharacsIdtmp:
                                                # Remove strange white space in front of potential column 'Med 40':
                                                dfkf_dict[7].columns = dfkf_dict[7].columns.str.lstrip()
                                                dfkf['EP'] = dfkf_dict[7][cols_idx].replace(-99.99, np.nan)
                                            else:
                                                pass
                                        else:
                                            dfkf['EP'] = dfkf_dict[6].replace(-99.99, np.nan)
                                    else:
                                        pass
                                except KeyError:
                                    pass
                            if c == 'CFP':
                                try:
                                    if kfFreq == 'A':
                                        if len(self.sortCharacsIdtmp) == 1:
                                            if 'CFP' in self.sortCharacsIdtmp:
                                                # Remove strange white space in front of potential column 'Med 40':
                                                dfkf_dict[7].columns = dfkf_dict[7].columns.str.lstrip()
                                                dfkf['CFP'] = dfkf_dict[7][cols_idx].replace(-99.99, np.nan)
                                            else:
                                                pass
                                        else:
                                            dfkf['CFP'] = dfkf_dict[6].replace(-99.99, np.nan)
                                    else:
                                        pass
                                except KeyError:
                                    pass
                            if c == 'DP':
                                try:
                                    if len(self.sortCharacsIdtmp) != 1 and kfFreq == 'A':
                                        dfkf['DP'] = dfkf_dict[6].replace(-99.99, np.nan)
                                    else:
                                        pass
                                except KeyError:
                                    pass

                    if len(prior_list) != 0:
                        for c in prior_list:
                            try:
                                if len(self.sortCharacsIdtmp) == 1:
                                    if c in self.sortCharacsIdtmp and kfFreq == 'A':
                                        # Remove strange white space in front of potential column 'Med 40':
                                        dfkf_dict[6].columns = dfkf_dict[6].columns.str.lstrip()
                                        dfkf[c] = dfkf_dict[6][cols_idx].replace(-99.99, np.nan)
                                    else:
                                        pass
                                else:
                                    if kfFreq == 'M':
                                        dfkf[c] = dfkf_dict[7].replace(-99.99, np.nan)
                                    else:
                                        pass
                            except KeyError:
                                pass

                    if len(set(['AC', 'BETA', 'NI']).intersection(set(self.mainCharacsId))) != 0:
                        for c in set(['AC', 'BETA', 'NI']).intersection(set(self.mainCharacsId)):
                            try:
                                if len(self.sortCharacsIdtmp) == 1:
                                    if c in self.sortCharacsIdtmp and kfFreq == 'A':
                                        # Remove strange white space in front of potential column 'Med 40':
                                        dfkf_dict[6].columns = dfkf_dict[6].columns.str.lstrip()
                                        dfkf[c] = dfkf_dict[6][cols_idx].replace(-99.99, np.nan)
                                    else:
                                        pass
                                else:
                                    if utils.any_in(['AC', 'NI'], self.sortCharacsIdtmp) and kfFreq == 'M':
                                        if c == 'AC':
                                            dfkf['AC'] = dfkf_dict[9].replace(-99.99, np.nan)
                                        elif c == 'NI':
                                            dfkf['NI'] = dfkf_dict[8].replace(-99.99, np.nan)
                                    elif 'BETA' in self.sortCharacsIdtmp and kfFreq == 'M':
                                        if c == 'BETA':
                                            dfkf['BETA'] = dfkf_dict[8].replace(-99.99, np.nan)
                                    else:
                                        pass
                            except KeyError:
                                pass

                    if len(set(['VAR', 'RESVAR']).intersection(set(self.mainCharacsId))) != 0:
                        for c in set(['VAR', 'RESVAR']).intersection(set(self.mainCharacsId)):
                            try:
                                if kfFreq == 'M':
                                    if len(self.sortCharacsIdtmp) == 1:
                                        if c in self.sortCharacsIdtmp:
                                            # Remove strange white space in front of potential column 'Med 40':
                                            dfkf_dict[6].columns = dfkf_dict[6].columns.str.lstrip()
                                            dfkf[c] = dfkf_dict[6][cols_idx].replace(-99.99, np.nan)
                                        else:
                                            pass
                                    else:
                                        dfkf[c] = dfkf_dict[8].replace(-99.99, np.nan)
                                else:
                                    pass
                            except KeyError:
                                pass

                if printkfName:
                    print('Ken French\'s dataset filename: ' + kfDataset)

                if (kfRetType == 'Characs') or (type(dfkf) is dict):
                    for key in dfkf:
                        # Adjust index if frequency is daily or weekly
                        if kfFreq in ['D', 'W']:
                            if kfFreq == 'W':
                                # NOTE: Ken French's weekly datasets provide incorrect dates for some weeks prior to 1953.
                                #       Specifically, some weeks end on a Saturday, instead of the correct trading weekday.
                                #       An adjustment is made to correct for the error, assuming the only mistake is in the
                                #       the weekly dates provided by Ken French and not how the daily returns are cumulated
                                #       for the aforementioned weeks.
                                dfkf[key].index = np.where(dfkf[key].index.day_name().isin(['Saturday', 'Sunday']), dfkf[key].index - BDay(1), dfkf[key].index)

                                # NYSE trading day holiday calendar
                                nyse_holidays = pd.DataFrame(nyse_cal.holidays().holidays, columns=['nyse_date'])
                                nyse_holidays = nyse_holidays[(dt_start <= nyse_holidays['nyse_date'].dt.date) & (dt_end >= nyse_holidays['nyse_date'].dt.date)]['nyse_date'].dt.date.tolist()
                                dfkf[key].index = np.where(dfkf[key].index.isin(nyse_holidays), dfkf[key].index - BDay(1), dfkf[key].index)
                            dfkf[key].index = pd.to_datetime(dfkf[key].index).date
                        else:
                            dfkf[key].index = dfkf[key].index.to_timestamp(kfFreq).date
                        dfkf[key].columns = dfkf[key].columns.str.lower()
                        dfkf[key] = dfkf[key].loc[dt_start:dt_end]
                else:
                    # Adjust index if frequency is daily or weekly
                    if kfFreq in ['D', 'W']:
                        if kfFreq == 'W':
                            # See most recent NOTE.
                            dfkf.index = np.where(dfkf.index.day_name().isin(['Saturday', 'Sunday']), dfkf.index - BDay(1), dfkf.index)
                        dfkf.index = pd.to_datetime(dfkf.index).date
                    else:
                        dfkf.index = dfkf.index.to_timestamp(kfFreq).date
                    dfkf.columns = dfkf.columns.str.lower()
                    dfkf = dfkf.loc[dt_start:dt_end]
                return dfkf

    def getkfPortfolioReturns(self, freq, dt_start, dt_end, dim, retType):
        """
        Query portfolio returns from Ken French's online library at a given frequency and for a given sample period.

        Parameters
        ___________
        freq : str
            Observation frequency of the portfolios. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.
        dim : list, int
            Dimensions for sorting on each element in the list ``self.sortCharacsId``.
        retType : str
            Weighting-scheme for portfolios. Possible choices are:

                * ``vw`` : value-weights
                * ``ew`` : equal-weights


        Returns
        ________
        kfportRetTable: pandas.DataFrame
            Cleaned dataset queried from Ken French's online library containing portfolio returns
            observed at frequency ``freq`` over sample period from ``dt_start`` to ``dt_end``
            for a given portfolio sorting strategy.

        """
        # Check if 'dt_start' and/or 'dt_end' are trading dates:
        # If they are, leave as is, else, get the trading date after 'dt_start' and/or the trading date before 'dt_end'
        check_start = nyse_cal.schedule(start_date=dt_start, end_date=dt_start)
        check_end = nyse_cal.schedule(start_date=dt_end, end_date=dt_end)
        if len(check_start) == 0:
            dt_start = (dt_start + BDay(1)).date()
        if len(check_end) == 0:
            dt_end = (dt_end - BDay(1)).date()

        if (type(dim) is list) and (type(retType) is str):
            if len(dim) != len(self.sortCharacsId):
                raise Error('Need # of elements in \'dim\' to match the # of elements in \'sortCharacsId \'!')
            else:
                kfportRetTable = self.kfLibrary('Returns', freq, dt_start, dt_end, dim, retType, printkfName=False)
                # Remove days landing on Saturday or Sunday which can be found in Ken French's online datasets.
                if freq == 'D':
                    kfportRetTable = kfportRetTable[(pd.to_datetime(kfportRetTable.index).weekday < 5)]
                return kfportRetTable
        else:
            raise TypeError('\'dim\' is not a list w/ the dimensions for each sort.\n'
                            '\'retType\' is not a string w/ weighting scheme for portfolio returns.')



    def getkfNumFirms(self, freq, dt_start, dt_end, dim):
        """
        Query number of firms in each portfolio from Ken French's online data library
        at a given frequency and for a given sample period.

        Parameters
        ___________
        freq : str
            Observation frequency of the portfolios. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.
        dim : list, int
            Dimensions for sorting on each element in the list ``self.sortCharacsId``.


        Returns
        ________
        kfNFirmsTable: pandas.DataFrame
            Cleaned dataset queried from Ken French's online library containing number of firms in each
            portfolio observed at frequency ``freq`` over sample period from ``dt_start`` to ``dt_end``
            for a given portfolio sorting strategy.

        """
        # Check if 'dt_start' and/or 'dt_end' are trading dates:
        # If they are, leave as is, else, get the trading date after 'dt_start' and/or the trading date before 'dt_end'
        check_start = nyse_cal.schedule(start_date=dt_start, end_date=dt_start)
        check_end = nyse_cal.schedule(start_date=dt_end, end_date=dt_end)
        if len(check_start) == 0:
            dt_start = (dt_start + BDay(1)).date()
        if len(check_end) == 0:
            dt_end = (dt_end - BDay(1)).date()

        if type(dim) is list:
            if len(dim) != len(self.sortCharacsId):
                raise Error('Need # of elements in \'dim\' to match the # of elements in \'sortCharacsId \'!')
            else:
                kfNFirmsTable = self.kfLibrary('NumFirms', freq, dt_start, dt_end, dim, printkfName=False)
                # Remove days landing on Saturday or Sunday which can be found in Ken French's online datasets.
                if freq == 'D':
                    kfNFirmsTable = kfNFirmsTable[(pd.to_datetime(kfNFirmsTable.index).weekday < 5)]
                return kfNFirmsTable
        else:
            raise TypeError('\'dim\' is not a list w/ the dimensions for each sort.')



    def getkfCharacs(self, freq, dt_start, dt_end, dim):
        """
        Query `average` anomaly portfolio characteristics from Ken French's online library
        at a given frequency and for a given sample period.

        Parameters
        ___________
        freq : str
            Observation frequency of the portfolios. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.
        dim : list, int
            Dimensions for sorting on each element in the list ``self.sortCharacsId``.

        Returns
        ________
        kfAvgCharacsTable: pandas.DataFrame
            Cleaned dataset queried from Ken French's online library containing `average` portfolio characteristics
            observed at frequency ``freq`` over sample period from ``dt_start`` to ``dt_end``
            for a given portfolio sorting strategy.

        """
        # Check if 'dt_start' and/or 'dt_end' are trading dates:
        # If they are, leave as is, else, get the trading date after 'dt_start' and/or the trading date before 'dt_end'.
        check_start = nyse_cal.schedule(start_date=dt_start, end_date=dt_start)
        check_end = nyse_cal.schedule(start_date=dt_end, end_date=dt_end)
        if len(check_start) == 0:
            dt_start = (dt_start + BDay(1)).date()
        if len(check_end) == 0:
            dt_end = (dt_end - BDay(1)).date()

        if type(dim) is list:
            if len(dim) != len(self.sortCharacsId):
                raise Error('Need # of elements in \'dim\' to match the # of elements in \'sortCharacsId \'!')
            else:
                kfAvgCharacsTable = self.kfLibrary('Characs', freq, dt_start, dt_end, dim, printkfName=False)
                # Remove days landing on Saturday or Sunday which can be found in Ken French's online datasets.
                if freq == 'D':
                    for charac in list(self.mainCharacsId):
                        kfAvgCharacsTable[charac] = kfAvgCharacsTable[charac][(pd.to_datetime(kfAvgCharacsTable[charac].index).weekday < 5)]
                return kfAvgCharacsTable
        else:
            raise TypeError('\'dim\' is not a list w/ the dimensions for each sort.')


    def getkfFFfactors(self, freq, dt_start, dt_end):
        """
        Query Fama-French-style factors from Ken French's online library
        at a given frequency and for a given sample period.

        Parameters
        ___________
        freq : str
            Observation frequency of the portfolios. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start : datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end : datetime.date
            Ending date for the dataset queried or locally retrieved.

        Returns
        ________
        kfffFactorsTable : pandas.DataFrame
            Cleaned dataset queried from Ken French's online library containing Fama-French-style factors
            observed at frequency ``freq`` over sample period from ``dt_start`` to ``dt_end``
            for a given portfolio sorting strategy.

        """
        # Check if 'dt_start' and/or 'dt_end' are trading dates:
        # If they are, leave as is, else, get the trading date after 'dt_start' and/or the trading date before 'dt_end'
        check_start = nyse_cal.schedule(start_date=dt_start, end_date=dt_start)
        check_end = nyse_cal.schedule(start_date=dt_end, end_date=dt_end)
        if len(check_start) == 0:
            dt_start = (dt_start + BDay(1)).date()
        if len(check_end) == 0:
            dt_end = (dt_end - BDay(1)).date()

        kfffFactorsTable = self.kfLibrary('Factors', freq, dt_start, dt_end, printkfName=False)
        # Remove days landing on Saturday or Sunday which can be found in Ken French's online datasets.
        if freq == 'D':
            kfffFactorsTable = kfffFactorsTable[(pd.to_datetime(kfffFactorsTable.index).weekday < 5)]
        return kfffFactorsTable


    @utils.timing
    def comparePortfolios(self, kfType, kfFreq, dt_start, dt_end, *args):
        """
        Generalized routine used to compare datasets constructed from `wrds-cloud` queries
        to their equivalents made publicly available on
        `Ken French's online library <https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html>`_
        at a given frequency and for a given sample period.

        Parameters
        ___________
        kfType : str
            Dataset type to query. Possible choices are:

                * ``Returns``
                * ``Factors``
                * ``NumFirms``
                * ``Characs``
        kfFreq : str
            Observation frequency of the portfolios. Possible choices are:

                * ``D`` : daily
                * ``W`` : weekly
                * ``M`` : monthly
                * ``Q`` : quarterly (3-months)
                * ``A`` : annual
        dt_start: datetime.date
            Starting date for the dataset queried or locally retrieved.
        dt_end: datetime.date
            Ending date for the dataset queried or locally retrieved.
        kfDim : list, int, [optional]
            Dimensions for sorting on each element in the list ``self.sortCharacsId``.
        kfRetType : str, [optional]
            Weighting-scheme for portfolios. Possible choices are:

                * ``vw`` : value-weights
                * ``ew`` : equal-weights

        Returns
        ________
        dfcorrTable : `pandas.DataFrame` or `list`, `pandas.DataFrame` if ``len(kfDim) == 3``
            Table w/ `Pearson correlations` between `wrds-cloud` constructed and Ken French online library portfolio variables
            at a given frequency and over a given sample period.
        dfmeanTable :` pandas.DataFrame` or `list`, `pandas.DataFrame` if ``len(kfDim) == 3``
            Table w/ `mean statistics` for `wrds-cloud` constructed and Ken French online library portfolio variables
            at a given frequency and over a given sample period.
        dfstdevTable : `pandas.DataFrame` or `list`, `pandas.DataFrame` if ``len(kfDim) == 3``
            Table w/ `standard deviation` statistics for `wrds-cloud` constructed and Ken French online library portfolio variables
            at a given frequency and over a given sample period.

        Note
        ______
        The routine is "wrapped" w/ the user-defined function ``timing()`` from module ``famafrench.utils.py``.
        This wrapper times (in seconds) how long the routine takes to complete.

        Note
        _____
        Portfolios require anomaly characteristics from the last fiscal year.
        To get non-missing observations starting on date ``dt_start``, we construct portfolios using a startdate that is two/three years prior to ``dt_start``.
        We then slice the resulting pandas.DataFrames starting w/ ``dt_start``.
        """
        # Check if 'dt_start' and/or 'dt_end' are trading dates:
        # If they are, leave as is, else, get the trading date after 'dt_start' and/or the trading date before 'dt_end'.
        check_start = nyse_cal.schedule(start_date=dt_start, end_date=dt_start)
        check_end = nyse_cal.schedule(start_date=dt_end, end_date=dt_end)
        if len(check_start) == 0:
            dt_start = (dt_start + BDay(1)).date()
        if len(check_end) == 0:
            dt_end = (dt_end - BDay(1)).date()

        def formatting(dType, value):
            if dType in ['Factor', 'Returns']:
                value = str(value) + '%'
            if dType == 'NumFirms':
                value = '{:.0f}'.format(value)
            return value

        if kfType == 'Factors':
            portTable = self.getFFfactors(dt_start - relativedelta(years=3), dt_end)
            kfportTable = self.getkfFFfactors(kfFreq, dt_start, dt_end)
            portTable = portTable.loc[dt_start:]
            scale = 100

            # Restrict index in 'portTable' to coincide w/ that of 'kfportTable'.
            # Get 'min' and 'max' date:
            portTable = portTable[portTable.index.isin(kfportTable.index)]
            min_date, max_date = portTable.index.min(), portTable.index.max()

            dfcorrTable = pd.DataFrame([{c: round(portTable[c].corr(kfportTable[c]), 3) for c in portTable.columns}], columns=portTable.columns, index=['corr:'])
            dfmeanTable = pd.DataFrame([{c: [formatting(kfType, round(portTable[c].mean() * scale, 2)), formatting(kfType, round(portTable[c].mean() * scale, 2))]
                                         for c in portTable.columns}], columns=kfportTable.columns, index=['[wrds, kflib]:'])
            dfstdevTable = pd.DataFrame([{c: [formatting(kfType, round(portTable[c].std() * scale, 2)), formatting(kfType, round(portTable[c].std() * scale, 2))]
                                          for c in portTable.columns}], columns=kfportTable.columns, index=['[wrds, kflib]:'])
            print('*********************************** Factor Returns:', min_date, 'to', max_date, '***********************************\n')
            print('    *********************** Observation frequency: ' + kfFreq + ' ************************')
            print('Fama-French factors: Correlation matrix:\n', dfcorrTable, '\n')
            print('Fama-French factors: Average matrix:\n', dfmeanTable, '\n')
            print('Fama-French factors: Std Deviation matrix:\n', dfstdevTable, '\n')
            return dfcorrTable, dfmeanTable, dfstdevTable

        elif kfType in ['Returns', 'NumFirms', 'Characs']:
            kfDim = args[0]
            if kfType == 'Returns':
                kfRetType = args[1]
                portTable = self.getPortfolioReturns(False, dt_start - relativedelta(years=3), dt_end, kfDim, kfRetType)
                kfportTable = self.getkfPortfolioReturns(kfFreq, dt_start, dt_end, kfDim, kfRetType)
                portTable = portTable.loc[dt_start:]
                scale = 100
            elif kfType == 'NumFirms':
                portTable = self.getNumFirms(False, dt_start - relativedelta(years=3), dt_end, kfDim)
                kfportTable = self.getkfNumFirms(kfFreq, dt_start, dt_end, kfDim)
                portTable = portTable.loc[dt_start:]
                scale = 1
            else:
                portTable = self.getCharacs(False, dt_start - relativedelta(years=3), dt_end, kfDim)
                for charac in list(self.mainCharacsId):
                    portTable[charac] = portTable[charac].loc[dt_start:]
                kfportTable = self.getkfCharacs(kfFreq, dt_start, dt_end, kfDim)
                scale = 1


            if len(kfDim) in [1, 2]:
                # Univariate sort
                if len(kfDim) == 1:
                    # (i) 30-70 sorts, (ii) quintiles, (iii) deciles
                    if kfDim in [[3], [5], [10]]:
                        # Here, we use the fact that the order of the column labels in 'portTable' is consistent w/ the
                        # order of the column lables in 'kfportTable'. If this changes in the future, then this part of the
                        # code should change accordingly.
                        if kfDim == [3]:
                            pbuckets = ['0-30', '30-70', '70-100']
                        elif kfDim == [5]:
                            pbuckets = ['0-20', '20-40', '40-60', '60-80', '80-100']
                        elif kfDim == [10]:
                            pbuckets = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100']

                        def univariateSortTable(dType, pTable, kfpTable, pSorts, pDim):
                            cols_idx = [id1 + value1 for id1, value1 in zip(list(map(str.lower, self.sortCharacsId)) * pDim, pSorts)]

                            # NOTE: We can replace the column labels in 'kfpTable' w/ those in cols_idx because the order of the columns
                            #       in Ken French's data perfectly matches the ordering constructed here.
                            #       e.g. Decile sorts, [lo 10, dec 2, dec 3, dec 4, dec 5, dec 6, dec 7, dec 8, dec 9, hi 10]
                            #            is the same as [0-10, 10-20, 20-30, 30-40, 40-50, 50-60, 60-70, 70-80, 80-90, 90-100]
                            kfpTable.columns = cols_idx
                            corrTable = pd.DataFrame([{c: round(pTable[c].corr(kfpTable[c]), 3) for c in cols_idx}], index=['corr:'])
                            meanTable = pd.DataFrame([{c: [formatting(dType, round(pTable[c].mean() * scale, 2)), formatting(dType, round(kfpTable[c].mean() * scale, 2))]
                                                       for c in cols_idx}], index=['[wrds, kflib]:'])
                            stdevTable = pd.DataFrame([{c: [formatting(dType, round(pTable[c].std() * scale, 2)), formatting(dType, round(kfpTable[c].std() * scale, 2))]
                                                        for c in cols_idx}], index=['[wrds, kflib]:'])
                            return corrTable, meanTable, stdevTable

                        dfcorrTable, dfmeanTable, dfstdevTable = {}, {}, {}
                        if kfType in ['Returns', 'NumFirms']:
                            for dummy in range(1):
                                try:
                                    # Restrict index in 'portTable' to coincide w/ that of 'kfportTable'.
                                    # Get 'min' and 'max' date:
                                    portTable = portTable[portTable.index.isin(kfportTable.index)]
                                    min_date, max_date = portTable.index.min(), portTable.index.max()

                                    dfcorrTable, dfmeanTable, dfstdevTable = univariateSortTable(kfType, portTable, kfportTable, pbuckets, kfDim[0])
                                    print('*********************************** ' + ' x '.join(self.sortCharacsId) + ' (' + ' x '.join(str(d) for d in kfDim) + ') ************************************')
                                    print('    *********************** Observation frequency: ' + kfFreq + ' ************************')
                                    print('    *************************', kfType + ':', min_date, 'to', max_date, '**************************\n')
                                    print('Correlation matrix:\n', dfcorrTable, '\n')
                                    print('Average matrix:\n', dfmeanTable, '\n')
                                    print('Std Deviation matrix:\n', dfstdevTable, '\n')
                                except (AttributeError, UnboundLocalError):
                                    print('*********************************** ' + ' x '.join(self.sortCharacsId) + ' (' + ' x '.join(str(d) for d in kfDim) + ') ************************************')
                                    print('    *********************** Observation frequency: ' + kfFreq + ' ************************')
                                    print('   *******************************', kfType + ' *******************************')
                                    print('   ******************************* NOT AVAILABLE *****************************\n')
                                    continue
                        else:
                            for charac in list(self.mainCharacsId):
                                try:
                                    # Restrict index in 'portTable' to coincide w/ that of 'kfportTable'.
                                    # Get 'min' and 'max' date:
                                    portTable[charac] = portTable[charac][portTable[charac].index.isin(kfportTable[charac].index)]
                                    min_date, max_date = portTable[charac].index.min(), portTable[charac].index.max()

                                    dfcorrTable[charac], dfmeanTable[charac], dfstdevTable[charac] = univariateSortTable(kfType, portTable[charac], kfportTable[charac], pbuckets, kfDim[0])
                                    print('*********************************** ' + ' x '.join(self.sortCharacsId) + ' (' + ' x '.join(str(d) for d in kfDim) + ') ************************************')
                                    print('    *********************** Observation frequency: ' + kfFreq + ' ************************')
                                    print('    ************************* (Characteristic: ' + charac + '):', min_date, 'to', max_date, '***************************\n')
                                    print('Correlation matrix:\n', dfcorrTable[charac], '\n')
                                    print('Average matrix:\n', dfmeanTable[charac], '\n')
                                    print('Std Deviation matrix:\n', dfstdevTable[charac], '\n')
                                except (KeyError, UnboundLocalError):
                                    print('*********************************** ' + ' x '.join(self.sortCharacsId) + ' (' + ' x '.join(str(d) for d in kfDim) + ') ************************************')
                                    print('    *********************** Observation frequency: ' + kfFreq + ' ************************')
                                    print('   ************************** (Characteristic: ' + charac + ') ***************************')
                                    print('   ******************************* NOT AVAILABLE *****************************\n')
                                    continue
                        return dfcorrTable, dfmeanTable, dfstdevTable
                    else:
                        raise ValueError('\'kfDim\' is not a standard type')
                # Bivariate sort
                else:
                    if kfDim in [[2, 3], [5, 5], [10, 10]]:
                        # (i) median splits x 30-70 sorts
                        if kfDim == [2, 3]:
                            pbuckets = [['0-50', '50-100'], ['0-30', '30-70', '70-100']]

                            def bivariateSortTable(dType, pTable, kfpTable, pSorts, pDim):
                                rows_idx = [id1 + value1 for id1, value1 in zip(list(map(str.lower, [self.sortCharacsId[0]])) * pDim[0], pSorts[0])]
                                cols_idx = [id2 + value2 for id2, value2 in zip(list(map(str.lower, [self.sortCharacsId[1]])) * pDim[1], pSorts[1])]
                                corrTable = pd.DataFrame(index=rows_idx, columns=cols_idx)
                                meanTable = pd.DataFrame(index=rows_idx, columns=cols_idx)
                                stdevTable = pd.DataFrame(index=rows_idx, columns=cols_idx)

                                def rowLabelReplace(row_idx, row_id):
                                    if row_id == 'ME':
                                        row_idx = getattr(row_idx, 'replace')('small', 'me0-50')
                                        row_idx = getattr(row_idx, 'replace')('big', 'me50-100')
                                    if 'prior' in row_id.lower():
                                        row_id_tmp = 'prior'
                                    else:
                                        row_id_tmp = row_id.lower()
                                    row_idx = sub(r'\b' + row_id_tmp + '1' + r'\b', row_id.lower() + '0-50', row_idx)
                                    row_idx = sub(r'\b' + row_id_tmp + '2' + r'\b', row_id.lower() + '50-100', row_idx)
                                    row_idx = getattr(row_idx, 'replace')('lo' + row_id_tmp, row_id.lower() + '0-50')
                                    row_idx = getattr(row_idx, 'replace')('hi' + row_id_tmp, row_id.lower() + '50-100')
                                    return row_idx

                                def colLabelReplace(col_idx, col_id):
                                    if 'prior' in col_id.lower():
                                        col_id_tmp = 'prior'
                                    else:
                                        col_id_tmp = col_id.lower()
                                    col_idx = sub(r'\b' + col_id_tmp + '2' + r'\b', col_id.lower() + '30-70', col_idx)
                                    col_idx = getattr(col_idx, 'replace')('lo' + col_id_tmp, col_id.lower() + '0-30')
                                    col_idx = getattr(col_idx, 'replace')('hi' + col_id_tmp, col_id.lower() + '70-100')
                                    return col_idx

                                for c in kfpTable.columns:
                                    row, col = c.split()[0], c.split()[1]
                                    if 'var' in row and self.sortCharacsId[0] == 'RESVAR':
                                        row = row.replace('var', 'resvar')
                                    if 'var' in col and self.sortCharacsId[1] == 'RESVAR':
                                        col = col.replace('var', 'resvar')
                                    row = rowLabelReplace(row, self.sortCharacsId[0])
                                    col = colLabelReplace(col, self.sortCharacsId[1])
                                    try:
                                        corrTable.at[row, col] = round(pTable[row + '_' + col].corr(kfpTable[c]), 3)
                                        meanTable.at[row, col] = [formatting(dType, round(pTable[row + '_' + col].mean() * scale, 2)),
                                                                  formatting(dType, round(kfpTable[c].mean() * scale, 2))]
                                        stdevTable.at[row, col] = [formatting(dType, round(pTable[row + '_' + col].std() * scale, 2)),
                                                                   formatting(dType, round(kfpTable[c].std() * scale, 2))]
                                    except KeyError:
                                        print('Portfolio \'' + row + '_' + col + '\' is not found in \'portTable\'.')
                                        continue
                                return corrTable, meanTable, stdevTable

                        # (ii) quintile sorts x quintile sorts, (iii) decile sorts x decile sorts.
                        else:
                            if kfDim == [5, 5]:
                                pbuckets = [['0-20', '20-40', '40-60', '60-80', '80-100']] * 2
                            else:
                                pbuckets = [['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100']] * 2

                            def bivariateSortTable(dType, pTable, kfpTable, pSorts, pDim):
                                rows_idx = [id1 + value1 for id1, value1 in zip(list(map(str.lower, [self.sortCharacsId[0]])) * pDim[0], pSorts[0])]
                                cols_idx = [id2 + value2 for id2, value2 in zip(list(map(str.lower, [self.sortCharacsId[1]])) * pDim[1], pSorts[1])]
                                corrTable = pd.DataFrame(index=rows_idx, columns=cols_idx)
                                meanTable = pd.DataFrame(index=rows_idx, columns=cols_idx)
                                stdevTable = pd.DataFrame(index=rows_idx, columns=cols_idx)

                                def labelReplace(pDim_sort, idx_df, id_df):
                                    if pDim_sort == 5:
                                        if id_df == 'ME':
                                            idx_df = getattr(idx_df, 'replace')('small', 'me0-20')
                                            idx_df = getattr(idx_df, 'replace')('big', 'me80-100')
                                        if 'prior' in id_df.lower():
                                            id_df_tmp = 'prior'
                                        else:
                                            id_df_tmp = id_df.lower()
                                        idx_df = sub(r'\b' + id_df_tmp + '1' + r'\b', id_df.lower() + '0-20', idx_df)
                                        idx_df = sub(r'\b' + id_df_tmp + '2' + r'\b', id_df.lower() + '20-40', idx_df)
                                        idx_df = sub(r'\b' + id_df_tmp + '3' + r'\b', id_df.lower() + '40-60', idx_df)
                                        idx_df = sub(r'\b' + id_df_tmp + '4' + r'\b', id_df.lower() + '60-80', idx_df)
                                        idx_df = sub(r'\b' + id_df_tmp + '5' + r'\b', id_df.lower() + '80-100', idx_df)
                                        idx_df = getattr(idx_df, 'replace')('lo' + id_df_tmp, id_df.lower() + '0-20')
                                        idx_df = getattr(idx_df, 'replace')('hi' + id_df_tmp, id_df.lower() + '80-100')
                                    else:
                                        if id_df == 'ME':
                                            idx_df = getattr(idx_df, 'replace')('small', 'me0-10')
                                            idx_df = getattr(idx_df, 'replace')('big', 'me90-100')
                                        if 'prior' in id_df.lower():
                                            id_df_tmp = 'prior'
                                        else:
                                            id_df_tmp = id_df.lower()
                                        idx_df = sub(r'\b' + id_df_tmp + '10' + r'\b', id_df.lower() + '90-100', idx_df)
                                        idx_df = sub(r'\b' + id_df_tmp + '1' + r'\b', id_df.lower() + '0-10', idx_df)
                                        idx_df = sub(r'\b' + id_df_tmp + '2' + r'\b', id_df.lower() + '10-20', idx_df)
                                        idx_df = sub(r'\b' + id_df_tmp + '3' + r'\b', id_df.lower() + '20-30', idx_df)
                                        idx_df = sub(r'\b' + id_df_tmp + '4' + r'\b', id_df.lower() + '30-40', idx_df)
                                        idx_df = sub(r'\b' + id_df_tmp + '5' + r'\b', id_df.lower() + '40-50', idx_df)
                                        idx_df = sub(r'\b' + id_df_tmp + '6' + r'\b', id_df.lower() + '50-60', idx_df)
                                        idx_df = sub(r'\b' + id_df_tmp + '7' + r'\b', id_df.lower() + '60-70', idx_df)
                                        idx_df = sub(r'\b' + id_df_tmp + '8' + r'\b', id_df.lower() + '70-80', idx_df)
                                        idx_df = sub(r'\b' + id_df_tmp + '9' + r'\b', id_df.lower() + '80-90', idx_df)
                                        idx_df = getattr(idx_df, 'replace')('lo' + id_df_tmp, id_df.lower() + '0-10')
                                        idx_df = getattr(idx_df, 'replace')('hi' + id_df_tmp, id_df.lower() + '90-100')
                                    return idx_df

                                for c in kfpTable.columns:
                                    row, col = c.split()[0], c.split()[1]
                                    if 'var' in row and self.sortCharacsId[0] == 'RESVAR':
                                        row = row.replace('var', 'resvar')
                                    if 'var' in col and self.sortCharacsId[1] == 'RESVAR':
                                        col = col.replace('var', 'resvar')
                                    row = labelReplace(pDim[0], row, self.sortCharacsId[0])
                                    col = labelReplace(pDim[1], col, self.sortCharacsId[1])
                                    try:
                                        corrTable.at[row, col] = round(pTable[row + '_' + col].corr(kfpTable[c]), 3)
                                        meanTable.at[row, col] = [formatting(dType, round(pTable[row + '_' + col].mean() * scale, 2)),
                                                                  formatting(dType, round(kfpTable[c].mean() * scale, 2))]
                                        stdevTable.at[row, col] = [formatting(dType, round(pTable[row + '_' + col].std() * scale, 2)),
                                                                   formatting(dType, round(kfpTable[c].std() * scale, 2))]
                                    except KeyError:
                                        print('Portfolio \'' + row + '_' + col + '\' is not found in \'portTable\'.')
                                        continue
                                return corrTable, meanTable, stdevTable

                        dfcorrTable, dfmeanTable, dfstdevTable = {}, {}, {}
                        if kfType in ['Returns', 'NumFirms']:
                            for dummy in range(1):
                                try:
                                    # Restrict index in 'portTable' to coincide w/ that of 'kfportTable'.
                                    # Get 'min' and 'max' date:
                                    portTable = portTable[portTable.index.isin(kfportTable.index)]
                                    min_date, max_date = portTable.index.min(), portTable.index.max()

                                    dfcorrTable, dfmeanTable, dfstdevTable = bivariateSortTable(kfType, portTable, kfportTable, pbuckets, kfDim)
                                    print('*********************************** ' + ' x '.join(self.sortCharacsId) + ' (' + ' x '.join(str(d) for d in kfDim) + ') ************************************')
                                    print('    *********************** Observation frequency: ' + kfFreq + ' ************************')
                                    print('    *************************', kfType + ':', min_date, 'to', max_date, '**************************\n')
                                    print('Correlation matrix:\n', dfcorrTable, '\n')
                                    print('Average matrix:\n', dfmeanTable, '\n')
                                    print('Std Deviation matrix:\n', dfstdevTable, '\n')
                                except (AttributeError, UnboundLocalError):
                                    print('*********************************** ' + ' x '.join(self.sortCharacsId) + ' (' + ' x '.join(str(d) for d in kfDim) + ') ************************************')
                                    print('    *********************** Observation frequency: ' + kfFreq + ' ************************')
                                    print('   *******************************', kfType + ' *******************************')
                                    print('   ******************************* NOT AVAILABLE *****************************\n')
                                    continue
                        else:
                            for charac in list(self.mainCharacsId):
                                try:
                                    # Restrict index in 'portTable' to coincide w/ that of 'kfportTable'.
                                    # Get 'min' and 'max' date:
                                    portTable[charac] = portTable[charac][portTable[charac].index.isin(kfportTable[charac].index)]
                                    min_date, max_date = portTable[charac].index.min(), portTable[charac].index.max()

                                    dfcorrTable[charac], dfmeanTable[charac], dfstdevTable[charac] = bivariateSortTable(kfType, portTable[charac], kfportTable[charac], pbuckets, kfDim)
                                    print('*********************************** ' + ' x '.join(self.sortCharacsId) + ' (' + ' x '.join(str(d) for d in kfDim) + ') ************************************')
                                    print('    *********************** Observation frequency: ' + kfFreq + ' ************************')
                                    print('    ************************* (Characteristic: ' + charac + '):', min_date, 'to', max_date, '***************************\n')
                                    print('Correlation matrix:\n', dfcorrTable[charac], '\n')
                                    print('Average matrix:\n', dfmeanTable[charac], '\n')
                                    print('Std Deviation matrix:\n', dfstdevTable[charac], '\n')
                                except (KeyError, UnboundLocalError):
                                    print('*********************************** ' + ' x '.join(self.sortCharacsId) + ' (' + ' x '.join(str(d) for d in kfDim) + ') ************************************')
                                    print('    *********************** Observation frequency: ' + kfFreq + ' ************************')
                                    print('    ************************* (Characteristic: ' + charac + ') ***************************')
                                    print('   ******************************* NOT AVAILABLE *****************************\n')
                                    continue
                        return dfcorrTable, dfmeanTable, dfstdevTable
                    else:
                        raise ValueError('\'kfDim\' is not a standard type!')
            # Trivariate sort
            elif len(kfDim) == 3:
                # (i) median splits x quartile sorts x quartile sorts
                if kfDim == [2, 4, 4]:
                    pbuckets = [['0-50', '50-100'], ['0-25', '25-50', '50-75', '75-100'], ['0-25', '25-50', '50-75', '75-100']]

                    def trivariateSortTable(dType, pTable, kfpTable, pSorts, pDim):
                        level0_idx = [id1 + value1 for id1, value1 in zip(list(map(str.lower, [self.sortCharacsId[0]])) * pDim[0], pSorts[0])]
                        rows_idx = [id2 + value2 for id2, value2 in zip(list(map(str.lower, [self.sortCharacsId[1]])) * pDim[1], pSorts[1])]
                        cols_idx = [id3 + value3 for id3, value3 in zip(list(map(str.lower, [self.sortCharacsId[2]])) * pDim[2], pSorts[2])]
                        corrTable = {level0: pd.DataFrame(index=rows_idx, columns=cols_idx) for level0 in level0_idx}
                        meanTable = {level0: pd.DataFrame(index=rows_idx, columns=cols_idx) for level0 in level0_idx}
                        stdevTable = {level0: pd.DataFrame(index=rows_idx, columns=cols_idx) for level0 in level0_idx}

                        def labelReplace(pDim_sort, idx_df, id_df):
                            if pDim_sort == 2:
                                if id_df == 'ME':
                                    idx_df = getattr(idx_df, 'replace')('small', 'me0-50')
                                    idx_df = getattr(idx_df, 'replace')('big', 'me50-100')
                                idx_df = sub(r'\b' + id_df.lower() + '1' + r'\b', id_df.lower() + '0-50', idx_df)
                                idx_df = sub(r'\b' + id_df.lower() + '2' + r'\b', id_df.lower() + '50-100', idx_df)
                                idx_df = getattr(idx_df, 'replace')('lo' + id_df.lower(), id_df.lower() + '0-50')
                                idx_df = getattr(idx_df, 'replace')('hi' + id_df.lower(), id_df.lower() + '50-100')
                                return idx_df
                            else:
                                if id_df == 'ME':
                                    idx_df = getattr(idx_df, 'replace')('small', 'me0-25')
                                    idx_df = getattr(idx_df, 'replace')('big', 'me75-100')
                                idx_df = sub(r'\b' + id_df.lower() + '1' + r'\b', id_df.lower() + '0-25', idx_df)
                                idx_df = sub(r'\b' + id_df.lower() + '2' + r'\b', id_df.lower() + '25-50', idx_df)
                                idx_df = sub(r'\b' + id_df.lower() + '3' + r'\b', id_df.lower() + '50-75', idx_df)
                                idx_df = sub(r'\b' + id_df.lower() + '4' + r'\b', id_df.lower() + '75-100', idx_df)
                                idx_df = getattr(idx_df, 'replace')('lo' + id_df.lower(), id_df.lower() + '0-25')
                                idx_df = getattr(idx_df, 'replace')('hi' + id_df.lower(), id_df.lower() + '75-100')
                            return idx_df

                        for c in kfpTable.columns:
                            level0, row, col = c.split()[0], c.split()[1], c.split()[2]
                            if 'var' in level0 and self.sortCharacsId[0] == 'RESVAR':
                                level0 = level0.replace('var', 'resvar')
                            if 'var' in row and self.sortCharacsId[1] == 'RESVAR':
                                row = row.replace('var', 'resvar')
                            if 'var' in col and self.sortCharacsId[2] == 'RESVAR':
                                col = col.replace('var', 'resvar')
                            level0 = labelReplace(pDim[0], level0, self.sortCharacsId[0])
                            row = labelReplace(pDim[1], row, self.sortCharacsId[1])
                            col = labelReplace(pDim[2], col, self.sortCharacsId[2])
                            try:
                                corrTable[level0].at[row, col] = round(pTable[level0 + '_' + row + '_' + col].corr(kfpTable[c]), 3)
                                meanTable[level0].at[row, col] = [formatting(dType, round(pTable[level0 + '_' + row + '_' + col].mean() * scale, 2)),
                                                                  formatting(dType, round(kfpTable[c].mean() * scale, 2))]
                                stdevTable[level0].at[row, col] = [formatting(dType, round(pTable[level0 + '_' + row + '_' + col].std() * scale, 2)),
                                                                   formatting(dType, round(kfpTable[c].std() * scale, 2))]
                            except KeyError:
                                print('Portfolio \'' + level0 + '_' + row + '_' + col + '\' is not found in \'portTable\'.')
                                continue
                        # NOTE: Unlike the first two cases w/ len(kfDim)==1 or ==2,
                        #       here 'dfcorrTable', 'dfmeanTable', and 'dfstdevTable' will be lists of dataframes
                        return corrTable, meanTable, stdevTable

                    dfcorrTable, dfmeanTable, dfstdevTable = {}, {}, {}
                    if kfType in ['Returns', 'NumFirms']:
                        for dummy in range(1):
                            try:
                                # Restrict index in 'portTable' to coincide w/ that of 'kfportTable'.
                                # Get 'min' and 'max' date:
                                portTable = portTable[portTable.index.isin(kfportTable.index)]
                                min_date, max_date = portTable.index.min(), portTable.index.max()

                                dfcorrTable, dfmeanTable, dfstdevTable = trivariateSortTable(kfType, portTable, kfportTable, pbuckets, kfDim)
                                print('*********************************** ' + ' x '.join(self.sortCharacsId) + ' (' + ' x '.join(str(d) for d in kfDim) + ') ***********************************')
                                print('    *********************** Observation frequency: ' + kfFreq + ' ************************')
                                print('    *************************', kfType + ':', min_date, 'to', max_date, '**************************\n')
                                print('Correlation matrix:\n')
                                {print(level0 + ':\n', dfcorrTable[level0], '\n') for level0 in list(dfcorrTable.keys())}
                                print('Average matrix:\n')
                                {print(level0 + ':\n', dfmeanTable[level0], '\n') for level0 in list(dfmeanTable.keys())}
                                print('Std Deviation matrix:\n')
                                {print(level0 + ':\n', dfstdevTable[level0], '\n') for level0 in list(dfstdevTable.keys())}
                            except (AttributeError, UnboundLocalError):
                                print('*********************************** ' + ' x '.join(self.sortCharacsId) + ' (' + ' x '.join(str(d) for d in kfDim) + ') ************************************')
                                print('    *********************** Observation frequency: ' + kfFreq + ' ************************')
                                print('   *******************************', kfType + ' *******************************')
                                print('   ******************************* NOT AVAILABLE *****************************\n')
                                continue
                    else:
                        for charac in list(self.mainCharacsId):
                            try:
                                # Restrict index in 'portTable' to coincide w/ that of 'kfportTable'.
                                # Get 'min' and 'max' date:
                                portTable[charac] = portTable[charac][portTable[charac].index.isin(kfportTable[charac].index)]
                                min_date, max_date = portTable[charac].index.min(), portTable[charac].index.max()

                                dfcorrTable[charac], dfmeanTable[charac], dfstdevTable[charac] = trivariateSortTable(kfType, portTable[charac], kfportTable[charac], pbuckets, kfDim)
                                print('*********************************** ' + ' x '.join(self.sortCharacsId) + ' (' + ' x '.join(str(d) for d in kfDim) + ') ************************************')
                                print('    *********************** Observation frequency: ' + kfFreq + ' ************************')
                                print('    ************************* (Characteristic: ' + charac + '):', min_date, 'to', max_date, '***************************\n')
                                print('Correlation matrix:\n')
                                {print(level0 + ':\n', dfcorrTable[charac][level0], '\n') for level0 in
                                 list(dfcorrTable[charac].keys())}
                                print('Average matrix:\n')
                                {print(level0 + ':\n', dfmeanTable[charac][level0], '\n') for level0 in
                                 list(dfmeanTable[charac].keys())}
                                print('Std Deviation matrix:\n')
                                {print(level0 + ':\n', dfstdevTable[charac][level0], '\n') for level0 in
                                 list(dfstdevTable[charac].keys())}
                            except (KeyError, UnboundLocalError):
                                print('*********************************** ' + ' x '.join(self.sortCharacsId) + ' (' + ' x '.join(str(d) for d in kfDim) + ') ************************************')
                                print('    *********************** Observation frequency: ' + kfFreq + ' ************************')
                                print('    ************************* (Characteristic: ' + charac + ') ***************************')
                                print('   ******************************* NOT AVAILABLE *****************************\n')
                                continue
                    return dfcorrTable, dfmeanTable, dfstdevTable
                else:
                    raise ValueError('\'kfDim\' is not a standard type!')
            else:
                raise ValueError('\'kfDim\' is not of standard length: should be 1, 2, or 3!')
        else:
            raise ValueError('\'kfType\' is not one of \'Returns\', \'Factors\', \'NumFirms\', or \'Characs\'.')
