"""
This submodule basedata.ops mixin classes for cleaning unique ID values.

The functionality of these mixin classes is aggregated in the basedata.ops
BaseDataOps class.
"""
import numpy as np
import pandas as pd

from .base import inplace_return_series, regex_sub_value, regex_replace_value


class DedupeMixin(object):
    """
    Mixin class methods used to inspect dataframe objects for duplicate key
    values, analyze duplicate key records, and to remove duplicate key records
    once identified.
    """

    def _check_dupes(self, column):
        """
        Checks column for duplicate key values

        :param column: str name of column to check for duplicate values
        :return: dict if no self.duperecords attribute exists, a the dict
            is created and a key is created named for the column, and the item
            saved to that key is a pandas.Dataframe of all records associated
            with that column's duplicate values
        """
        if not hasattr(self, 'duperecords'):
            self.duperecords = dict()
        value_counts = self.df[column].value_counts()
        dupekeys = list(value_counts[value_counts > 1].index)
        self.duperecords[column] = self.df.loc[self.df[column].isin(dupekeys)]

    def report_dupes(self, column, to_file=None, return_df=True):
        """
        Invokes a dataframe consisting of records associated with duplicate
        values in the specified column and saves csv of dataframe to file if
        specified.

        In saved csv, duplicate records indices are save in column 'index_id'

        :param column: str name of column to check for duplicate values
        :param to_file: str optional filename if a csv of the duplicates
            dataframe should be saved. Default is None.
        :param return_df: bool indicates whether or not to return dataframe
        :returns: pandas.Dataframe of all records associated with column dupes
        """
        self._check_dupes(column)
        if to_file:
            self.duperecords[column].to_csv(
                to_file,
                index=True,
                index_label='index_id'
            )
        if return_df:
            return self.duperecords[column]

    def drop_dupes(self, column, index_list, validate=True):
        """
        Drops rows in self.df based on input index_list values, will
        return print message if any duplicate vlaues remain in the specified
        column.

        :param index_list: list indices to be dropped
        :param validate: bool raises exception if duplicates still remain
        """
        self.df = self.df.drop(
            index_list,
        ).reset_index(
            drop=True,
        )
        self._check_dupes(column)
        if len(self.duperecords[column]) > 0 and validate:
            raise AssertionError(
                "Duplicate keys still exist in the '{0}' column.\n\nInspect"
                " class object's duperecords dataframe for this column to\n"
                "identify remaining duplicates for the following column "
                "values:\n{1}"
                .format(
                    column,
                    list(set(self.duperecords[column][column])),
                )
            )

    def flush_duperecords(self):
        """
        Deletes self.duperecords dictionary from class __dict__ to free memory
        """
        if not hasattr(self, 'duperecords'):
            pass
        else:
            del self.__dict__['duperecords']


class ValidIDsMixin(object):
    """
    functions for validating and modifying ID values
    """

    def strip_nonnumeric(self, column, pattern='[^0-9]', val_sub='',
                         val_exception=np.nan, val_none=np.nan,
                         inplace=True, return_series=False,
                         target_column=None):
        """
        strips nonnumeric characters from column values

        :param pattern: str Regex pattern specifying which types of charaters
            to substiture with val_sub str, optional, default='[^0-9]'
        :param val_sub: str character(s) with which to replace pattern values,
            default = ''
        :param val_exception: str or numpy.nan value to return for instances
            where an exception is raised
        :param val_none: str or numpy.nan value to return for instances of
            either None or np.nan
        :param inplace: bool whether to make changes to self.df in place,
            default=True
        :param return_series: bool whether to return modified pandas.Series
            object, default=False
        :return: pandas.Series if return_series is specified as True
        """
        series = self.df[column].copy().astype(str).apply(
            lambda x: regex_sub_value(
                val=x,
                pattern=pattern,
                val_sub=val_sub,
                val_exception=val_exception,
                val_none=val_none
            )
        )
        return inplace_return_series(self.df, column, series,
                                     inplace, return_series, target_column)

    def report_offlenIDs(self, column, target_len=8, dropna=False):
        """
        generate a value_counts report with all of the column values
        with number of characters not matching the specified target length

        :param target_len: int specifying length of a valid id, default=8
        :param dropna: bool indicating whether to include np.nan values in
            the output value_counts series, default=False
        :returns: pandas.Series of the IDs not matching the target_len
        """
        value_counts = self.df.loc[
            self.df[column].astype(str).str.len() != target_len
        ][column].value_counts(dropna=dropna)
        return value_counts

    def remove_offlenIDs(self, column, target_len=8, pattern='[0-9]',
                         val_new=np.nan, val_exception=np.nan,
                         inplace=True, return_series=False,
                         target_column=None):
        """
        removes all IDs not matching the desired character length and replaces
        them with a chosen replacement value

        :param target_len: int specifying length of a valid id, default=8
        :param pattern: str Regex pattern specifying which types of characters
            to substiture with val_sub str, default='[0-9]'
        :param val_new: str or numpy.nan value with which to replace values
            of incorrect length, default=numpy.nan
        :param val_exception: str or numpy.nan value to return for instances
            where an exception is raised, default=numpy.nan
        :param inplace: bool whether to make changes to self.df in place,
            default=True
        :param return_series: bool whether to return modified pandas.Series
            object, default=False
        :return: pandas.Series of column values after replacing offlenIDs
        """
        series = self.df[column].copy().astype(str).apply(
            lambda x: regex_replace_value(
                val=x,
                val_new=val_new,
                pattern=''.join([pattern, '{{{0}}}$']).format(target_len),
                val_exception=val_exception,
            )
        )
        return inplace_return_series(self.df, column, series,
                                     inplace, return_series, target_column)

    def replace_blankIDs(self, column, replace_col,
                         inplace=True, return_series=False,
                         target_column=None):
        """
        replaces all blank ID values with the corresponding values from
        a different value in the same dataframe

        :param replace_col: str name of column with replacement values
        :param inplace: bool make changes to self.df inplace, default=True
        :param return_series: bool whether to return modified pandas.Series
            object, default=False
        """
        series = self.df.copy().apply(
            lambda row:
            row[replace_col] if pd.isnull(row[column])
            else row[column],
            axis=1,
        )
        return inplace_return_series(self.df, column, series,
                                     inplace, return_series, target_column)

    def drop_blankID_rows(self, column):
        """
        drops all rows from self.df where the choosen column value
        is a nan value

        changes to self.df are made inplace and the df index is reset to
        contiguous values 0-n.
        """
        self.df = self.df.dropna(
            subset=[column],
        ).reset_index(drop=True)
