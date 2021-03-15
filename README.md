# Global Satellite Assessment Tool (globalsat)

[![Build Status](https://travis-ci.com/edwardoughton/globalsat.svg?branch=master)](https://travis-ci.com/edwardoughton/globalsat)
[![Documentation Status](https://readthedocs.org/projects/globalsat/badge/?version=latest)](https://globalsat.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/edwardoughton/globalsat/badge.svg?branch=master)](https://coveralls.io/github/edwardoughton/globalsat?branch=master)


Human activity is increasibly reliant on satellite broadband connectivity for internet access,
timing, syncronization, positioning etc.

However, we lack analytics to help model the engineering-economics of new global satellite
constellations, in order to understand capacity, coverage and cost.

This codebase provides an open-source model to help analyze the global satellite fleet. Such
a model can be used for numerous applications, such as assessing the role of new Low Earth
Orbit constellations in delivering universal broadband services.


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

    python vis/vis.py


Background and funding
======================

**globalsat** has been developed by researchers at George Mason University.


Contributors
============
- Bonface Osoro (George Mason University) (Engineering Lead)
- Ed Oughton (George Mason University) (Project lead)
