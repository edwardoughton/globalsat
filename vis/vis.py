"""
Visualize results.

Written by Ed Oughton

December 2020.

"""
import os
import sys
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

ROOT_DIR = os.path.normpath(os.path.join(os.path.abspath(__file__), '..', '..', 'scripts'))
sys.path.insert(0, ROOT_DIR)

from inputs import parameters


def plot_aggregated_engineering_metrics(data):
    """
    Create 2D engineering plots for system capacity model.

    """

    data.columns = [
        'Constellation', 'Number of Satellites','Asset Distance',
        'Coverage Area', 'Iteration', 'Free Space Path Loss',
        'Random Variation', 'Antenna Gain', 'EIRP',
        'Received Power', 'Noise', 'Carrier-to-Noise-Ratio',
        'Spectral Efficiency', 'Channel Capacity',
        'Aggregate Channel Capacity', 'Area Capacity'
    ]

    data['Channel Capacity'] = round(data['Channel Capacity'] / 1e3,2)
    data['Aggregate Channel Capacity'] = round(data['Aggregate Channel Capacity'] / 1e3)

    data = data[[
        'Constellation',
        'Number of Satellites',
        'Free Space Path Loss',
        'Received Power',
        'Carrier-to-Noise-Ratio',
        'Spectral Efficiency',
        'Channel Capacity',
        'Aggregate Channel Capacity',
    ]].reset_index()

    data['Constellation'] = data['Constellation'].replace(regex='starlink', value='Starlink')
    data['Constellation'] = data['Constellation'].replace(regex='oneweb', value='OneWeb')
    data['Constellation'] = data['Constellation'].replace(regex='kuiper', value='Kuiper')

    long_data = pd.melt(data,
        id_vars=[
            'Constellation', 'Number of Satellites'
        ],
        value_vars=[
            'Free Space Path Loss',
            'Received Power',
            'Carrier-to-Noise-Ratio',
            'Spectral Efficiency',
            'Channel Capacity',
            'Aggregate Channel Capacity',
        ]
    )

    long_data.columns = ['Constellation', 'Number of Satellites', 'Metric', 'Value']

    long_data = long_data.loc[long_data['Number of Satellites'] < 1000]

    sns.set(font_scale=1.1, font="Times New Roman", rc={'figure.figsize':(12,8)})

    plot = sns.relplot(
        x="Number of Satellites", y='Value', linewidth=1.2, hue='Constellation',
        col="Metric", col_wrap=2,
        palette=sns.color_palette("bright", 3),
        kind="line", data=long_data,
        facet_kws=dict(sharex=False, sharey=False), legend='full'#, ax=ax
    )

    handles = plot._legend_data.values()
    labels = plot._legend_data.keys()
    plot._legend.remove()
    plot.fig.legend(handles=handles, labels=labels, loc='lower center', ncol=7)
    plt.subplots_adjust(hspace=0.3, wspace=0.3, bottom=0.07)
    plot.axes[0].set_ylabel('Free Space Path Loss (dB)')
    plot.axes[1].set_ylabel('Received Power (dB)')
    plot.axes[0].set_xlabel('Number of Satellites')
    plot.axes[1].set_xlabel('Number of Satellites')
    plot.axes[2].set_ylabel('Carrier-to-Noise-Ratio (dB)')
    plot.axes[0].set_xlabel('Number of Satellites')
    plot.axes[3].set_ylabel('Spectral Efficiency (Bps/Hz)')
    plot.axes[0].set_xlabel('Number of Satellites')
    plot.axes[4].set_ylabel('Channel Capacity (Gbps)')
    plot.axes[0].set_xlabel('Number of Satellites')
    plot.axes[5].set_ylabel('Aggregate Channel Capacity (Gbps)')
    plot.axes[0].set_xlabel('Number of Satellites')

    plt.savefig(os.path.join(VIS, 'engineering_metrics.png'), dpi=300)


