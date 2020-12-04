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
    # data = data.loc[data['scenario'] == 'Baseline']
    data['pop_density_km2'] = round(data['pop_density_km2'])
    n = len(regions)

    data = data[['GID_id', 'pop_density_km2']]
    regions = regions[['GID_id', 'geometry']]#[:1000]

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
        '>45 $\mathregular{km^2}$']

    regions['bin'] = pd.cut(
        regions[metric],
        bins=bins,
        labels=labels
    )#.fillna('<20')

    fig, ax = plt.subplots(1, 1, figsize=(15, 10))

    minx, miny, maxx, maxy = regions.total_bounds
    ax.set_xlim(minx+7, maxx+2)
    ax.set_ylim(miny-5, maxy)

    regions.plot(column='bin', ax=ax, cmap='inferno_r',
    linewidth=0, legend=True, edgecolor='grey')

    # handles, labels = ax.get_legend_handles_labels()

    # fig.legend(handles, labels)
    # fig.legend(handles=handles[::-1], labels=labels[::-1], title='Population Density (km^2)',
    #     loc='lower left')

    ctx.add_basemap(ax, crs=regions.crs, source=ctx.providers.CartoDB.Voyager)

    fig.suptitle('Population Density Deciles for Sub-National Regions (n={})'.format(n))

    fig.tight_layout()
    fig.savefig(os.path.join(VIS, 'region_by_pop_density.png'))

    plt.close(fig)


def plot_sub_national_cost_per_square_km(data, regions):
    """
    """
    n = len(regions)
    data = data.loc[data['scenario'] == 'Baseline']
    data = data.loc[data['strategy'] == '4G(MW)']
    data = data.loc[data['confidence'] == 50]

    data['cost_per_km2'] = (data['total_cost'] / data['area_km2']) / 1e3
    data = data[['GID_id', 'cost_per_km2']]
    regions = regions[['GID_id', 'geometry']]#[:1000]

    regions = regions.merge(data, left_on='GID_id', right_on='GID_id')
    regions.reset_index(drop=True, inplace=True)

    metric = 'cost_per_km2'

    # bins = [-1, 2.5, 5, 7.5, 10, 12.5, 15, 17.5, 20, 22.5, 25, 1e9]
    bins = [-1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1e9]
    labels = [
        '<1k USD $\mathregular{km^2}$',
        '1-2k USD $\mathregular{km^2}$',
        '2-3k USD $\mathregular{km^2}$',
        '3-4k USD $\mathregular{km^2}$',
        '4-5k USD $\mathregular{km^2}$',
        '5-6k USD $\mathregular{km^2}$',
        '6-7k USD $\mathregular{km^2}$',
        '7-8k USD $\mathregular{km^2}$',
        '8-9k USD $\mathregular{km^2}$',
        '9-10k USD $\mathregular{km^2}$',
        '>10k USD $\mathregular{km^2}$',
    ]
    regions['bin'] = pd.cut(
        regions[metric],
        bins=bins,
        labels=labels
    )#.fillna('<20')

    fig, ax = plt.subplots(1, 1, figsize=(10,10))

    minx, miny, maxx, maxy = regions.total_bounds
    ax.set_xlim(minx+7, maxx-12)
    ax.set_ylim(miny+5, maxy)

    regions.plot(column='bin', ax=ax, cmap='inferno_r', linewidth=0.2, legend=True, edgecolor='grey')

    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles[::-1], labels[::-1]) #, title='Population Density (km^2)'

    #we probably need to fine tune the zoom level to bump up the resolution of the tiles
    ctx.add_basemap(ax, crs=regions.crs, source=ctx.providers.CartoDB.Voyager)

    # plt.subplots_adjust(top=1.5)
    fig.suptitle(
        'Square Kilometer Cost for 4G Universal Broadband using Wireless Backhaul (n={})'.format(n)) # fontsize=12

    fig.tight_layout()
    fig.savefig(os.path.join(VIS, 'sub_national_cost_per_square_km.png'))
    # fig.savefig(os.path.join(VIS, 'region_by_total_cost.pdf'))
    plt.close(fig)


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

    print('Plotting regions by geotype')
    plot_regions_by_geotype(data, shapes)

    # print('Loading regional results data')
    # path = os.path.join(BASE_PATH, '..', 'results', 'regional_cost_estimates.csv')
    # regional_costs = pd.read_csv(path)

    # print('Plotting sub-national regions by cost per km^2')
    # plot_sub_national_cost_per_square_km(regional_costs, shapes)

    print('Complete')
