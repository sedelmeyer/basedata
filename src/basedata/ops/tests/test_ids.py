"""
Unittests for basedata.ops.ids submodule
"""
import os
from unittest import TestCase
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd

from ..ids import DedupeMixin, ValidIDsMixin
from .test_databuild import make_dirty_ids_dataframe


duplicates = [12345678] * 2
id_dirt_list = ['', '1234abcd', '-', '   5678', *duplicates]
keycol = 'ids'


class DedupeMixinTests(TestCase):
    """unittests for DedupeMixin class methods"""

    def create_Dedupe_class(self):
        """returns DedupeMixin instance for reuse in TestCase"""
        df = make_dirty_ids_dataframe(keycol)
        Dedupe = DedupeMixin()
        Dedupe.df = df
        return Dedupe

    def test_check_dupes_not_hasattr(self):
        """ensure accurate df saves to duperecords if attr does not exist"""
        Dedupe = self.create_Dedupe_class()
        Dedupe._check_dupes(keycol)
        dupes_dict = Dedupe.duperecords
        dupes_df = dupes_dict[keycol]
        self.assertIsInstance(dupes_dict, dict)
        self.assertIsInstance(dupes_df, pd.DataFrame)
        self.assertEqual(list(dupes_df[keycol].values), duplicates)

    def test_check_dupes_hasattr(self):
        """ensure accurate df saves to duperecords if attr does exist"""
        test_item, test_key = ['item'], 'test'
        Dedupe = self.create_Dedupe_class()
        Dedupe.duperecords = dict({test_key: test_item})
        Dedupe._check_dupes(keycol)
        dupes_dict = Dedupe.duperecords
        dupes_df = dupes_dict[keycol]
        self.assertEqual(list(dupes_df[keycol].values), duplicates)
        self.assertEqual(dupes_dict[test_key], test_item)

    def test_report_dupes_returns(self):
        """ensure report_dupes returns accurate df"""
        Dedupe = self.create_Dedupe_class()
        df = Dedupe.report_dupes(keycol)
        dupes_list = list(df.values)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(dupes_list, duplicates)

    def test_report_dupes_to_file(self):
        """ensure report_dupes saves .csv when to_file specified"""
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, 'test.csv')
            Dedupe = self.create_Dedupe_class()
            Dedupe.report_dupes(keycol, to_file=fp, return_df=False)
            assert os.path.exists(fp)

    def test_report_dupes_to_file_index(self):
        """ensure report_dupes saves .csv when to_file specified"""
        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, 'test.csv')
            Dedupe = self.create_Dedupe_class()
            Dedupe.report_dupes(keycol, to_file=fp, return_df=False)
            df = pd.read_csv(fp)
            self.assertEqual(len(df['index_id']), len(duplicates))

    def test_drop_dupes_drop(self):
        """ensure drop_dupes drops rows from self.df"""
        Dedupe = self.create_Dedupe_class()
        len_df = len(Dedupe.df)
        index_list = list(Dedupe.report_dupes(keycol).index)[0]
        Dedupe.drop_dupes(keycol, index_list, validate=True)
        new_len = len(Dedupe.df)
        self.assertEqual(new_len, len_df-len(set(duplicates)))

    def test_drop_dupes_validate(self):
        """ensure drop_dupes raises exception when validate==True"""
        Dedupe = self.create_Dedupe_class()
        with self.assertRaises(AssertionError):
            Dedupe.drop_dupes(keycol, [0], validate=True)

    def test_flush_duperecords_del(self):
        """ensure flush_duperecords deletes class attribute"""
        Dedupe = self.create_Dedupe_class()
        Dedupe.duperecords = 'test'
        assert hasattr(Dedupe, 'duperecords')
        Dedupe.flush_duperecords()
        assert not hasattr(Dedupe, 'duperecords')

    def test_flush_duperecords_pass(self):
        """ensure flush_duperecords pass when class attribute doesn't exist"""
        Dedupe = self.create_Dedupe_class()
        assert not hasattr(Dedupe, 'duperecords')
        Dedupe.flush_duperecords()


