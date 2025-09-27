.. _installation:

************
Installation
************

Note that EPyT-Flow supports Python 3.9 - 3.13

.. note::

    EPyT-Flow builds upon `EPANET-PLUS <https://github.com/WaterFutures/EPANET-PLUS>`_ which
    constitutes a C extension and Python package.
    In the rare case that the pre-build package of EPANET-PLUS does not work on your system,
    you have to build and install it manually -- please follow the instructions provided
    `here <https://epanet-plus.readthedocs.io/en/stable/installation.html>`_.

PyPI
----

.. code:: bash

    pip install epyt-flow


Git
---

Download or clone the repository:

.. code:: bash

    git clone https://github.com/WaterFutures/EPyT-Flow.git
    cd EPyT-Flow

Install all requirements as listed in `REQUIREMENTS.txt <https://raw.githubusercontent.com/WaterFutures/EPyT-Flow/master/REQUIREMENTS.txt>`_:

.. code:: bash

    pip install -r REQUIREMENTS.txt


Install the toolbox:

.. code:: bash

    pip install .