def process_capacity_data(data):
    """
    Process capacity data.

    """
    output = {}

    constellations = [
        'starlink',
        'oneweb',
        'kuiper',
    ]

    for constellation in constellations:

        max_satellites_set = set() #get the maximum network density
        coverage_area_set = set() #and therefore minimum coverage area

        for idx, item in data.iterrows():
            if constellation.lower() == item['Constellation'].lower():
                max_satellites_set.add(item['Number of Satellites'])
                coverage_area_set.add(item['Coverage Area'])

        max_satellites = max(list(max_satellites_set)) #max density
        coverage_area = min(list(coverage_area_set)) #minimum coverage area

        capacity_results = []

        for idx, item in data.iterrows():
            if constellation.lower() == item['Constellation'].lower():
                if item['Number of Satellites'] == max_satellites:
                    capacity_results.append(item['Aggregate Channel Capacity'])

        mean_capacity = sum(capacity_results) / len(capacity_results)

        output[constellation] = {
            'number_of_satellites': max_satellites,
            'satellite_coverage_area': coverage_area,
            'capacity': mean_capacity,
            'capacity_kmsq': mean_capacity / coverage_area,
        }

    return output


def plot_panel_plot_of_per_user_metrics(capacity, parameters):
    """

    """
    constellations = [
        'starlink',
        'oneweb',
        'kuiper'
    ]

    results = []

    for constellation in constellations:

        overbooking_factor = parameters[constellation.lower()]['overbooking_factor']

        for i in range(5, 101):

            i = (i / 100)

            if constellation.lower() == 'starlink':
                capacity_kmsq = capacity[constellation]['capacity_kmsq']
                coverage_area_km = capacity[constellation]['satellite_coverage_area']
                cost_per_satellite_npv =  588820
            elif constellation.lower() == 'oneweb':
                capacity_kmsq = capacity[constellation]['capacity_kmsq']
                coverage_area_km = capacity[constellation]['satellite_coverage_area']
                cost_per_satellite_npv =   5565027
            elif constellation.lower() == 'kuiper':
                capacity_kmsq = capacity[constellation]['capacity_kmsq']
                coverage_area_km = capacity[constellation]['satellite_coverage_area']
                cost_per_satellite_npv =   3087811
            else:
                print('did not recognize constellation')

            cost_kmsq = cost_per_satellite_npv / coverage_area_km

            results.append({
                'constellation': constellation,
                'subscribers_kmsq': i,
                'capacity_per_subscriber': capacity_kmsq / (i / overbooking_factor),
                'cost_per_subscriber': cost_kmsq / i,
            })

    results = pd.DataFrame(results)

    results['Constellation'] = results['constellation'].copy()
    results['Constellation'] = results['Constellation'].replace(regex='starlink', value='Starlink')
    results['Constellation'] = results['Constellation'].replace(regex='oneweb', value='OneWeb')
    results['Constellation'] = results['Constellation'].replace(regex='kuiper', value='Kuiper')

    sns.set(font_scale=1, font="Times New Roman")

    #Now plot results
    fig, axs = plt.subplots(1, 2, figsize=(10, 5.5))

    axs[0] = sns.lineplot(x="subscribers_kmsq", y="capacity_per_subscriber",
                        hue="Constellation", data=results, ax=axs[0])
    axs[0].set(xlabel='Subscriber Density (km^2)', ylabel='Mean Capacity (Mbps)')
    axs[0].title.set_text('(A) Mean Capacity Per Subscriber (Busy Hour) (OBF: 20)')

    axs[1] = sns.lineplot(x="subscribers_kmsq", y="cost_per_subscriber",
                        hue="Constellation", data=results, ax=axs[1])
    axs[1].set(xlabel='Subscriber Density (km^2)', ylabel='NPV TCO Per Subscriber ($USD)')
    axs[1].title.set_text('(B) 10-Year NPV TCO Per Subscriber')

    plt.subplots_adjust(hspace=0.25, wspace=.25, bottom=0.4)
    plt.tight_layout()

    plt.savefig(os.path.join(VIS, 'capacity_per_user.png'))
    plt.clf()


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
    data = data.loc[data['constellation'] == 'Starlink'].reset_index()
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

    sns.set(font_scale=.85, font="Times New Roman")

    fig, ax = plt.subplots(1, 1, figsize=(10, 5.5))#(13, 6))

    minx, miny, maxx, maxy = regions.total_bounds
    ax.set_xlim(minx+10, maxx)
    ax.set_ylim(miny-5, maxy)

    regions.plot(column='bin', ax=ax, cmap='inferno_r',
        linewidth=0, legend=True, edgecolor='grey')

    ctx.add_basemap(ax, crs=regions.crs, source=ctx.providers.CartoDB.Voyager)

    fig.suptitle('Population Density by Sub-National Region (n={})'.format(n), y=0.87)

    fig.tight_layout()
    fig.savefig(os.path.join(VIS, 'region_by_pop_density.png'))

    plt.close(fig)


