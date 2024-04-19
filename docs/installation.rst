.. _installation:

************
Installation
************

Note that EPyT-Flow supports Python 3.9 - 3.12

.. note::

    EPyT-Flow compiles EPANET and EPANET-MSX libraries (and uses those instead of the pre-compiled
    libraries that are shipped with EPyT) if it is installed on a Linux system and if
    build tools (i.e. *build-essentials* package) are available.

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
