=================
ProdNet
=================

ProdNet is a collection of models of economic Production Networks and their associated measures and functions. It can be used to perform and compare economic shock propagation simulations.

It is currently in development and functions may be broken, change, or be deleted. Before use contact the authors.

* Free software: GNU General Public License v3


Installation
------------
Install using:

.. code-block:: python

   pip install ProdNet

Usage
-----
Currently only the Per Bak models are fully implemented.
An example of how it can be used is the following. 
For more see the example notebooks in the examples folder.

.. code-block:: python

    import numpy as np
    import matplotlib.pyplot as plt
    from ProdNet import PerBak
    from ProdNet.lib import icdf
    import time

    # Select economy depth and width, and total number of iterations
    L = 1600
    T = 1000

    # Time performance for reference
    start = time.time()

    # Initialize simulation object
    model = PerBak(L, T)

    # Compute p, probability of demand "shock"
    model.set_final_demand()

    # Simulate
    model.simulate()

    # Print elapsed time
    print(time.time() - start)  # current best=37s

    # Plot Y distribution
    Y = np.sum(model.P, axis=(1, 2))
    x, p = icdf(Y)
    plt.scatter(x, p)
    plt.yscale('log')
    plt.xscale('log')
    plt.show()


Development
-----------
Please work on a feature branch and create a pull request to the development 
branch. If necessary to merge manually do so without fast forward:

.. code-block:: bash

    git merge --no-ff myfeature

To build a development environment run:

.. code-block:: bash

    python3 -m venv env 
    source env/bin/activate 
    pip install -e '.[dev]'

For testing:

.. code-block:: bash

    pytest --cov

Credits
-------
This is a project by `Leonardo Niccolò Ialongo <https://datasciencephd.eu/students/leonardo-niccol%C3%B2-ialongo/>`_ and `Davide Luzzati <https://www.santannapisa.it/it/davide-samuele-luzzati>`_, under 
the supervision of `Diego Garlaschelli <https://networks.imtlucca.it/members/diego>`_ and `Giorgio Fagiolo <https://www.santannapisa.it/en/giorgio-fagiolo>`_ .

