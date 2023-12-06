Installation
============

If graph visualization is not required then install via `pip`:

.. code:: shell

   pip install ananke-causal

Alternatively, the package may be installed from gitlab by cloning and `cd` into the directory. Then, `poetry <https://python-poetry.org>`_ can be used to install:

.. code:: shell

    poetry install

Install with graph visualization
################################


If graphing support is required, it is necessary to install `graphviz <https://www.graphviz.org/download/>`_.


Non M1 Mac instructions
***********************
Ubuntu:

.. code:: shell

   sudo apt install graphviz libgraphviz-dev pkg-config

Mac `Homebrew <https://brew.sh/>`_:

.. code:: shell

   brew install graphviz

Fedora:

.. code:: shell

   sudo yum install graphviz

Once graphviz has been installed, then:

.. code:: shell

    pip install ananke-causal[viz] # if pip is preferred
    poetry install --extras viz # if poetry is preferred

M1 Mac specific instructions
############################

If on M1 see this `issue <https://github.com/pygraphviz/pygraphviz/issues/398>`_. The fix is to run the following before installing:

.. code:: shell

   brew install graphviz
   python -m pip install \
       --global-option=build_ext \
       --global-option="-I$(brew --prefix graphviz)/include/" \
       --global-option="-L$(brew --prefix graphviz)/lib/" \
       pygraphviz

Install `graphviz <https://www.graphviz.org/download/>`_ using the appropriate method for your OS
    
.. code:: shell

    # Ubuntu

    sudo apt install graphviz libgraphviz-dev pkg-config

    # Mac

    brew install graphviz

    # Mac (M1)
    ## see https://github.com/pygraphviz/pygraphviz/issues/398
    
    brew install graphviz
    python -m pip install \
        --global-option=build_ext \
        --global-option="-I$(brew --prefix graphviz)/include/" \
        --global-option="-L$(brew --prefix graphviz)/lib/" \
        pygraphviz

    # Fedora

    sudo yum install graphviz

Install the latest `release <https://pypi.org/project/ananke-causal/>`__ using pip.

.. code:: shell

    pip3 install ananke-causal

For more details please see the `gitlab <https://gitlab.com/causal/ananke>`_, or the `documentation <https://ananke.readthedocs.io>`_ for details on how to use Ananke.
