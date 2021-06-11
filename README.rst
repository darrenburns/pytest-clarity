=================
pytest-clarity
=================

.. image:: https://img.shields.io/pypi/v/pytest-clarity.svg
    :target: https://pypi.org/project/pytest-clarity
    :alt: PyPI version
    
.. image:: https://img.shields.io/conda/vn/conda-forge/pytest-clarity.svg
    :target: https://anaconda.org/conda-forge/pytest-clarity
    :alt: conda-forge version    

.. image:: https://img.shields.io/pypi/pyversions/pytest-clarity.svg
    :target: https://pypi.org/project/pytest-clarity
    :alt: Python versions

.. image:: https://travis-ci.org/darrenburns/pytest-clarity.svg?branch=master
    :target: https://travis-ci.org/darrenburns/pytest-clarity
    :alt: See Build Status on Travis CI

A plugin which brings the coloured diff output from the `Ward test framework <https://github.com/darrenburns/ward>`_ to pytest.

Requirements
------------

Supports Python 3.6+.

Installation
------------

You can install "pytest-clarity" via `pip`_ from `PyPI`_::

    $ pip install pytest-clarity


Usage
-----

Install the plugin as described above.

*The plugin will only be activated when the `-vv` option is supplied to `pytest`.*

You can configure the width of the output with the :code:`--diff-width` option:

::

    pytest -vv --diff-width=60


You can force `pytest-clarity` to show a symbolic diff with :code:`--diff-symbols`::

    pytest -vv --diff-symbols
