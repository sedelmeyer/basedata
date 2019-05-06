BaseData Utilities Library
=======

[![Build Status](https://travis-ci.org/sedelmeyer/basedata.svg?branch=master)](https://travis-ci.org/sedelmeyer/basedata)

## Summary
This is an installable Python utilities library containing the following modules:

1. `basedata.ops`
    - A number of classes and functions supporting the `BaseDataOps` class.
    - This class packages a number of methods focused on performing repeatable and predictable data transformations, built upon `numpy`, `pandas`, `re`, and other Python libraries.
    - See the diagram below for a high-level summary of how this module and the `BaseDataOps` class is structured.
1. `basedata.inventory`
    - **(Currently under development)** Class methods for generating data and file inventory lists and tables.
1. `basedata.log`
    - **(Not yet implemented)** Class methods for enhanced logging capabilities for recording and saving plain text data transformation log files.

This library is written using Python 3.6 and is tested against all Python versions >=3.5.

**Figure 1: Summary diagram for the BaseDataOps class**

![basedata-diagram](https://www.dropbox.com/s/cim4opz1qtdkx2j/basedata-diagram.png?raw=1)

## Installation

To install this library using `pipenv`, you can add the following to your Pipfile packages section and run `pipenv update`.

```python
...

[packages]
...
basedata = {editable = true,git = "https://github.com/sedelmeyer/basedata"}
...
```

## Documentation

The documentation for this library is still under development. Modules, functions, and classes already contained in this library all currently have extensive docstrings describing their behavior.

**The use of the `BaseDataOps` class, which is currently the most complete of all features contained in this library, follows this basic pattern...**

```python
# Import the BaseDataOps from the appropriate basedata module
from basedata.ops import BaseDataOps

# Invoke the BaseDataOps class by reading in a dataframe from file
Base = BaseDataOps.from_file("test_datafile.csv")

# Or, optionally, the class can be invoked by reading in a pandas.DataFrame
# object directly
Base =  BaseDataOps.from_object(dataframe)

# The resulting dataframe persists in the BaseDataOps class object as self.df.
# Therefore, if you'd like to access the dataframe directly...
df_copy = Base.df

# Likewise, as transformations are performed using the BaseDataOps class
# instance, those changes are performed on the self.df object directly.
Base.drop_dupes(column=column_name, index_list=list_items, validate=True)

# The modified dataframe can also be saved to .csv directly via the BaseDataOps
# class instance.
Base.to_file("target_filename.csv")
```

For more detailed review of available class methods, behaviors, and associated parameters, please see the docstrings located directly within each `basedata.ops` submodule.