def plot_capacity_per_user_maps(data, regions):
    """

    """
    n = len(regions)
    data = data.loc[data['scenario'] == 'baseline'].reset_index()

    regions = regions[['GID_id', 'geometry']]#[:1000]

    constellations = data['constellation'].unique()#[:1]

    sns.set(font_scale=1, font="Times New Roman")

    fig, axs = plt.subplots(3, 1, figsize=(10, 12)) #width height

    i = 0

    for constellation in list(constellations):

        subset = data.loc[data['constellation'] == constellation]

        subset = subset[['GID_id', 'per_user_capacity']]

        regions_merged = regions.merge(subset, left_on='GID_id', right_on='GID_id')
        regions_merged.reset_index(drop=True, inplace=True)

        metric = 'per_user_capacity'

        # bins = [-1,2,4,6,8,10,12,14,16,18,1e9]
        # bins = [-1,5,10,15,20,25,30,35,40,45,1e9]
        bins = [-1,10,20,30,40,50,60,70,80,90,1e9]
        labels = [
            '<10 Mbps',
            '<20 Mbps',
            '<30 Mbps',
            '<40 Mbps',
            '<50 Mbps',
            '<60 Mbps',
            '<70 Mbps',
            '<80 Mbps',
            '<90 Mbps',
            '>90 Mbps',
        ]
        regions_merged['bin'] = pd.cut(
            regions_merged[metric],
            bins=bins,
            labels=labels
        )#.fillna('<20')

        minx, miny, maxx, maxy = regions_merged.total_bounds
        axs[i].set_xlim(minx, maxx)
        axs[i].set_ylim(miny, maxy)

        regions_merged.plot(column='bin', ax=axs[i], cmap='inferno_r',
            linewidth=0, legend=True)

        ctx.add_basemap(axs[i], crs=regions_merged.crs,
            source=ctx.providers.CartoDB.Voyager)

        letter = get_letter(constellation)

        axs[i].set_title("({}) {} Mean Per User Capacity Based on 1 Percent Adoption (n={})".format(
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
    elif constellation == 'Kuiper':
        return 'C'
    else:
        print('Did not recognize constellation')


if __name__ == '__main__':

    if not os.path.exists(VIS):
        os.makedirs(VIS)

    print('Loading capacity simulation results')
    path = os.path.join(RESULTS, 'sim_results.csv')
    sim_results = pd.read_csv(path)#[:1000]

    print('Plotting capacity simulation results')
    plot_aggregated_engineering_metrics(sim_results)

    print('Processing capacity data')
    capacity = process_capacity_data(sim_results)

    print('Generating data for panel plots')
    plot_panel_plot_of_per_user_metrics(capacity, parameters)

    print('Loading shapes')
    path = os.path.join(DATA_INTERMEDIATE, 'all_regional_shapes.shp')
    if not os.path.exists(path):
        shapes = get_regional_shapes()
        shapes.to_file(path)
    else:
        shapes = gpd.read_file(path, crs='epsg:4326')#[:1000]

    print('Loading data by pop density geotype')
    path = os.path.join(RESULTS, 'global_results.csv')
    global_results = pd.read_csv(path)#[:1000]

    print('Plotting population density per area')
    plot_regions_by_geotype(global_results, shapes)

    print('Plotting capacity per user')
    plot_capacity_per_user_maps(global_results, shapes)

    print('Complete')
