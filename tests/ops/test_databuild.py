"""
This test submodule contains the functions and accompanying unit-tests used to
build the test datasets that are reused among the various basedata.ops modules'
unit-tests
"""
import os
import datetime
from unittest import TestCase
from tempfile import TemporaryDirectory
from random import randint
from collections import ChainMap

import numpy as np
import pandas as pd


numeric_dirt_list = ['', np.nan, '12,400', 'test', '15,987.00']
datetime_dirt_list = ['2010-10-10', 'test', ' ', np.nan, 123456789]
duplicates = [12345678] * 2
id_dirt_list = ['', '1234abcd', '-', '   5678', *duplicates]
keycol = 'test'


def generate_random_int(int_len=8):
    """returns a random integer (i.e. ID number) of given length"""
    min_val = 10**(int_len-1)
    max_val = (10**int_len)-1
    return randint(min_val, max_val)


def generate_random_datetime(start=datetime.datetime(2007, 1, 1),
                             end=datetime.datetime(2017, 1, 1),
                             string=True):
    """returns random datetime between two datetime objects"""
    delta = end - start
    int_delta = int(delta.total_seconds())
    random_second = randint(0, int_delta)
    datetime_value = start + datetime.timedelta(seconds=random_second)
    if string:
        return str(datetime_value)
    else:
        return datetime_value


def make_id_dict(n=5, int_len=8, keyname='id'):
    """generates dict containing randomly generated IDs"""
    values = [generate_random_int(int_len) for i in range(n)]
    return {keyname: values}


def make_datetime_dict(n=5, keyname='datetime'):
    """generates dict containing randomly generated datetimes"""
    values = [generate_random_datetime() for i in range(n)]
    return {keyname: values}


def make_dirt_dict(clean_dict, keyname, dirt_list):
    """generates updated dict with dirt values appended"""
    dirt_dict = {
        keyname: clean_dict[keyname] + dirt_list,
    }
    return dirt_dict


def merge_dicts(dicts_list):
    """generates a single dict from an arbitrary number of separate dicts"""
    return dict(ChainMap(*dicts_list))


def make_dataframe(dicts_list):
    """builds test dataframe using list of dicts"""
    df = pd.DataFrame.from_dict(merge_dicts(dicts_list))
    return df


def save_dataframe(dataframe, filename, **to_kwargs):
    """saves df to file, type is either csv or xlsx based on extension"""
    _, ext = os.path.splitext(filename)
    if ext == '.csv':
        dataframe.to_csv(filename, index=False, **to_kwargs)
    elif ext in ('.xls', '.xlsx'):
        dataframe.to_excel(filename, index=False, **to_kwargs)


def make_simple_dataframe():
    """builds and returns simple dataframe for TestCase reuse"""
    df_dict = make_id_dict()
    df = make_dataframe([df_dict])
    return df


def make_twocol_dataframe(colname_1='col1', colname_2='col2', n=5):
    """builds two column dataframe of random digits for TestCase reuse"""
    df_dict1 = make_id_dict(keyname=colname_1)
    df_dict2 = make_id_dict(keyname=colname_2)
    df = make_dataframe([df_dict1, df_dict2])
    return df


def save_simple_dataframe(tmp_dir, filename):
    """saves simple dataframe for TestCase reuse"""
    fp = os.path.join(tmp_dir, filename)
    df = make_simple_dataframe()
    save_dataframe(df, fp)
    return fp, df


def make_dirty_numeric_dataframe(keycol=keycol):
    """returns df with dirty IDs column for reuse in unittests"""
    numbers_dict = make_id_dict(keyname=keycol)
    numbers_dict[keycol] = numbers_dict[keycol] + numeric_dirt_list
    df = make_dataframe([numbers_dict])
    return df


def make_dirty_datetime_dataframe(keycol=keycol):
    """returns df with dirty IDs column for reuse in unittests"""
    dt_dict = make_datetime_dict(keyname=keycol)
    dt_dict[keycol] = dt_dict[keycol] + datetime_dirt_list
    df = make_dataframe([dt_dict])
    return df


def make_dirty_ids_dataframe(keycol=keycol):
    """returns df with dirty IDs column for reuse in unittests"""
    ids_dict = make_id_dict(keyname=keycol)
    ids_dict[keycol] = ids_dict[keycol] + id_dirt_list
    df = make_dataframe([ids_dict])
    return df


