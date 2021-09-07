"""
Process settlement layer

Written by Ed Oughton.

December 2020

"""
import os
import configparser
import json
import math
import glob
import numpy as np
import pandas as pd
import geopandas as gpd
import pyproj
from shapely.geometry import Point, LineString, Polygon, MultiPolygon, shape, mapping, box
from shapely.ops import unary_union, nearest_points, transform
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio.mask import mask
from rasterstats import zonal_stats, gen_zonal_stats
from tqdm import tqdm

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

DATA_RAW = os.path.join(BASE_PATH, 'raw')
DATA_INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')
DATA_PROCESSED = os.path.join(BASE_PATH, 'processed')


def find_country_list(continent_list):
    """
    This function produces country information by continent.

    Parameters
    ----------
    continent_list : list
        Contains the name of the desired continent, e.g. ['Africa']

    Returns
    -------
    countries : list of dicts
        Contains all desired country information for countries in
        the stated continent.

    """
    path = os.path.join(DATA_RAW, 'gadm36_levels_shp', 'gadm36_0.shp')
    countries = gpd.read_file(path)

    glob_info_path = os.path.join(DATA_RAW, '..', 'global_information.csv')
    load_glob_info = pd.read_csv(glob_info_path, encoding = "ISO-8859-1")
    countries = countries.merge(load_glob_info, left_on='GID_0',
        right_on='ISO_3digit')

    if len(continent_list) > 0:
        selected_countries = countries.loc[countries['continent'].isin(continent_list)]
    else:
        selected_countries = countries.loc[countries['global'] == 1]

    countries = []

    for index, country in selected_countries.iterrows():

        countries.append({
            'country_name': country['country'],
            'iso3': country['GID_0'],
            'iso2': country['ISO_2digit'],
            'regional_level': country['gid_region'],
        })

    return countries


def process_country_shapes(country):
    """
    Creates a single national boundary for the desired country.

    Parameters
    ----------
    country : string
        Three digit ISO country code.

    """
    iso3 = country['iso3']

    path = os.path.join(DATA_INTERMEDIATE, iso3)

    if os.path.exists(os.path.join(path, 'national_outline.shp')):
        return 'Completed national outline processing'

    if not os.path.exists(path):
        # print('Creating directory {}'.format(path))
        os.makedirs(path)

    shape_path = os.path.join(path, 'national_outline.shp')

    # print('Loading all country shapes')
    path = os.path.join(DATA_RAW, 'gadm36_levels_shp', 'gadm36_0.shp')
    countries = gpd.read_file(path)

    # print('Getting specific country shape for {}'.format(iso3))
    single_country = countries[countries.GID_0 == iso3]

    # print('Excluding small shapes')
    single_country['geometry'] = single_country.apply(
        exclude_small_shapes, axis=1)

    # print('Adding ISO country code and other global information')
    glob_info_path = os.path.join(DATA_RAW, 'global_information.csv')
    load_glob_info = pd.read_csv(glob_info_path, encoding = "ISO-8859-1")
    single_country = single_country.merge(
        load_glob_info,left_on='GID_0', right_on='ISO_3digit')

    single_country.to_file(shape_path, driver='ESRI Shapefile')

    return


def process_regions(country):
    """
    Function for processing the lowest desired subnational regions for the
    chosen country.

    Parameters
    ----------
    country : string
        Three digit ISO country code.

    """
    regions = []

    iso3 = country['iso3']
    level = country['regional_level']

    for regional_level in range(1, level + 1):

        filename = 'regions_{}_{}.shp'.format(regional_level, iso3)
        folder = os.path.join(DATA_INTERMEDIATE, iso3, 'regions')
        path_processed = os.path.join(folder, filename)

        if os.path.exists(path_processed):
            continue

        if not os.path.exists(folder):
            os.mkdir(folder)

        filename = 'gadm36_{}.shp'.format(regional_level)
        path_regions = os.path.join(DATA_RAW, 'gadm36_levels_shp', filename)
        regions = gpd.read_file(path_regions)

        regions = regions[regions.GID_0 == iso3]

        regions['geometry'] = regions.apply(exclude_small_shapes, axis=1)

        try:
            regions.to_file(path_processed, driver='ESRI Shapefile')
        except:
            pass

    return


