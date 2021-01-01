Global Satellite Assessment Tool (globalsat)
=========

[![Build Status](https://travis-ci.com/edwardoughton/globalsat.svg?branch=master)](https://travis-ci.com/edwardoughton/globalsat)
[![Coverage Status](https://coveralls.io/repos/github/edwardoughton/globalsat/badge.svg?branch=master)](https://coveralls.io/github/edwardoughton/globalsat?branch=master)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Description
===========

Human activity is increasibly reliant on satellite connectivity services for broadband
internet access, timing, syncronization, positioning etc.

However, we lack analytics to help model global satellite systems, whether we wish to
understand capacity, coverage, cost, vulnerability or resilience.

This codebase provides an open-source model to help analyze the global satellite fleet.
Such a model can be used for numerous applications, including assessment of digital
connectivity or understanding the vulnerability and resilience of the global satellite fleet.


Using conda
===========

The recommended installation method is to use conda, which handles packages and virtual
environments, along with the conda-forge channel which has a host of pre-built libraries and
packages.

Create a conda environment called globalsat:

    conda create --name globalsat python=3.7 gdal

Activate it (run this each time you switch projects):

    conda activate globalsat

First, to run the just simulation (`sim.py`) you need to install necessary packages:

    conda install numpy pandas

Secondly, to run the preprocessing (`preprocess.py`) and get_results (`results.py`):

    conda install geopandas rasterio rasterstats tqdm

Finally, to visualize the results (`vis.py`) you will need:

    conda install matplotlib seaborn contextily descartes


Quick Start
===========

To quick start, install the `globalsat` package:

    python setup.py install

Or if you want to develop the package:

    python setup.py develop

Then run the simulation to generate results:

    python scripts/run.py

If you want to create the map try:

    python scripts/preprocess.py

Followed by:

    python scripts/results.py

And then:

    python vis/vis.py


Background and funding
======================

**globalsat** has been developed by researchers at George Mason University.


Contributors
============
- Bonface Osoro (George Mason University) (Engineering Lead)
- Ed Oughton (George Mason University) (Project lead)


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
