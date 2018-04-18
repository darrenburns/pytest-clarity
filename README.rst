=================
pytest-betterdiff
=================

.. image:: https://img.shields.io/pypi/v/pytest-betterdiff.svg
    :target: https://pypi.org/project/pytest-betterdiff
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-betterdiff.svg
    :target: https://pypi.org/project/pytest-betterdiff
    :alt: Python versions

.. image:: https://travis-ci.org/darrenburns/pytest-betterdiff.svg?branch=master
    :target: https://travis-ci.org/darrenburns/pytest-betterdiff
    :alt: See Build Status on Travis CI


A plugin providing an alternative, colourful, ExUnit inspired diff output for failing assertions.

Features
--------

* Enables an easier to parse and more understandable diff for your failing tests.
* Adds hints to the output for failing tests to help you track down common issues.

.. image:: https://raw.githubusercontent.com/darrenburns/pytest-betterdiff/master/sample_image.png
    :alt: Example output with betterdiff

Requirements
------------

Supports Python 2.7.X, 3.4, 3.5, and 3.6. Untested on newer versions.


Installation
------------

You can install "pytest-betterdiff" via `pip`_ from `PyPI`_::

    $ pip install pytest-betterdiff


Usage
-----

Install the plugin as described above, and it will automatically enabled.

You may need to use the :code:`-vv` pytest flag to display the full output in larger diffs:

.. code-block::python
    pytest -vv

You can disable hints using the :code:`--no-hints` flag:

.. code-block::python
    pytest -vv --no-hints


Contributing
------------
Contributions are very welcome. Tests can be run with `tox`_, please ensure
the coverage at least stays the same before you submit a pull request.

License
-------

Distributed under the terms of the `MIT`_ license, "pytest-betterdiff" is free and open source software


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
.. _`file an issue`: https://github.com/darrenburns/pytest-betterdiff/issues
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`tox`: https://tox.readthedocs.io/en/latest/
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