def process_settlement_layer(country):
    """
    Clip the settlement layer to the chosen country boundary and place in
    desired country folder.

    Parameters
    ----------
    country : string
        Three digit ISO country code.

    """
    iso3 = country['iso3']

    path_settlements = os.path.join(DATA_RAW,'settlement_layer',
        'ppp_2020_1km_Aggregated.tif')

    settlements = rasterio.open(path_settlements, 'r+')
    settlements.nodata = 255
    settlements.crs = {"init": "epsg:4326"}

    iso3 = country['iso3']
    path_country = os.path.join(DATA_INTERMEDIATE, iso3,
        'national_outline.shp')

    if os.path.exists(path_country):
        country = gpd.read_file(path_country)
    else:
        print('Must generate national_outline.shp first for {}'.format(iso3) )

    path_country = os.path.join(DATA_INTERMEDIATE, iso3)
    shape_path = os.path.join(path_country, 'settlements.tif')

    if os.path.exists(shape_path):
        return

    bbox = country.envelope
    geo = gpd.GeoDataFrame()

    geo = gpd.GeoDataFrame({'geometry': bbox})

    coords = [json.loads(geo.to_json())['features'][0]['geometry']]

    #chop on coords
    out_img, out_transform = mask(settlements, coords, crop=True)

    # Copy the metadata
    out_meta = settlements.meta.copy()

    out_meta.update({"driver": "GTiff",
                    "height": out_img.shape[1],
                    "width": out_img.shape[2],
                    "transform": out_transform,
                    "crs": 'epsg:4326'})

    with rasterio.open(shape_path, "w", **out_meta) as dest:
            dest.write(out_img)

    return


def exclude_small_shapes(x):
    """
    Remove small multipolygon shapes.

    Parameters
    ---------
    x : polygon
        Feature to simplify.

    Returns
    -------
    MultiPolygon : MultiPolygon
        Shapely MultiPolygon geometry without tiny shapes.

    """
    # if its a single polygon, just return the polygon geometry
    if x.geometry.geom_type == 'Polygon':
        return x.geometry

    # if its a multipolygon, we start trying to simplify
    # and remove shapes if its too big.
    elif x.geometry.geom_type == 'MultiPolygon':

        area1 = 0.01
        area2 = 50

        # dont remove shapes if total area is already very small
        if x.geometry.area < area1:
            return x.geometry
        # remove bigger shapes if country is really big

        if x['GID_0'] in ['CHL','IDN']:
            threshold = 0.01
        elif x['GID_0'] in ['RUS','GRL','CAN','USA']:
            threshold = 0.01

        elif x.geometry.area > area2:
            threshold = 0.1
        else:
            threshold = 0.001

        # save remaining polygons as new multipolygon for
        # the specific country
        new_geom = []
        for y in x.geometry:
            if y.area > threshold:
                new_geom.append(y)

        return MultiPolygon(new_geom)


def create_pop_regional_lookup(country):
    """
    Extract regional luminosity and population data.

    Parameters
    ----------

    country : string
        Three digit ISO country code.

    """
    level = country['regional_level']
    iso3 = country['iso3']
    GID_level = 'GID_{}'.format(level)

    filename = 'population_lookup_level_{}.csv'.format(level)
    path_output = os.path.join(DATA_INTERMEDIATE, iso3, filename)

    if os.path.exists(path_output):
        output = pd.read_csv(path_output).to_dict('records')
        return output

    filename = 'settlements.tif'
    path_settlements = os.path.join(DATA_INTERMEDIATE, iso3, filename)

    filename = 'regions_{}_{}.shp'.format(level, iso3)
    folder = os.path.join(DATA_INTERMEDIATE, iso3, 'regions')
    regions = gpd.read_file(os.path.join(folder, filename), crs='epsg:4326')

    output = []

    for index, region in regions.iterrows():

        area_km = get_area(region['geometry'])

        population = find_population(region, path_settlements)

        if not isinstance(population, float):
            continue

        if population > 0:
            pop_density_km2 = population / area_km
        else:
            pop_density_km2 = 0

        output.append({
            'iso3': iso3,
            'regions': region[GID_level],
            'population': population,
            'area_m': area_km,
            'pop_density_km2': pop_density_km2,
        })

    output_pandas = pd.DataFrame(output)

    output_pandas.to_csv(path_output, index=False)

    return output


def find_population(region, path_settlements):
    """

    """
    with rasterio.open(path_settlements) as src:

        affine = src.transform
        array = src.read(1)
        array[array <= 0] = 0

        population = [d['sum'] for d in zonal_stats(
            region['geometry'], array, stats=['sum'], affine=affine)][0]

    return population


def get_area(modeling_region_geom):
    """
    Return the area in square km.

    """
    project = pyproj.Transformer.from_crs('epsg:4326', 'epsg:3857', always_xy=True).transform
    new_geom = transform(project, modeling_region_geom)
    area_km = new_geom.area / 1e6

    return area_km


if __name__ == '__main__':

    countries = find_country_list([])#[:2] #['Africa']

    output = []

    for country in tqdm(countries):

        print('-Working on {}: {}'.format(country['country_name'], country['iso3']))

        process_country_shapes(country)

        process_regions(country)

        process_settlement_layer(country)

        results = create_pop_regional_lookup(country)

        output = output + results

    path_output = os.path.join(DATA_INTERMEDIATE, 'global_regional_population_lookup.csv')
    output = pd.DataFrame(output)
    output.to_csv(path_output, index=False)

    print('Preprocessing complete')
