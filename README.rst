=================
pytest-clarity
=================

.. image:: https://img.shields.io/pypi/v/pytest-clarity.svg
    :target: https://pypi.org/project/pytest-clarity
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-clarity.svg
    :target: https://pypi.org/project/pytest-clarity
    :alt: Python versions

.. image:: https://travis-ci.org/darrenburns/pytest-clarity.svg?branch=master
    :target: https://travis-ci.org/darrenburns/pytest-clarity
    :alt: See Build Status on Travis CI

A plugin to improve the readability of pytest output.

Features
--------

* Enables an easier to parse and more understandable diff for your failing tests.
* Adds hints to the output for failing tests to help you track down common issues.

.. image:: https://raw.githubusercontent.com/darrenburns/pytest-clarity/master/sample_image.png
    :alt: Example output with clarity

Requirements
------------

Supports Python 2.7 and 3.4+


Installation
------------

You can install "pytest-clarity" via `pip`_ from `PyPI`_::

    $ pip install pytest-clarity


Usage
-----

Install the plugin as described above, and it will automatically enabled.

You may need to use the :code:`-vv` pytest flag to display the full output in larger diffs:

::

    pytest -vv

You can disable hints using the :code:`--no-hints` flag:

::

    pytest -vv --no-hints

You can configure the width of the output with the :code:`--diff-width` option:

::

    pytest -vv --diff-width=60


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-clarity" is free and open source software


Issues
------

If you encounter any problems, please `file an issue`_ along with a detailed description.

This `pytest`_ plugin was generated with `Cookiecutter`_ along with `@hackebrot`_'s `cookiecutter-pytest-plugin`_ template.


.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`@hackebrot`: https://github.com/hackebrot
.. _`MIT`: http://opensource.org/licenses/MIT
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`GNU GPL v3.0`: http://www.gnu.org/licenses/gpl-3.0.txt
.. _`Apache Software License 2.0`: http://www.apache.org/licenses/LICENSE-2.0
.. _`cookiecutter-pytest-plugin`: https://github.com/pytest-dev/cookiecutter-pytest-plugin
.. _`file an issue`: https://github.com/darrenburns/pytest-clarity/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
