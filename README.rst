========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis|
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/basedata/badge/?style=flat
    :target: https://readthedocs.org/projects/basedata
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/sedelmeyer/basedata.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/sedelmeyer/basedata

.. |version| image:: https://img.shields.io/pypi/v/basedata.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/basedata

.. |commits-since| image:: https://img.shields.io/github/commits-since/sedelmeyer/basedata/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/sedelmeyer/basedata/compare/v0.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/basedata.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/basedata

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/basedata.svg
    :alt: Supported versions
    :target: https://pypi.org/project/basedata

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/basedata.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/basedata


.. end-badges

A python utilities library for base data operations.

* Free software: MIT license

Installation
============

::

    pip install basedata

Documentation
=============


https://basedata.readthedocs.io/


Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
