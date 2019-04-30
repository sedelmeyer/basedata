"""
This submodule, basedata.inventory, contains functions for generating
datafile inventory data for a target directory's sub-directories.
"""
import os
from glob import glob

import numpy as np
import pandas as pd


def list_subdir_paths(directory):
    """
    Generates a list of subdirectory paths

    :param directory: str pathname of target parent directory
    :return: list of paths for each subdirectory in the target parent
        directory
    """
    subdir_paths = glob("{}/*/".format(directory))
    return subdir_paths


def list_subdirs(directory):
    """
    Generates a list of subdirectory directory basenames.

    :param directory: str pathname of target parent directory
    :return: list of subdirectory basenames for each subdirectory in the
        target parent directory
    """
    subdir_paths = list_subdir_paths(directory)
    subdir_list = [os.path.basename(path[:-1]) for path in subdir_paths]
    return subdir_list


def list_files_with_extensions(directory, ext_list):
    """
    Generates a list of files in a directory that have desired extension
    types as specified.

    :param directory: str pathname of target parent directory
    :param ext_list: list of strings specifying target extension types
        e.g. ['.csv', '.xls']
    :return: list of filenames for files with matching extension type
    """
    filepath_list = sum(
        [
            glob("{0}/*{1}".format(directory, ext))
            for ext in ext_list
        ],
        [],
    )
    filenames = [os.path.basename(filepath) for filepath in filepath_list]
    return filenames


def list_datafiles(directory, add_extensions=None):
    """
    Generates a list of data-type files in a directory that have desired
    extension types as specified.

    Default extensions captured in this function are
    ['.csv', '.xls', '.xlsx', '.sqlite3']

    This list can be appended with the add_extensions parameter

    :param directory: str pathname of target parent directory
    :param add_extensions: list of strings specifying additional target
        extension types, e.g. ['.txt', '.parquet']
    :return: list of filenames for files with matching extension type
    """
    ext_types = ['.csv', '.xls', '.xlsx', 'sqlite3']
    if add_extensions:
        ext_types = ext_types + add_extensions
    filenames = list_files_with_extensions(directory, ext_types)
    return filenames


def make_datafile_array(directory, add_extensions=None):
    """
    Generates an array of datafile names in a specified directory, along with
    the basename of the directory repeated in a separate column.

    Default extensions captured in this function are
    ['.csv', '.xls', '.xlsx', '.sqlite3']

    This list of extensions can be appended with the add_extensions parameter.

    :param directory: str pathname of target parent directory
    :param add_extensions: list of strings specifying additional target
        extension types, e.g. ['.txt', '.parquet']
    :return: numpy.ndarray of filenames for files with matching extension type
        along with a column repeating the basename of the directory
    """
    if directory[-1:] == '\\' or directory[-1:] == '/':
        directory = directory[:-1]
    directory_name = os.path.basename(directory)
    datafile_list = list_datafiles(directory, add_extensions)
    filename_array = np.array(datafile_list).reshape(-1, 1)
    dirname_array = np.array(
        [directory_name] * len(filename_array)
    ).reshape(-1, 1)
    datafile_array = np.hstack([dirname_array, filename_array])
    return datafile_array


def make_datafile_dataframe(directory, columns=('directory', 'filename'),
                            add_extensions=None, return_df=True,
                            to_file=None, **kwargs):
    """
    Generates a dataframe of subdirectory names and associated datafiles
    contained in each of those subdirectories.

    Default extensions captured in this function are
    ['.csv', '.xls', '.xlsx', '.sqlite3']

    This list of extensions can be appended with the add_extensions parameter

    :param directory: str pathname of target parent directory
    :param columns: tuple specifying the name of each column,
        default=('directory', 'filename')
    :param add_extensions: list of strings specifying additional target
        extension types, e.g. ['.txt', '.parquet']
    :param return_df: bool indicates whether dataframe object is returned,
        default=True
    :param to_file: str or None indicates target filepath to which dataframe
        is saved as a .csv file. None does not save .csv. Default=None
    :param kwargs: additional named parameters for pandas.DataFrame.to_csv()
    :return: pandas.DataFrame of subdirectory names and associate datafiles
        stored in each subdirectory, returned only if return_df=True
    """
    subdir_paths = list_subdir_paths(directory)
    datafile_arrays = [
        make_datafile_array(subdir, add_extensions)
        for subdir in subdir_paths
    ]
    stacked_arrays = np.vstack(datafile_arrays)
    datafile_df = pd.DataFrame(stacked_arrays, columns=columns)
    if to_file:
        datafile_df.to_csv(to_file, index=False, **kwargs)
    if return_df:
        return datafile_df
