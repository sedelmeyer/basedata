"""
This submodule basedata.ops mixin classes for manipulating column values and
column names.

The functionality of these mixin classes is aggregated in the basedata.ops
BaseDataOps class.
"""
import numpy as np
import pandas as pd

from .base import inplace_return_series, regex_sub_value


class ColumnConversionsMixin(object):
    """
    Mixin class methods and associated tools for converting column
    values to specific types
    """

    def substitute_chars(self, column, pattern, val_sub,
                         val_exception=np.nan, val_none=np.nan,
                         inplace=True, return_series=False,
                         target_column=None):
        """
        Strips or replaces characters from column values.

        When val_sub is '', this method strips the characters specified by
        the regex pattern. If the objective is to replace the specified
        characters, specify the desired replacement characters using val_sub
        (i.e. val_sub='substring')

        :param column: str name of column on which to apply this operation
        :param pattern: str Regex pattern specifying which types of characters
            to substiture with val_sub str
        :param val_sub: str character(s) with which to replace pattern values
        :param val_exception: str or numpy.nan value to return for instances
            where an exception is raised, default=numpy.nan
        :param val_none: str or numpy.nan value to return for instances of
            either None or np.nan, default=numpy.nan
        :param inplace: bool whether to make changes to self.df in place,
            default=True
        :param return_series: bool whether to return modified pandas.Series
            object, default=False
        :param target_column: None or string name of new column created, if
            None and inplace=True, modified series replaces original column,
            default=None
        :return: pandas.Series if return_series is specified as True
        """
        series = self.df[column].copy().astype(str).apply(
            lambda x: regex_sub_value(
                val=x,
                pattern=pattern,
                val_sub=val_sub,
                val_exception=val_exception,
                val_none=val_none,
            )
        )
        return inplace_return_series(self.df, column, series,
                                     inplace, return_series, target_column)

    def check_nonnumeric(self, column, dropna=False, **kwargs):
        """
        returns a value_counts series reporting all column values that cannot
        be directly converted to numeric data types int or float

        :param column: str name of column to check for nonnumeric
        :param dropna: bool optional, whether to drop na values from resulting
            value_count series, default=False
        :param **kwargs: additional arguments for pandas value_counts method
        :return: pandas.Series object
        """
        value_counts = self.df[
            pd.to_numeric(
                self.df[column].astype(str),
                errors='coerce'
            ).isnull()
        ][column].value_counts(dropna=dropna, **kwargs)
        return value_counts

    def to_numeric(self, column, coerce=True,
                   inplace=True, return_series=False, target_column=None):
        """
        wrapper for pandas to_numeric method, which converts column values to
        a numeric data type (int or float)

        :param column: str name of column to convert to numeric
        :param coerce: bool optional, specifies whether to 'coerce'
            non-convertable values to numpy.nan if True or to leave those
            values as is if False, default=True
        :param inplace: bool whether to make changes to self.df in place,
            default=True
        :param return_series: bool whether to return modified pandas.Series
            object, default=False
        :param target_column: None or string name of new column created, if
            None and inplace=True, modified series replaces original column,
            default=None
        :return: pandas.Series if return_series is specified as True
        """
        series = pd.to_numeric(
            self.df[column],
            errors='coerce' if coerce else 'ignore'
        )
        return inplace_return_series(self.df, column, series,
                                     inplace, return_series, target_column)

    def check_datetime(self, column, dropna=False, **kwargs):
        """
        returns a value_counts series reporting all column values that cannot
        be directly converted to a datetime data type

        :param column: str name of column to check for datetime conversion
        :param dropna: bool optional, whether to drop na values from resulting
            value_count series, default=False
        :param **kwargs: additional arguments for pandas value_counts method
        :return: pandas.Series object
        """
        value_counts = self.df[
            pd.to_datetime(
                self.df[column].astype(str),
                errors='coerce'
            ).isnull()
        ][column].value_counts(dropna=dropna, **kwargs)
        return value_counts

    def to_datetime(self, column, coerce=True,
                    inplace=True, return_series=False, target_column=None):
        """
        wrapper for pandas to_numeric method, which converts column values to
        a datetime data type

        :param column: str name of column to convert to datetime
        :param coerce: bool optional, specifies whether to 'coerce'
            non-convertable values to numpy.nan if True or to leave those
            values as is if False, default=True
        :param inplace: bool whether to make changes to self.df in place,
            default=True
        :param return_series: bool whether to return modified pandas.Series
            object, default=False
        :param target_column: None or string name of new column created, if
            None and inplace=True, modified series replaces original column,
            default=None
        :return: pandas.Series if return_series is specified as True
        """
        series = pd.to_datetime(
            self.df[column],
            errors='coerce' if coerce else 'ignore'
        )
        return inplace_return_series(self.df, column, series,
                                     inplace, return_series, target_column)

    def report_values(self, column, dropna=False, **kwargs):
        """
        returns a value_counts series reporting all unique column values

        :param column: str name of column to check for unique values
        :param dropna: bool optional, whether to drop na values from resulting
            value_count series, default=False
        :param **kwargs: additional arguments for pandas value_counts method
        :return: pandas.Series object
        """
        value_counts = self.df[column].value_counts(dropna=False, **kwargs)
        return value_counts

    def map_values(self, column, map_dict, na_action=None, exhaustive=False,
                   inplace=True, return_series=False, target_column=None):
        """
        maps existing column values to new value based on input dictionary

        acts as a simple wrapper for the pandas Series.map method

        :param column: str name of column in which value will be mapped
        :param map_dict: dict mapping {current_value: new_value}
        :param na_action: None or 'ignore', if 'ignore' propogate NaN values
            without passing them to the mapping correspondence, defaul=None
        :param exhaustive: bool whether or not value map is expected to affect
            all values in the series, if True, any values not matching map_dict
            will be converted to np.nan, if False, they retain their original
            values. default=False
        :param inplace: bool whether to make changes to self.df in place,
            default=True
        :param return_series: bool whether to return modified pandas.Series
            object, default=False
        :param target_column: None or string name of new column created, if
            None and inplace=True, modified series replaces original column,
            default=None
        :return: pandas.Series if return_series is specified as True
        """
        if exhaustive:
            series = self.df[column].copy().map(map_dict, na_action)
        else:
            series = self.df[column].copy().map(
                map_dict,
                na_action
            ).fillna(self.df[column].copy())
        return inplace_return_series(self.df, column, series,
                                     inplace, return_series, target_column)

    def map_column_names(self, map_dict, inplace=True):
        """
        maps existing column names to new names based on input dictionary

        acts as a simple wrapper for the pandas DataFrame.rename method, when
        columns are specified in that functions parameters

        :param map_dict: dict mapping {current_value: new_value}
        :param inplace: bool whether to make changes to self.df in place,
            default=True
        :return: pandas.DataFrame if inplace is specified as False
        """
        return self.df.rename(columns=map_dict, inplace=inplace)

    def apply_function(self, column_list, function, target_column,
                       inplace=True, return_series=False, **kwargs):
        """
        Applies function to dataframe object, using pandas.DataFrame.apply()
        method.

        :param column_list: list column name(s) against which to apply function
        :param function: function to apply to dataframe object
        :param target_column: None or string name of new column created, if
            inplace=True target_column name must be specified
        :param inplace: bool whether to make changes to self.df in place,
            default=True
        :param return_series: bool whether to return modified pandas.Series
            object, default=False
        :param **kwargs: optional keyword args to for pandas apply method.
            Axis=1 is required whenever the function is applied to multiple
            input columns
        :return: pandas.Series if return_series is specified as True
        """
        if inplace and not target_column:
            raise ValueError(
                'When inplace == True a target_column name must be specified.'
            )
        result = self.df[column_list].copy().apply(function, **kwargs)
        is_df = isinstance(result, pd.DataFrame)
        series = result.iloc[:, 0] if is_df else result
        return inplace_return_series(self.df, target_column, series,
                                     inplace, return_series, target_column)
