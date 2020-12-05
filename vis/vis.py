"""
Visualize results.

"""
import os
import configparser
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import contextily as ctx

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')
RESULTS = os.path.join(BASE_PATH, '..', 'results')
VIS = os.path.join(BASE_PATH, '..', 'vis', 'figures')


def get_regional_shapes():
    """
    """
    output = []

    for item in os.listdir(DATA_INTERMEDIATE):#[:2]:
        if len(item) == 3: # we only want iso3 code named folders

            filename_gid1 = 'regions_1_{}.shp'.format(item)
            path_gid1 = os.path.join(DATA_INTERMEDIATE, item, 'regions', filename_gid1)

            filename_gid2 = 'regions_2_{}.shp'.format(item)
            path_gid2 = os.path.join(DATA_INTERMEDIATE, item, 'regions', filename_gid2)

            if os.path.exists(path_gid2):
                data = gpd.read_file(path_gid2)
                data['GID_id'] = data['GID_2']
                data = data.to_dict('records')
            elif os.path.exists(path_gid1):
                data = gpd.read_file(path_gid1)
                data['GID_id'] = data['GID_1']
                data = data.to_dict('records')
            else:
               print('No shapefiles for {}'.format(item))
               continue

            for datum in data:
                output.append({
                    'geometry': datum['geometry'],
                    'properties': {
                        'GID_id': datum['GID_id'],
                    },
                })

    output = gpd.GeoDataFrame.from_features(output, crs='epsg:4326')

    return output


def plot_regions_by_geotype(data, regions):
    """
    """
    data = data.loc[data['scenario'] == 'baseline']
    data = data.loc[data['constellation'] == 'Starlink']
    data['pop_density_km2'] = round(data['pop_density_km2'])
    n = len(regions)

    data = data[['GID_id', 'pop_density_km2']]
    regions = regions[['GID_id', 'geometry']]

    regions = regions.merge(data, left_on='GID_id', right_on='GID_id')
    regions.reset_index(drop=True, inplace=True)

    metric = 'pop_density_km2'

    bins = [-1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 111607]
    labels = [
        '<5 $\mathregular{km^2}$',
        '5-10 $\mathregular{km^2}$',
        '10-15 $\mathregular{km^2}$',
        '15-20 $\mathregular{km^2}$',
        '20-25 $\mathregular{km^2}$',
        '25-30 $\mathregular{km^2}$',
        '30-35 $\mathregular{km^2}$',
        '35-40 $\mathregular{km^2}$',
        '40-45 $\mathregular{km^2}$',
        '>45 $\mathregular{km^2}$'
    ]

    regions['bin'] = pd.cut(
        regions[metric],
        bins=bins,
        labels=labels
    )

    fig, ax = plt.subplots(1, 1, figsize=(15, 6))

    minx, miny, maxx, maxy = regions.total_bounds
    ax.set_xlim(minx+10, maxx)
    ax.set_ylim(miny-5, maxy)

    regions.plot(column='bin', ax=ax, cmap='inferno_r',
    linewidth=0, legend=True, edgecolor='grey')

    ctx.add_basemap(ax, crs=regions.crs, source=ctx.providers.CartoDB.Voyager)

    fig.suptitle('Population Density by Sub-National Region (n={})'.format(n))

    fig.tight_layout()
    fig.savefig(os.path.join(VIS, 'region_by_pop_density.png'))

    plt.close(fig)


def plot_capacity_per_user(data, regions):
    """

    """
    n = len(regions)
    data = data.loc[data['scenario'] == 'baseline']

    regions = regions[['GID_id', 'geometry']]#[:1000]

    constellations = data['constellation'].unique()#[:1]

    fig, axs = plt.subplots(3, 1, figsize=(10, 12)) #width height

    i = 0

    for constellation in list(constellations):

        subset = data.loc[data['constellation'] == constellation]

        subset = subset[['GID_id', 'per_user_capacity']]

        regions_merged = regions.merge(subset, left_on='GID_id', right_on='GID_id')
        regions_merged.reset_index(drop=True, inplace=True)

        metric = 'per_user_capacity'

        bins = [-1, 5, 10, 25, 50, 100, 150, 200, 250, 300, 1e9]
        labels = [
            '<5 Mbps',
            '5-10 Mbps',
            '10-25 Mbps',
            '25-50 Mbps',
            '50-100 Mbps',
            '100-150 Mbps',
            '150-200 Mbps',
            '200-250 Mbps',
            '250-300 Mbps',
            '>300 Mbps',
        ]
        regions_merged['bin'] = pd.cut(
            regions_merged[metric],
            bins=bins,
            labels=labels
        )#.fillna('<20')

        minx, miny, maxx, maxy = regions_merged.total_bounds
        axs[i].set_xlim(minx, maxx)
        axs[i].set_ylim(miny, maxy)

        regions_merged.plot(column='bin', ax=axs[i], cmap='inferno_r', linewidth=0, legend=True)

        ctx.add_basemap(axs[i], crs=regions_merged.crs, source=ctx.providers.CartoDB.Voyager)

        letter = get_letter(constellation)

        axs[i].set_title("({}) {} Per User Capacity Based on 10 Percent Adoption (n={})".format(
            letter, constellation, n))

        i += 1

    fig.tight_layout()
    fig.savefig(os.path.join(VIS, 'per_user_capacity_panel.png'))

    plt.close(fig)


def get_letter(constellation):
    """
    Return the correct letter.

    """
    if constellation == 'Starlink':
        return 'A'
    elif constellation == 'OneWeb':
        return 'B'
    elif constellation == 'Telesat':
        return 'C'
    else:
        print('Did not recognize constellation')


if __name__ == '__main__':

    if not os.path.exists(VIS):
        os.makedirs(VIS)

    print('Loading regional data by pop density geotype')
    path = os.path.join(RESULTS, 'results.csv')
    data = pd.read_csv(path)#[:1000]

    print('Loading shapes')
    path = os.path.join(DATA_INTERMEDIATE, 'all_regional_shapes.shp')
    if not os.path.exists(path):
        shapes = get_regional_shapes()
        shapes.to_file(path)
    else:
        shapes = gpd.read_file(path, crs='epsg:4326')#[:1000]

    print('Plotting population density per area')
    plot_regions_by_geotype(data, shapes)

    print('Plotting capacity per user')
    plot_capacity_per_user(data, shapes)

    print('Complete')
