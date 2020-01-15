"""
Unittests for basedata.ops.cols submodule
"""
from unittest import TestCase

import numpy as np
import pandas as pd

from basedata.ops.cols import ColumnConversionsMixin

from test_databuild import make_dirty_numeric_dataframe,\
    make_dirty_datetime_dataframe, make_twocol_dataframe


numeric_dirt_list = ['', np.nan, '12,400', 'test', '15,987.00']
datetime_dirt_list = ['2010-10-10', 'test', ' ', np.nan, 123456789]
keycol = 'test'


class ColumnConversionsMixinTests(TestCase):
    """unittests for data.cols ColumnConversionsMixin class"""

    def create_ColumnConversions_class(self, df):
        """returns ColumnConversionsMixin instance for reuse in TestCase"""
        Conv = ColumnConversionsMixin()
        Conv.df = df
        return Conv

    def test_substitute_chars(self):
        """ensure substitute_chars strips non-match characters from column"""
        Conv = self.create_ColumnConversions_class(
            make_dirty_numeric_dataframe()
        )
        Conv.substitute_chars(keycol, '[^0-9]', '')
        assert False not in [
            isinstance(val, np.int32) for val
            in Conv.df[keycol].dropna().astype(int).values
        ]

    def test_check_nonnumeric(self):
        """ensure check_numeric returns value counts for all errors"""
        Conv = self.create_ColumnConversions_class(
            make_dirty_numeric_dataframe()
        )
        value_count_series = Conv.check_nonnumeric(keycol)
        value_test = np.array(numeric_dirt_list).astype(str)
        self.assertCountEqual(
            value_count_series.index.values.astype(str),
            value_test,
        )

    def test_to_numeric_coerce(self):
        """ensure to_numeric returns only numerics with coerce default"""
        Conv = self.create_ColumnConversions_class(
            make_dirty_numeric_dataframe()
        )
        Conv.to_numeric(keycol)
        assert False not in [
            isinstance(val, np.float64) for val
            in Conv.df[keycol].values
        ]

    def test_to_numeric_coerce_false(self):
        """ensure to_numeric returns non-numeric values with coerce=False"""
        Conv = self.create_ColumnConversions_class(
            make_dirty_numeric_dataframe()
        )
        Conv.to_numeric(keycol, coerce=False)
        value_count_series = Conv.check_nonnumeric(keycol)
        value_test = np.array(numeric_dirt_list).astype(str)
        self.assertCountEqual(
            value_count_series.index.values.astype(str),
            value_test,
        )
        self.assertIsInstance(Conv.df[keycol].values[0], int)

    def test_check_datetime(self):
        """ensure check_datetime returns value counts for all errors"""
        Conv = self.create_ColumnConversions_class(
            make_dirty_datetime_dataframe()
        )
        value_count_series = Conv.check_datetime(keycol)
        value_test = np.array(datetime_dirt_list[1:]).astype(str)
        self.assertCountEqual(
            value_count_series.index.values.astype(str),
            value_test,
        )

    def test_to_datetime_coerce(self):
        """ensure to_datetime returns only numerics with coerce default"""
        Conv = self.create_ColumnConversions_class(
            make_dirty_datetime_dataframe()
        )
        Conv.to_datetime(keycol)
        assert False not in [
            isinstance(val, np.datetime64) for val
            in Conv.df[keycol].values
        ]

    def test_to_datetime_coerce_false(self):
        """ensure to_datetime returns non-numeric values with coerce=False"""
        Conv = self.create_ColumnConversions_class(
            make_dirty_datetime_dataframe()
        )
        Conv.to_datetime(keycol, coerce=False)
        value_count_series = Conv.check_datetime(keycol)
        value_test = np.array(datetime_dirt_list[1:]).astype(str)
        self.assertCountEqual(
            value_count_series.index.values.astype(str),
            value_test,
        )
        self.assertIsInstance(Conv.df[keycol].values[0], str)

    def test_report_values(self):
        """ensure report_values reports all values and returns series"""
        df = make_dirty_numeric_dataframe()
        Conv = self.create_ColumnConversions_class(df)
        value_count_series = Conv.report_values(keycol)
        value_test = df[keycol].unique().astype(str)
        self.assertCountEqual(
            value_count_series.index.values.astype(str),
            value_test,
        )
        self.assertIsInstance(value_count_series, pd.Series)

    def test_map_values_exhaustive(self):
        """ensure map_values accurately maps values"""
        df = make_dirty_numeric_dataframe()
        Conv = self.create_ColumnConversions_class(df)
        map_keys = list(df[keycol].unique())[:-1]
        keys_len = len(map_keys)
        map_vals = list(range(keys_len))
        map_dict = dict(zip(map_keys, map_vals))
        Conv.map_values(keycol, map_dict, exhaustive=True)
        value_test = list(Conv.df[keycol].unique())
        self.assertCountEqual(map_vals, value_test[:-1])
        self.assertTrue(np.isnan(value_test[-1]))

    def test_map_values_not_exhaustive(self):
        """ensure map_values accurately maps values"""
        df = make_dirty_numeric_dataframe()
        Conv = self.create_ColumnConversions_class(df)
        map_keys = list(df[keycol].unique())[:-1]
        test_val = list(df[keycol].unique())[-1]
        keys_len = len(map_keys)
        map_vals = list(range(keys_len))
        map_dict = dict(zip(map_keys, map_vals))
        Conv.map_values(keycol, map_dict, exhaustive=False)
        value_test = list(Conv.df[keycol].unique())
        self.assertCountEqual(map_vals, value_test[:-1])
        self.assertEqual(test_val, value_test[-1])

    def test_map_column_names_inplace(self):
        """ensure map_column_names accurately maps names inplace"""
        df = make_dirty_numeric_dataframe()
        Conv = self.create_ColumnConversions_class(df)
        map_keys = list(Conv.df)
        keys_len = len(map_keys)
        map_vals = list(range(keys_len))
        map_dict = dict(zip(map_keys, map_vals))
        out = Conv.map_column_names(map_dict=map_dict)
        value_test = list(Conv.df)
        self.assertCountEqual(
            map_vals,
            value_test,
        )
        self.assertIsNone(out)

    def test_map_column_names_return(self):
        """ensure map_column_names returns df and not inplace when False"""
        df = make_dirty_numeric_dataframe()
        Conv = self.create_ColumnConversions_class(df)
        map_keys = list(Conv.df)
        keys_len = len(map_keys)
        map_vals = list(range(keys_len))
        map_dict = dict(zip(map_keys, map_vals))
        out = Conv.map_column_names(
            map_dict=map_dict,
            inplace=False
        )
        value_test = list(Conv.df)
        out_test = list(out)
        self.assertCountEqual(
            map_keys,
            value_test,
        )
        self.assertIsInstance(out, pd.DataFrame)
        self.assertCountEqual(
            out_test,
            map_vals,
        )

    def test_apply_function_lambda(self):
        """ensure apply_function works with lambda function"""
        colname_list = ['col1', 'col2']
        df = make_twocol_dataframe(colname_list[0], colname_list[1])
        Conv = self.create_ColumnConversions_class(df)
        series = Conv.apply_function(
            [colname_list[0]],
            target_column=None,
            function=lambda x: x,
            inplace=False,
            return_series=True,
        )
        self.assertIsInstance(series, pd.Series)
        self.assertCountEqual(series.values, df[colname_list[0]].values)

    def test_apply_function_multicol(self):
        """ensure apply_function works when applied to multiple columns"""
        colname_list = ['col1', 'col2']

        def test_func(row):
            return row[colname_list[0]] + row[colname_list[1]]

        df = make_twocol_dataframe(colname_list[0], colname_list[1])
        Conv = self.create_ColumnConversions_class(df)
        series = Conv.apply_function(
            colname_list,
            target_column=None,
            function=test_func,
            inplace=False,
            return_series=True,
            axis=1,
        )
        print(series)
        test_series = df[colname_list].sum(axis=1)
        print(test_series)
        self.assertIsInstance(series, pd.Series)
        self.assertCountEqual(series.values, test_series.values)

    def test_apply_function_saves_target_column(self):
        """ensure apply_function saves inplace to target_column"""
        colname_list = ['col1', 'col2', 'col3']
        df = make_twocol_dataframe(colname_list[0], colname_list[1])
        Conv = self.create_ColumnConversions_class(df)
        series = Conv.apply_function(
            [colname_list[0]],
            target_column=colname_list[2],
            function=lambda x: x,
            inplace=True,
            return_series=True,
        )
        self.assertCountEqual(series.values, df[colname_list[2]].values)

    def test_apply_function_raises_value_error(self):
        """ensure apply_function raises error for inplace no target_column"""
        colname_list = ['col1', 'col2', 'col3']
        df = make_twocol_dataframe(colname_list[0], colname_list[1])
        Conv = self.create_ColumnConversions_class(df)
        with self.assertRaises(ValueError):
            Conv.apply_function(
                [colname_list[0]],
                target_column=None,
                function=lambda x: x,
                inplace=True,
            )

    def test_add_column(self):
        """ensure add_column appends new column to self.df"""
        colname_list = ['col1', 'col2', 'col3']
        rows = 5
        df = make_twocol_dataframe(colname_list[0], colname_list[1], n=rows)
        Conv = self.create_ColumnConversions_class(df)
        Conv.add_column(colname_list[2], 1)
        self.assertEqual(sum(df[colname_list[2]].values), rows)
