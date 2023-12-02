Installation
============

Quick guide to installing ``pe-configurator``.

.. _install:

Installing pe-configurator
--------------------------
The easiest way to install ``pe-configurator`` is from ``pypi``:

.. code:: console

    pip install pe-configurator

It can also be installed from ``conda-forge``:

.. code:: console

    conda install -c conda-forge pe-configurator

Installing pe-configurator from source
---------------------------------------
We highly recommend creating an isolated environment with ``conda`` or ``mamba``.
A minimal environment can be created with:

.. code:: console

    conda install -c conda-forge mamba
    conda create -n configurator-env python=3.10
    conda activate configurator-env

Clone the ``pe-configurator`` repository and run

.. code-block:: console

    pip install .


.. tip::

    If you are actively developing the code, consider using ``pip install -e .`` to
    avoid having to reinstall after ever change to the code.



Installing optional dependencies to build documentation
-------------------------------------------------------

To build documentation, install the relevant dependencies with

.. code-block:: console

    pip install .[docs]

Then the documentation can be built via

.. code-block:: console

    cd docs
    make html
