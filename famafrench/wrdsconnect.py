"""
This file is part of famafrench.
Copyright (c) 2020, Christian Jauregui <chris.jauregui@berkeley.edu>
See file LICENSE.txt for license information.

Filename
_________
`famafrench/wrdsconnect.py`

Description
___________
wrdsConnection
    Object class used to set up a remote connection to `wrds-cloud`.
    This class largely builds on the "Connection" class in the `WRDS-Py` library.
"""

__author__ = 'Christian Jauregui <chris.jauregui@berkeley.edu'
__all__ = ["wrdsConnection"]

# Standard Imports
import os
import sys
import pandas as pd
import sqlalchemy as sa
from sys import version_info
from wrds import __version__ as wrds_version

# Declare 'wrdsConnection' object class
class wrdsConnection:
    __doc__ = """
        Class for setting up the remote connection to `wrds-cloud`;
        largely builds on the ``Connection`` class in the `WRDS-Py library <https://pypi.org/project/wrds/0.0.5/>`_.
        
        Copyright (c) 2017 Wharton Research Data Services
        """
    def __init__(self, autoconnect=True):
        """
        Set up connection to WRDS database by providing necessary parameters,
        including username and password. By default, also establish the connection to the database.
        """
        py3 = version_info[0] > 2
        if not py3:
            raise SyntaxError('PLEASE USE PYTHON 3+')

        appname = '{0} python {1}.{2}.{3}/wrds {4}'.format(
                  sys.platform,
                  version_info[0],
                  version_info[1],
                  version_info[2],
                  wrds_version)

        # Sane defaults
        self.WRDS_params = {'WRDS_USERNAME': os.getenv('WRDS_USERNAME'),
                            'WRDS_PASSWORD': os.getenv('WRDS_PASSWORD'),
                            'WRDS_POSTGRES_HOST': 'wrds-pgdata.wharton.upenn.edu',
                            'WRDS_POSTGRES_PORT': 9737,
                            'WRDS_POSTGRES_DB': 'wrds',
                            'WRDS_CONNECT_ARGS': {'sslmode': 'require',
                                                  'application_name': appname}}

        pghost = 'postgresql://{usr}:{pwd}@{host}:{port}/{dbname}'
        self.engine = sa.create_engine(pghost.format(usr=self.WRDS_params['WRDS_USERNAME'],
                                                     pwd=self.WRDS_params['WRDS_PASSWORD'],
                                                     host=self.WRDS_params['WRDS_POSTGRES_HOST'],
                                                     port=self.WRDS_params['WRDS_POSTGRES_PORT'],
                                                     dbname=self.WRDS_params['WRDS_POSTGRES_DB']),
                                                     connect_args=self.WRDS_params['WRDS_CONNECT_ARGS'])
        if autoconnect:
            self.connect()

    def connect(self):
        """
        Make a connection to the `wrds-cloud` database. Similar to the `WRDS-Py` package's method :meth:`wrds.sql.connect`.

        Parameters
        ___________
        None

        Returns
        _______
        None
            Class instance attributes are updates.
        """
        try:
            self.connection = self.engine.connect()
        except Exception:
            # Parameters for sa.create_engine(*args, **kwargs):
            # https://docs.sqlalchemy.org/en/13/core/engines.html#sqlalchemy.create_engine
            pghost = 'postgresql://{usr}:{pwd}@{host}:{port}/{dbname}'
            self.engine = sa.create_engine(pghost.format(usr=self.WRDS_params['WRDS_USERNAME'],
                                                         pwd=self.WRDS_params['WRDS_PASSWORD'],
                                                         host=self.WRDS_params['WRDS_POSTGRES_HOST'],
                                                         port=self.WRDS_params['WRDS_POSTGRES_PORT'],
                                                         dbname=self.WRDS_params['WRDS_POSTGRES_DB']),
                                                         connect_args=self.WRDS_params['WRDS_CONNECT_ARGS'])
            try:
                self.connection = self.engine.connect()
                return self.connection
            except Exception as e:
                print("There was an error with your username and password.")
                raise e

    def close(self):
        """
        Close the connection to the database. Similar to the `WRDS-Py` package's method :meth:`wrds.sql.close`.

        Parameters
        ___________
        None

        Returns
        _______
        """
        self.connection.close()
        self.engine.dispose()
        return None

    def raw_sql(self, sqlquery, coerce_float=True, date_cols=None, index_col=None, params=None):
        """
        Query the `wrds-cloud` database using a raw SQL string.
        Based on the `WRDS-Py` package's method :meth:`wrds.sql.raq_sql`

        Parameters
        ___________
        sqlquery : str
            SQL code in string object.
        coerce_float : bool, default True [optional]
            Attempts to convert values to non-string, non-numeric objects
            to floating point. Can result in loss of precision.
        date_cols : list or dict, default None [optional]
            - List of column names to parse as date
            - dict of "{column_name: format string}" where format string is:
                * :meth:`date.strftime` compatible in case of parsing string times or is one of (D, s, ns, ms, us) in case of parsing integer timestamps
            - dict of ``{column_name: arg dict}``, where the arg dict corresponds to the keyword arguments of :func:`pandas.to_datetime`
        index_col : str, or list, str, default None [optional]
            Column(s) to set as ``index(MultiIndex)``.
        params : dict
            Parameters to SQL query, if parameterized.

        Returns
        ________
        pd_sql : pandas.DataFrame
            SQL query result.
        """
        try:
            pd_sql = pd.read_sql_query(sqlquery,
                                         self.connection,
                                         coerce_float=coerce_float,
                                         parse_dates=date_cols,
                                         index_col=index_col,
                                         params=params)
            return pd_sql

        except sa.exc.ProgrammingError as e:
            raise e


    def get_wrds_table(self, library, table, obs=-1, offset=0, columns=None, coerce_float=None, index_col=None, date_cols=None):
        """
        Create a :class:`pandas.DataFrame` from an entire table in the database.
        Based on the `WRDS-Py` package's method :meth:`wrds.sql.get_table`

        Parameters
        ___________
        library : str
            Postgres schema name
        table : str
            Postgress table name
        obs : int, default -1, [optional]
            Specifies the number of observations to pull from the table.
            An integer less than 0 will return the entire table.
        offset : int, default 0, [optional]
            Specifies the starting point for the query.
            An offset of 0 will start selecting from the beginning.
        columns : list or tuple, default None, [optional]
            Specifies the columns to be included in the output data frame.
        coerce_float : bool, default True, [optional]
            Attempt to convert values to non-string, non-numeric objects
            to floating point. Can result in loss of precision.
        date_cols : list or dict, default None, [optional]
            - list of column names to parse as date
            - dict of ``{column_name: format string}`` where format string is :meth:`date.strftime` compatible in case of
              parsing string times or is one of (D, s, ns, ms, us) in case of parsing integer timestamps
            - dict of ``{column_name: arg dict}``, where the arg dict corresponds to the keyword arguments of
                       :func:1pandas.to_datetime`
        index_col : str, or list, str, default None, [optional]
            Column(s) to set as `index(MultiIndex)`

        Returns
        _______
        None

        """
        if obs < 0:
            obsstmt = ''
        else:
            obsstmt = ' LIMIT {}'.format(obs)

        if columns is None:
            cols = '*'
        else:
            cols = ','.join(columns)

        sqlstmt = ('SELECT {cols} FROM {schema}.{table} {obsstmt} OFFSET {offset};'.\
                   format(cols=cols,
                          schema=library,
                          table=table,
                          obsstmt=obsstmt,
                          offset=offset))
        return self.raw_sql(sqlstmt, coerce_float=coerce_float, index_col=index_col, date_cols=date_cols)
