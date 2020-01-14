"""
unittests for basedata.inventory submodule functions
"""
import os
from pathlib import Path
from unittest import TestCase
from tempfile import TemporaryDirectory

import numpy as np
import pandas as pd

from basedata.inventory import list_subdir_paths, list_subdirs,\
    list_files_with_extensions, list_datafiles, make_datafile_array,\
    make_datafile_dataframe


testdir_list = [
    'test1',
    'test2',
    'test3',
]

testfile_list = [
    'test.csv',
    'test.txt',
    'test.xls',
    'test.pptx',
]


def make_subdirs(root_dir, subdir_list):
    """makes subdirectories in root directory for use in unittests"""
    for subdir in subdir_list:
        dirpath = os.path.join(root_dir, subdir)
        os.mkdir(dirpath)


def make_files(dir_path, file_list):
    """makes files in directory path for use in unittests"""
    for filename in file_list:
        filepath = os.path.join(dir_path, filename)
        Path(filepath).touch()


def make_dirfiles(root_dir, subdir_list, file_list):
    """makes subdirectories and populates them with test files for unittests"""
    make_subdirs(root_dir, subdir_list)
    [
        make_files(os.path.join(root_dir, subdir), file_list)
        for subdir in subdir_list
    ]


class DirBuildTests(TestCase):
    """unittests for subdirectory and test files build functions"""

    def test_make_subdirs(self):
        """ensure subdirectories are created"""
        with TemporaryDirectory() as tmp:
            make_subdirs(tmp, testdir_list)
            listdir = os.listdir(tmp)
            self.assertCountEqual(listdir, testdir_list)

    def test_make_files(self):
        """ensure test files are created"""
        with TemporaryDirectory() as tmp:
            make_files(tmp, testfile_list)
            listdir = os.listdir(tmp)
            self.assertCountEqual(listdir, testfile_list)

    def test_make_dirfiles(self):
        """ensure subdirectories are populated with test files"""
        with TemporaryDirectory() as tmp:
            make_dirfiles(tmp, testdir_list, testfile_list)
            listdir = os.listdir(tmp)
            for subdir in listdir:
                listfiles = os.listdir(os.path.join(tmp, subdir))
                self.assertCountEqual(listfiles, testfile_list)
            self.assertCountEqual(listdir, testdir_list)


class InventoryTests(TestCase):
    """unittests for data.inventory submodule"""

    def test_list_subdir_paths(self):
        """ensure list_subdir_paths generates an accurate path list"""
        with TemporaryDirectory() as tmp:
            make_dirfiles(tmp, testdir_list, testfile_list)
            subdir_paths = list_subdir_paths(tmp)
            self.assertIsInstance(subdir_paths, list)
            self.assertEqual(len(subdir_paths), len(testdir_list))
            for subdir in subdir_paths:
                assert os.path.exists(subdir)

    def test_list_subdirs(self):
        """ensure list_subdirs returns an accurate subdir name list"""
        with TemporaryDirectory() as tmp:
            make_dirfiles(tmp, testdir_list, testfile_list)
            subdir_list = list_subdirs(tmp)
            self.assertIsInstance(subdir_list, list)
            self.assertCountEqual(subdir_list, testdir_list)

    def test_list_files_with_extensions(self):
        """ensure list_files_with_extensions returns an accurate file list"""
        with TemporaryDirectory() as tmp:
            make_files(tmp, testfile_list)
            ext_list = ['.csv', '.txt']
            file_list = list_files_with_extensions(tmp, ext_list)
            test_ext = [
                os.path.splitext(filename)[1] for filename in file_list
            ]
            self.assertCountEqual(ext_list, test_ext)

    def test_list_datafiles(self):
        """ensure list_datafiles returns an accurate file list"""
        with TemporaryDirectory() as tmp:
            make_files(tmp, testfile_list)
            base_ext_list = ['.csv', '.xls', '.xlsx', 'sqlite3']
            add_ext_list = ['.txt']
            file_list = list_datafiles(tmp, add_ext_list)
            test_ext = [
                os.path.splitext(filename)[1] for filename in file_list
            ]
            [self.assertIn(ext, test_ext) for ext in base_ext_list[:-2]]
            self.assertIn(add_ext_list[0], test_ext)
            self.assertNotIn('.pptx', test_ext)

    def test_make_datafile_array(self):
        """ensure make_datafile_array returns an accurate array"""
        with TemporaryDirectory() as tmp:
            make_files(tmp, testfile_list)
            basename = os.path.basename(tmp)
            datafile_array = make_datafile_array(tmp)
            dir_array = datafile_array[:, 0]
            filename_array = datafile_array[:, 1]
            self.assertIsInstance(datafile_array, np.ndarray)
            self.assertEqual(len(set(dir_array)), 1)
            self.assertEqual(*list(set(dir_array)), basename)
            self.assertNotIn('.pptx', filename_array)

    def test_make_datafile_dataframe(self):
        """ensure make_datafile_dataframe returns an accurate dataframe"""
        with TemporaryDirectory() as tmp:
            make_dirfiles(tmp, testdir_list, testfile_list)
            datafile_df = make_datafile_dataframe(
                tmp,
                columns=['dir', 'file']
            )
            dirs_list = list(set(datafile_df['dir'].values))
            filename_list = list(set(datafile_df['file'].values))
            self.assertIsInstance(datafile_df, pd.DataFrame)
            self.assertCountEqual(dirs_list, testdir_list)
            self.assertNotIn('.pptx', filename_list)

    def test_make_datafile_dataframe_save(self):
        """ensure make_datafile_dataframe to_file arg saves a .csv to file"""
        with TemporaryDirectory() as tmp:
            make_dirfiles(tmp, testdir_list, testfile_list)
            fp = os.path.join(tmp, 'test_out.csv')
            datafile_df = make_datafile_dataframe(
                tmp,
                return_df=False,
                to_file=fp
            )
            self.assertIsNone(datafile_df)
            assert os.path.exists(fp)
