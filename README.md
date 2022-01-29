# Global Satellite Assessment Tool (globalsat)

[![Build Status](https://travis-ci.com/edwardoughton/globalsat.svg?branch=master)](https://travis-ci.com/edwardoughton/globalsat)
[![Documentation Status](https://readthedocs.org/projects/globalsat/badge/?version=latest)](https://globalsat.readthedocs.io/en/latest/?badge=latest)
[![Coverage Status](https://coveralls.io/repos/github/edwardoughton/globalsat/badge.svg?branch=master)](https://coveralls.io/github/edwardoughton/globalsat?branch=master)

There is considerable hype around the potential for Low Earth Orbit (LEO) satellite broadband
constellations to provide connectivity to the billions of unconnected users globally.

But how true is this? How much capacity could one of the new LEO constellations provide to
users? How will this approach compare to terrestrial methods?

Given we still lack analytics to help model the engineering-economics of new global satellite
constellations, this `globalsat` repository provides code to help model capacity, coverage
and cost.

Citation
---------

- Osoro, O.B., Oughton, E.J., 2021. A Techno-Economic Framework for Satellite Networks Applied to Low Earth Orbit Constellations: Assessing Starlink, OneWeb and Kuiper. IEEE Access 9, 141611–141625. [https://doi.org/10.1109/ACCESS.2021.3119634](https://doi.org/10.1109/ACCESS.2021.3119634)

Example Method
==============

The method is based on a stochastic engineering simulation model which estimates the radio
link budget, and then provides capacity estimates after accounting for propagation losses. A
demand module provides  estimates for various adoption scenarios, including how much busy hour
traffic is likely to be created in a local statistical area. Additionally, a cost module
brings together the capital and operational expenses for the total cost of ownership of each
constellation. Finally, an assessment process is undertaken which links together the provided
capacity to each active user, as well as the cost implications. Figure 1 illustrates this
method.

## Figure 1 Techno-economic method for satellite broadband assessment
<p align="center">
  <img src="/figures/Box_model.jpg" />
</p>

Example Results
==============

Rather than estimating only aggregated network capacity results, the purpose of the
`globalsat` repository (as reported in the affiliated paper) is to provide insight on the potential
Quality of Service which a user may experience on the ground. Example scenarios are applied
in the modeling process, and results for the estimated capacity are visualized in Figure 2.

## Figure 2 Estimated per user capacity in the busy hour for three LEO constellations
<p align="center">
  <img src="/figures/per_user_capacity_panel.png" />
</p>

Required data
==============

To use `globalsat` various input datasets need to be downloaded from their source.

Firstly, download the Global Administrative Database (GADM), following the link below and
making sure you download the "six separate layers.":

- https://gadm.org/download_world.html

Place the data into the following path `data/raw/gadm36_levels_shp`.

Then download the WorldPop global settlement data from:

- https://www.worldpop.org/geodata/summary?id=24777.

Place the data (e.g. 'ppp_2020_1km_Aggregated.tiff') into `data/raw/settlement_layer`.

Now you should be ready to start running the codebase.

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
- Osoro Ogutu Bonface (George Mason University) (Engineering Lead)
- Ed Oughton (George Mason University) (Project lead)
