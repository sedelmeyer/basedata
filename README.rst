BaseData Utilities Python Library
=================================

This is a utilities library for Python-based data analysis, in which I attempt to encapsulate repeatable data cleansing workflows within a number of classes, methods, and helper functions focused on performing repeatable and predictable data transformations.

.. image:: https://travis-ci.org/sedelmeyer/basedata.svg?branch=master
    :target: https://travis-ci.org/sedelmeyer/basedata

* **GitHub repo:** https://github.com/sedelmeyer/basedata
* **Documentation:** https://sedelmeyer.github.io/basedata

.. contents:: Contents
  :local:
  :depth: 1
  :backlinks: none

Summary
-------

This is an installable Python utilities library containing the following modules:

1. `basedata.ops <https://github.com/sedelmeyer/basedata/tree/develop/src/basedata/ops>`_
    - A number of classes and functions supporting the ``BaseDataOps`` class.
    - This class packages a number of methods focused on performing repeatable and predictable data transformations, built upon ``numpy``, ``pandas``, ``re``, and other Python libraries.
    - See the diagram below for a high-level summary of how this module and the ``BaseDataOps`` class is structured.
2. `basedata.inventory <https://github.com/sedelmeyer/basedata/tree/develop/src/basedata/inventory>`_
    - **(Currently under development)** Class methods for generating data and file inventory lists and tables.
3. basedata.log
    - **(Not yet implemented)** Class methods for enhanced logging capabilities for recording and saving plain text data transformation log files.

This library is written using Python 3.6 and is tested against all Python versions >=3.5.

Design
------

**Figure 1: Summary diagram for the BaseDataOps class**

.. image:: https://raw.githubusercontent.com/sedelmeyer/basedata/master/docs/_static/basedata-diagram.png

Installation
------------

If you are using Pipenv_ to manage your dependencies and virtual environments, you can add the following to your Pipfile packages section (you can decide whether you want the package to be ``editable`` or not) and run ``pipenv update``::

    ...

    [packages]
    ...
    basedata = {editable = true,git = "https://github.com/sedelmeyer/basedata"}
    ...

If you are using pure pip_ for installing the library, the equivalent command to what I have shown above is::

    pip install -e git+https://github.com/sedelmeyer/basedata

If you are using conda_ environments you can likewise invoke ``pip`` from within your virtual environment to install directly from the GitHub repo. This can be accomplished either (a) directly from the command line after activating your environment, or (b) as a dependency specified in your conda ``environment.yml`` file as shown below::

    name: ...
    channels: ...
    dependencies:
        - ...
        - pip
        - pip:
            - -e git+https://github.com/sedelmeyer/basedata
            - ...


Basic Usage
-----------

The documentation for this library is still under development. Modules, functions, and classes already contained in this library all currently have extensive docstrings describing their behavior. Those docstrings can be easily viewed within `the documentation <https://sedelmeyer.github.io/basedata/modules.html>`_.

**The use of the** ``BaseDataOps`` **class, which is currently the most complete of all features contained in this library, follows this basic pattern...**

.. code:: python

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


For more detailed review of available class methods, behaviors, and associated parameters, please see the docstrings and source code located within the `src/basedata <https://github.com/sedelmeyer/basedata/tree/develop/src/basedata>`_ directory.


.. _Pipenv: https://pipenv.readthedocs.io/en/latest/
.. _pip: https://pip.pypa.io/en/stable/
.. _conda: https://docs.conda.io/en/latest/
