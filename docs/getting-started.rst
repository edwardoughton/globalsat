===============
Getting Started
===============

This tutorial provides explanation for the ``globalsat`` codebase which includes:

1) A fully-tested simulation model to assess the techno-economics of satellite constellations.
2) A processing script for obtaining population metrics from a global settlement layer.
3) A script to gather simulation outputs and prepare the data for visualization.
4) A visualization script which can create global maps for satellite broadband metrics.

Each will be discussed in detail in this documentation.

Simulation model
----------------

The simulation model develops a set of Monte Carlo results based on a stochastic geometry
method for assessing the capacity of a wireless network.

After creating the virtual environment, the package needs to be installed as follows:

.. code-block:: python

    python setup.py install

Or if you want to develop the packages, like this:

.. code-block:: python

    python setup.py develop

To change any model parameters you will need to access `inputs.py`, and then run the model:

.. code-block:: python

    python scripts/run.py

The simulation outputs will be written out into the `results` directory.


Processing
----------

The preprocessing script uses a global settlement layer and global administrative boundaries
to extract population metrics.

First you need to download the required data layers including:

- A global settlement layer from WorldPop (https://www.worldpop.org/)
- Global administrative boundaries from GADM (https://gadm.org/)

You can either create the same folder structure as is already in the code (`data/raw`), or
adjust the input file paths to reflect your desired directory structure.

Then to run this code use the following:

.. code-block:: python

    python scripts/results.py


Results gathering
-----------------

The results script gathers the outputs from the simulation, combines them with any scenario
data and then exports the dataset ready for visualization. You can run this code like this:

.. code-block:: python

    python scripts/results.py


Visualization
-------------

The visualization code loads the results data and creates global maps for each of the
constellations modeled. To create the maps use:

.. code-block:: python

    python vis/vis.py

The script exports the images to a `figures` folder within the `vis` directory.
