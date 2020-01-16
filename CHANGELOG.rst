
Changelog
=========

Future releases
---------------

.. todo::

    * Remove uneeded files from project

0.6.4 (2020-01-...
------------------

* Update ``CHANGELOG.rst`` to reflect project version history.
* ...

0.6.3 (2020-01-15)
------------------

* Add initial sphinx documentation to project.

0.6.2 (2020-01-15)
------------------

* Move tests out of ``src/basedata`` package directoy and into ``tests`` directory.
* Fix data types for failing unit tests.
* Update ``setup.cfg`` ``addopts`` to fix TravisCI ``tox`` error.

0.6.1 (2019-05-06)
------------------

* Added initial ``README.md``.

0.6.0 (2019-04-29)
------------------

* Added ``apply_function`` and ``add_column`` methods to ``ColumnConversionsMixin`` class.

0.5.0 (2019-04-29)
------------------

* Added ``basedata.inventory`` submodule with datafile inventory functions.

0.4.0 (2019-04-29)
------------------

* Added ``basedata.ops.cols`` submodule with ``ColumnConversionsMixin``.

0.3.0 (2019-04-29)
------------------

* Added ``basedata.ops.ids`` submodule with ``DedupeMixin`` and ``ValidIDsMixin`` classes.

0.2.0 (2019-04-29)
------------------

* Added ``basedata.ops.base`` submodule with ``BaseDataOps`` class.

0.1.0 (2019-04-29)
------------------

* Generated base library template (with a modified version of the `cookiecutter-pylibrary`_ template) and installed Pipenv virtual environment dependencies.

.. _cookiecutter-pylibrary: https://github.com/ionelmc/cookiecutter-pylibrary