class DatabuildTests(TestCase):
    """unittests for test databuild functions"""

    def test_generate_random_int(self):
        """ensures specified random id generated"""
        int_len = 8
        result = generate_random_int(int_len)
        result_str = str(result)
        self.assertIsInstance(result, int)
        self.assertEqual(len(result_str), int_len)

    def test_generate_random_datetime_str(self):
        """ensures datetime string is generated"""
        str_len = 19
        result = generate_random_datetime()
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), str_len)

    def test_generate_random_datetime_object(self):
        """ensures datetime object is generated"""
        result = generate_random_datetime(string=False)
        self.assertIsInstance(result, datetime.datetime)

    def test_make_datetime_dict(self):
        """ensure accurate dict returned"""
        n, keyname = 5, 'test'
        dt_dict = make_datetime_dict(n=n, keyname=keyname)
        values = dt_dict[keyname]
        self.assertIsInstance(dt_dict, dict)
        self.assertIsInstance(values, list)
        self.assertEqual(len(values), n)

    def test_make_id_dict(self):
        """ensure accurate dict returned"""
        n, keyname = 5, 'test'
        id_dict = make_id_dict(n=n, keyname=keyname)
        values = id_dict[keyname]
        self.assertIsInstance(id_dict, dict)
        self.assertIsInstance(values, list)
        self.assertEqual(len(values), n)

    def test_make_dirt_dict(self):
        """ensure accurate dict returned"""
        keyname, clean_list, dirt_list = 'key', [1, 2, 3, 4], [5, 6, 7, 8]
        clean_dict = {keyname: clean_list}
        dirt_dict = make_dirt_dict(clean_dict, keyname, dirt_list)
        new_list = dirt_dict[keyname]
        self.assertIsInstance(dirt_dict, dict)
        self.assertIsInstance(new_list, list)
        self.assertEqual(len(new_list), 8)
        self.assertEqual(new_list, clean_list + dirt_list)

    def test_merge_dicts(self):
        """ensure merged dict returned"""
        dict_1, dict_2 = {'a': [1, 2, 3, 4, 5]}, {'b': [6, 7, 8, 9, 10]}
        dicts_list = [dict_1, dict_2]
        merged_dict = merge_dicts(dicts_list)
        test_dict = {**dict_1, **dict_2}
        self.assertIsInstance(merged_dict, dict)
        self.assertEqual(merged_dict, test_dict)

    def test_make_dataframe(self):
        """ensure accurate df returned"""
        keys, values = ['a', 'b'], [1, 2, 3, 4, 5]
        dict_list = [dict(zip(keys, [values, values]))]
        df = make_dataframe(dict_list)
        df_vals = list(df[keys[0]].values)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df_vals, values)

    def test_save_dataframe_csv(self):
        """ensure csv is saved"""
        with TemporaryDirectory() as tmp:
            name = 'test.csv'
            fp = os.path.join(tmp, name)
            df = pd.DataFrame(np.random.randn(3, 3), columns=list('ABC'))
            save_dataframe(df, fp)
            assert os.path.exists(fp)

    def test_save_dataframe_excel(self):
        """ensure excel is saved"""
        with TemporaryDirectory() as tmp:
            name = 'test.xls'
            fp = os.path.join(tmp, name)
            df = pd.DataFrame(np.random.randn(3, 3), columns=list('ABC'))
            save_dataframe(df, fp)
            assert os.path.exists(fp)

    def test_save_dataframe_excel_xml(self):
        """ensure excel xml format is saved"""
        with TemporaryDirectory() as tmp:
            name = 'test.xlsx'
            fp = os.path.join(tmp, name)
            df = pd.DataFrame(np.random.randn(3, 3), columns=list('ABC'))
            save_dataframe(df, fp)
            assert os.path.exists(fp)

    def test_make_simple_dataframe(self):
        """ensure make_simple_dataframe returns dataframe type"""
        df = make_simple_dataframe()
        self.assertIsInstance(df, pd.DataFrame)

    def test_make_twocol_dataframe(self):
        """ensure make_twocol_datafram returns two column dataframe"""
        colname_list = ['col1', 'col2']
        rows = 5
        df = make_twocol_dataframe(colname_list[0], colname_list[1], n=rows)
        test_list = list(df)
        test_rows = len(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertCountEqual(test_list, colname_list)
        self.assertEqual(test_rows, rows)

    def test_save_simple_dataframe(self):
        """ensure save_simple_dataframe returns fp, df, and path exists"""
        with TemporaryDirectory() as tmp:
            name = 'test.csv'
            fp, df = save_simple_dataframe(tmp, name)
            self.assertEqual(fp, os.path.join(tmp, name))
            self.assertIsInstance(df, pd.DataFrame)
            assert os.path.exists(fp)

    def test_make_dirty_numeric_dataframe(self):
        """ensure make_dirty_ids returns accurate dataframe"""
        df = make_dirty_numeric_dataframe()
        dirt_len = len(numeric_dirt_list)
        dirt_test = list(df[keycol].values)[-dirt_len:]
        self.assertIsInstance(df, pd.DataFrame)
        self.assertCountEqual(numeric_dirt_list, dirt_test)

    def test_make_dirty_datetime_dataframe(self):
        """ensure make_dirty_ids returns accurate dataframe"""
        df = make_dirty_datetime_dataframe()
        dirt_len = len(numeric_dirt_list)
        dirt_test = list(df[keycol].values)[-dirt_len:]
        self.assertIsInstance(df, pd.DataFrame)
        self.assertCountEqual(datetime_dirt_list, dirt_test)

    def test_make_dirty_ids_dataframe(self):
        """ensure make_dirty_ids returns accurate dataframe"""
        df = make_dirty_ids_dataframe()
        dirt_len = len(id_dirt_list)
        dirt_test = list(df[keycol].values)[-dirt_len:]
        self.assertIsInstance(df, pd.DataFrame)
        self.assertCountEqual(id_dirt_list, dirt_test)
