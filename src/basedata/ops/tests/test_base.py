"""
Unit-tests for basedata.ops.base submodule
"""
import os
from unittest import TestCase
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd

from ..base import BaseDataClass, inplace_return_series,\
    regex_sub_value, regex_replace_value
from .test_databuild import make_simple_dataframe, save_simple_dataframe,\
    make_dirty_numeric_dataframe, make_dirty_datetime_dataframe


keycol = 'test'


class MiscFunctionsTest(TestCase):
    """unittests for misc functions located in data/ids submodule"""

    def test_inplace_return_series_inplace(self):
        """ensure inplace_return_series makes inplace changes"""
        df = make_dirty_numeric_dataframe()
        series = make_dirty_datetime_dataframe()[keycol]
        series_test = inplace_return_series(
            df,
            keycol,
            series,
            inplace=True,
            return_series=False,
        )
        self.assertIsNone(series_test)
        self.assertSequenceEqual(
            df[keycol].values.tolist(),
            series.values.tolist()
        )

    def test_inplace_return_series_inplace_target_col(self):
        """ensure inplace_return_series makes inplace changes to target_col"""
        df = make_dirty_numeric_dataframe()
        series_original = df[keycol]
        series_target = make_dirty_datetime_dataframe()[keycol]
        target_column = 'test_target'
        series_test = inplace_return_series(
            df,
            keycol,
            series_target,
            inplace=True,
            return_series=False,
            target_column=target_column
        )
        self.assertIsNone(series_test)
        self.assertSequenceEqual(
            df[keycol].values.tolist(),
            series_original.values.tolist()
        )
        self.assertSequenceEqual(
            df[target_column].values.tolist(),
            series_target.values.tolist()
        )

    def test_inplace_return_series_return(self):
        """ensure inplace_return_series returns series"""
        df = make_dirty_numeric_dataframe()
        series_original = df[keycol]
        series = make_dirty_datetime_dataframe()[keycol]
        series_test = inplace_return_series(
            df,
            keycol,
            series,
            inplace=False,
            return_series=True,
        )
        self.assertSequenceEqual(
            series.values.tolist(),
            series_test.values.tolist()
        )
        self.assertSequenceEqual(
            df[keycol].values.tolist(),
            series_original.values.tolist()
        )

    def test_regex_sub_value(self):
        """ensures sub_value_regex returns accurate values"""
        inputs = ['1234', '123abc4', '', 1234, None, np.nan]
        outputs = ['1234', '1234', np.nan, np.nan, np.nan, np.nan]
        pattern = '[^0-9]'
        outputs_test = [
            regex_sub_value(input_val, pattern)
            for input_val in inputs
        ]
        self.assertEqual(outputs, outputs_test)

    def test_regex_replace_value(self):
        """ensures sub_value_regex returns accurate values"""
        inputs = ['1234', '12345', '123a5', '', 1234, None, np.nan]
        outputs = ['1234', 'test', 'test', 'test', np.nan, np.nan, np.nan]
        pattern = '[0-9]{4}$'
        outputs_test = [
            regex_replace_value(input_val, 'test', pattern)
            for input_val in inputs
        ]
        self.assertEqual(outputs, outputs_test)


class BaseDataClassTests(TestCase):
    """Tests to ensure class data.BaseDataClass functions properly"""

    def test_from_file_csv(self):
        """ensure csv is read and stored to BaseDataClass class"""
        with TemporaryDirectory() as tmp:
            fp, df_test = save_simple_dataframe(tmp, 'test.csv')
            df_read = BaseDataClass.from_file(fp).df
            self.assertEqual(
                pd.testing.assert_frame_equal(df_test, df_read),
                None,
            )

    def test_from_file_xls(self):
        """ensure xls is read and stored to BaseDataClass class"""
        with TemporaryDirectory() as tmp:
            fp, df_test = save_simple_dataframe(tmp, 'test.xls')
            df_read = BaseDataClass.from_file(fp).df
            self.assertEqual(
                pd.testing.assert_frame_equal(df_test, df_read),
                None,
            )

    def test_from_file_xlsx(self):
        """ensure xlsx is read and stored to BaseDataClass class"""
        with TemporaryDirectory() as tmp:
            fp, df_test = save_simple_dataframe(tmp, 'test.xlsx')
            df_read = BaseDataClass.from_file(fp).df
            self.assertEqual(
                pd.testing.assert_frame_equal(df_test, df_read),
                None,
            )

    def test_from_file_fail(self):
        """ensure from_file fails elegantly with wrong filetype read"""
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "test.txt")
            open(fp, 'a').close()
            assert os.path.exists(fp)
            with self.assertRaises(TypeError):
                BaseDataClass.from_file(fp)

    def test_from_file_inputdf_persists(self):
        """ensure input_df persist only when specified"""
        with TemporaryDirectory() as tmp:
            fp, df_test = save_simple_dataframe(tmp, 'test.xlsx')
            df_read = BaseDataClass.from_file(fp, copy_input=True).input_df
            self.assertEqual(
                pd.testing.assert_frame_equal(df_test, df_read),
                None,
            )
            with self.assertRaises(AttributeError):
                BaseDataClass.from_file(fp).input_df

    def test_from_object_df(self):
        """ensure dataframe object is read and stored to BaseDataClass class"""
        df_test = make_simple_dataframe()
        df_read = BaseDataClass.from_object(df_test).df
        self.assertEqual(
            pd.testing.assert_frame_equal(df_test, df_read),
            None,
        )

    def test_from_object_class(self):
        """ensure class.df object is read and stored to BaseDataClass class"""
        df_test = make_simple_dataframe()
        Base_object = BaseDataClass.from_object(df_test)
        df_read = BaseDataClass.from_object(Base_object).df
        self.assertEqual(
            pd.testing.assert_frame_equal(df_test, df_read),
            None,
        )

    def test_from_object_fail(self):
        """ensure from_object fails elegantly with invalid object"""
        class InvalidClass(object):
            pass
        Invalid_object = InvalidClass()
        with self.assertRaises(TypeError):
            BaseDataClass.from_object(Invalid_object)

    def test_to_file(self):
        """ensure to_file saves self.df to disk"""
        with TemporaryDirectory() as tmp:
            df_test = make_simple_dataframe()
            Base = BaseDataClass.from_object(df_test)
            fp_save = os.path.join(tmp, "test_save.csv")
            Base.to_file(fp_save)
            assert os.path.exists(fp_save)