class ValidIDsMixinTests(TestCase):
    """unittests for ValidIDsMixin class methods"""

    def create_ValidIDs_class(self):
        """returns DedupeMixin instance for reuse in TestCase"""
        df = make_dirty_ids_dataframe(keycol)
        Valid = ValidIDsMixin()
        Valid.df = df
        return Valid

    def test_strip_nonnumeric(self):
        """ensure strip_nonnumeric strips nonnumeric characters from column"""
        Valid = self.create_ValidIDs_class()
        Valid.strip_nonnumeric(keycol)
        assert False not in [
            isinstance(val, np.int32) for val
            in Valid.df[keycol].dropna().astype(int).values
        ]

    def test_strip_nonnumeric_returns_series(self):
        """ensure strip_nonnumeric returns series when specified"""
        Valid = self.create_ValidIDs_class()
        series = Valid.strip_nonnumeric(keycol, return_series=True)
        self.assertIsInstance(series, pd.Series)

    def test_report_offlenIDs(self):
        """ensure report_offlenIDs returns accurate value_counts series"""
        Valid = self.create_ValidIDs_class()
        target_len = 8
        series = Valid.report_offlenIDs(keycol, target_len=target_len)
        vals = series.index.astype(str)
        print(series)
        print(vals)
        assert target_len not in [len(val) for val in vals]
        self.assertIsInstance(series, pd.Series)

    def test_remove_offlenIDs(self):
        """ensure offlenIDs replaced with np.nan values"""
        Valid = self.create_ValidIDs_class()
        target_len = 8
        Valid.remove_offlenIDs(keycol, target_len=target_len)
        assert False not in [
            target_len == len(val) for val in Valid.df[keycol].dropna().values
        ]

    def test_remove_offlenIDs_return_series(self):
        """ensure offlenIDs replaced with np.nan values"""
        Valid = self.create_ValidIDs_class()
        target_len = 8
        series = Valid.remove_offlenIDs(
            keycol,
            target_len=target_len,
            return_series=True)
        self.assertIsInstance(series, pd.Series)

    def test_replace_blankIDs(self):
        """ensure blank ids are replaced with values from target column"""
        test_col, test_val, target_len = 'test', 'test', 8
        Valid = self.create_ValidIDs_class()
        Valid.df[test_col] = test_val
        Valid.remove_offlenIDs(keycol, target_len=target_len)
        Valid.replace_blankIDs(keycol, replace_col=test_col)
        new_values = Valid.report_offlenIDs(
            keycol,
            target_len=target_len
        ).index
        assert False not in [test_val == val for val in new_values]

    def test_replace_blankIDs_return_series(self):
        """ensure blank ids are replaced with values from target column"""
        test_col, test_val, target_len = 'test', 'test', 8
        Valid = self.create_ValidIDs_class()
        Valid.df[test_col] = test_val
        Valid.remove_offlenIDs(keycol, target_len=target_len)
        series = Valid.replace_blankIDs(
            keycol,
            replace_col=test_col,
            return_series=True,
        )
        self.assertIsInstance(series, pd.Series)

    def test_drop_blankID_rows(self):
        """ensure blankID rows are dropped from dataframe and index reset"""
        target_len = 8
        Valid = self.create_ValidIDs_class()
        num_all = len(Valid.df)
        Valid.strip_nonnumeric(keycol)
        num_offlen = sum(Valid.report_offlenIDs(keycol, target_len=target_len))
        Valid.remove_offlenIDs(keycol, target_len=target_len)
        Valid.drop_blankID_rows(keycol)
        num_test = len(Valid.df)
        idx_test = max(Valid.df.index.values)
        self.assertEqual(num_all - num_offlen, num_test)
        self.assertEqual(idx_test + 1, num_test)
