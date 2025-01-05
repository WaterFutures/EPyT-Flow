.. _installation:

************
Installation
************

Note that EPyT-Flow supports Python 3.9 - 3.13

.. note::

    EPyT-Flow compiles EPANET and EPANET-MSX libraries (and uses those instead of the pre-compiled
    libraries that are shipped with EPyT) if it is installed on a Unix system and if
    the *gcc* compiler is available -- i.e. Linux user can simply install the
    *build-essentials* package.

    **Attention macOS users:** The "true" *gcc* compiler (version 12) is needed which is not the
    *clang* compiler that is shipped with Xcode and is linked to gcc!
    The correct version of the "true" *gcc* can be installed via `brew <https://brew.sh/>`_:
    
    .. code:: bash

        brew install gcc@12

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
