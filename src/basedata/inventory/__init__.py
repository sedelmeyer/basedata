import os
from glob import glob

import numpy as np
import pandas as pd


def list_subdir_paths(directory):
    """"""
    subdir_paths = glob("{}/*/".format(directory))
    return subdir_paths


def list_subdirs(directory):
    """"""
    subdir_paths = list_subdir_paths(directory)
    subdir_list = [os.path.basename(path[:-1]) for path in subdir_paths]
    return subdir_list


def list_files_with_extensions(directory, ext_list):
    """"""
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
    """"""
    ext_types = ['.csv', '.xls', '.xlsx', 'sqlite3']
    if add_extensions:
        ext_types = ext_types + add_extensions
    filenames = list_files_with_extensions(directory, ext_types)
    return filenames


def make_datafile_array(directory, add_extensions=None):
    """"""
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
    """"""
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
