"""
This module contains the BaseDataClass parent class and common functions that
are that are reused across basedata.ops submodules.
"""
import os
import re

import numpy as np
import pandas as pd


def inplace_return_series(dataframe, column, series,
                          inplace, return_series, target_column=None):
    """
    helper function to reuse throughout library. It applies logic for
    performing inplace series transformations and returning copies of
    modified series

    :param dataframe: pandas.DataFrame for which we are modifying series
    :param column: str name of target column for our series
    :param series: pandas.Series
    :param inplace: bool whether we wish to overwrite existing column
        with series
    :param return_series: bool whether we wish to return a copy of the
        pandas.Series object
    :return: pandas.Series
    """
    if inplace:
        dataframe[target_column if target_column else column] = series
    if return_series:
        return series


def regex_sub_value(val, pattern, val_sub='',
                    val_exception=np.nan, val_none=np.nan):
    """
    Replaces characters in a string value based on specified Regex pattern

    :param val: str input value to be evaluated by Regex re.sub function
    :param pattern: str regex pattern used to identify characters to subsitute
    :param val_sub: str value to substitute for specified input characters
    :param val_exception: str or np.nan value to return in input value raises
        an exception (default=np.nan)
    :param val_none: str or np.nan value to return if input value is none or
        np.nan (default=np.nan)
    :return: str value based on input parameters
    """
    try:
        stripped = re.sub(pattern, val_sub, val)
        new_val = val_none if stripped == '' else stripped
        return new_val
    except:
        return val_exception


def regex_replace_value(val, val_new, pattern,
                        val_exception=np.nan):
    """
    Replaces string value if Regex pattern is not satisfied by the input value

    :param val: str input value to be evaluated by Regex re.match function
    :param pattern: str regex pattern used to identify values to replace
    :param val_new: str replacement value if input pattern is not satisfied
    :param val_exception: str or np.nan value to return in input value raises
        an exception (default=np.nan)
    :param val_none: str or np.nan value to return if input value is none or
        np.nan (default=np.nan)
    :return: str output value based on input parameters
    """
    try:
        if not bool(re.match(pattern, val)):
            return val_new
        else:
            return val
    except:
        return val_exception


class BaseDataClass(object):
    """
    BaseDataOps class manages base read/write operations and instantiates
    self.df for child classes across data submodule classes
    """

    def __init__(self, input_df, copy_input):
        if copy_input:
            self.input_df = input_df.copy()  # input df persists for reference
        self.df = input_df  # subset changes applied to this df

    @classmethod
    def from_file(cls, filename, copy_input=False, **read_kwargs):
        """
        Invokes BaseDataOps class and reads input csv or excel from disk
        into a pandas.DataFrame object.

        :param filename: str filename of .csv, .xls, or .xlsx file to be read
        :param copy_input: bool to specify whether self.input_df persists
        :param read_kwargs: optional args to pandas.DataFrame.read_...()
        :return: pandas.DataFrame and copy_input bool as class variables
        """
        _, ext = os.path.splitext(filename)
        if ext == '.csv':
            input_df = pd.read_csv(filename, **read_kwargs)
        elif ext in ('.xls', '.xlsx'):
            input_df = pd.read_excel(filename, **read_kwargs)
        else:
            raise TypeError(
                'from_file reads only .csv, .xls, or .xlsx filetypes'
            )
        return cls(input_df, copy_input)

    @classmethod
    def from_object(cls, input_object, copy_input=False):
        """
        Invokes BaseDataOps class and reads input df from class or df
        object.

        :param input_object: object to be read into BaseDataOps
        :param copy_input: bool to specify whether self.input_df persists
        :return: pandas.DataFrame and copy_input bool as class variables
        """
        if isinstance(input_object, pd.DataFrame):
            input_df = input_object.copy()
        else:
            try:
                if isinstance(input_object.df, pd.DataFrame):
                    input_df = input_object.df.copy()
                    # TODO implement self.log = input_object.log.copy()
            except:
                raise TypeError(
                    'input_object must be either pandas.DataFrame or '
                    'class object with input_object.df attribute of type '
                    'pandas.DataFrame.'
                )
        return cls(input_df, copy_input)

    def to_file(self, target_filename, **to_csv_kwargs):
        """
        Saves current version of self.df to file in csv format

        :param target_filename: str filename to which csv should be written
        :param to_csv_kwargs: optional args to pandas.DataFrame.to_csv()
        """
        # TODO: to_file saves will need trigger log file in future versions
        self.df.to_csv(target_filename, index=False, **to_csv_kwargs)
