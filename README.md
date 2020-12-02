# globalsat
Global Satellite Fleet Model

Human activity is increasibly reliant on satellite connectivity services for broadband
internet access, timing, syncronization, positioning etc.

However, we lack analytics to help model global satellite systems, whether we wish to
understand capacity, coverage, cost, vulnerability or resilience.

This codebase provides an open-source model to help analyze the global satellite fleet.
Such a model can be used for numerous applications, including assessment of digital
connectivity or understanding the vulnerability and resilience of the global satellite fleet.

Using conda
==========

The recommended installation method is to use conda, which handles packages and virtual
environments, along with the conda-forge channel which has a host of pre-built libraries and
packages.

Create a conda environment called globalsat:

    conda create --name globalsat python=3.7 gdal

Activate it (run this each time you switch projects):

    conda activate globalsat

First, install optional packages:

    conda install geopandas rasterio rasterstats


Background and funding
======================

**globalsat** is being collaboratively developed by researchers at George Mason University, as
well as colleagues at the British Antartic Survey and University of Cambridge.


Contributors
============
- Edward J. Oughton (George Mason University/Oxford)
- Bonface Osaro (George Mason University)
- Daikichi Seki (Cambridge/Kyoto University)
- Richard Horne (British Antartic Survey)
