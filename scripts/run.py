"""
Simulation run script for Globalsat.

Written by Bonface Osoro & Ed Oughton.

December 2020

"""
import configparser
import os
import pandas as pd

from globalsat.sim import system_capacity
from inputs import parameters, lut

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')
RESULTS = os.path.join(BASE_PATH, '..', 'results')


def process_capacity_data(data, constellations):
    """
    Process capacity data.

    """
    output = {}

    for constellation in constellations:

        max_satellites_set = set() #get the maximum network density
        coverage_area_set = set() #and therefore minimum coverage area

        for idx, item in data.iterrows():
            if constellation.lower() == item['constellation'].lower():
                max_satellites_set.add(item['number_of_satellites'])
                coverage_area_set.add(item['satellite_coverage_area'])

        max_satellites = max(list(max_satellites_set)) #max density
        coverage_area = min(list(coverage_area_set)) #minimum coverage area

        channel_capacity_results = []
        aggregate_capacity_results = []

        for idx, item in data.iterrows():
            if constellation.lower() == item['constellation'].lower():
                if item['number_of_satellites'] == max_satellites:
                    channel_capacity_results.append(item['channel_capacity']) #append to list
                    aggregate_capacity_results.append(item['aggregate_capacity']) #append to list

        mean_channel_capacity = sum(channel_capacity_results) / len(channel_capacity_results)
        mean_agg_capacity = sum(aggregate_capacity_results) / len(aggregate_capacity_results)

        output[constellation] = {
            'number_of_satellites': max_satellites,
            'satellite_coverage_area': coverage_area,
            'channel_capacity': mean_channel_capacity,
            'aggregate_capacity': mean_agg_capacity,
            'capacity_kmsq': mean_agg_capacity / coverage_area,
        }

    return output


def process_mean_results(data, capacity, constellation, scenario, parameters):
    """
    Process results.

    """
    output = []

    adoption_rate = scenario[1]
    overbooking_factor = parameters[constellation.lower()]['overbooking_factor']
    constellation_capacity = capacity[constellation]

    max_capacity = constellation_capacity['capacity_kmsq']
    number_of_satellites = constellation_capacity['number_of_satellites']
    satellite_coverage_area = constellation_capacity['satellite_coverage_area']

    for idx, item in data.iterrows():

        users_per_km2 = item['pop_density_km2'] * (adoption_rate / 100)

        active_users_km2 = users_per_km2 / overbooking_factor

        if active_users_km2 > 0:
            per_user_capacity = max_capacity / active_users_km2
        else:
            per_user_capacity = 0

        output.append({
            'scenario': scenario[0],
            'constellation': constellation,
            'number_of_satellites': number_of_satellites,
            'satellite_coverage_area': satellite_coverage_area,
            'iso3': item['iso3'],
            'GID_id': item['regions'],
            'population': item['population'],
            'area_m': item['area_m'],
            'pop_density_km2': item['pop_density_km2'],
            'adoption_rate': adoption_rate,
            'users_per_km2': users_per_km2,
            'active_users_km2': active_users_km2,
            'per_user_capacity': per_user_capacity,
        })

    return output


def process_stochastic_results(data, results, constellation, scenario, parameters):
    """
    Process results.

    """
    output = []

    overbooking_factor = parameters[constellation.lower()]['overbooking_factor']

    for i in range(0, 6):

        if i == 0:
            i = 0.1

        for idx, result in results.iterrows():

            if constellation.lower() == result['constellation']:

                if constellation == 'Starlink':
                    if not result['number_of_satellites'] == 5040:
                        continue
                if constellation == 'OneWeb':
                    if not result['number_of_satellites'] == 720:
                        continue
                if constellation == 'Kuiper':
                    if not result['number_of_satellites'] == 3240:
                        continue

                users_per_km2 = i

                active_users_km2 = users_per_km2 / overbooking_factor

                if active_users_km2 > 0:
                    per_user_capacity = result['capacity_kmsq'] / active_users_km2
                else:
                    per_user_capacity = 0

                output.append({
                    'scenario': scenario[0],
                    'constellation': constellation,
                    'iteration': result['iteration'],
                    'number_of_satellites': result['number_of_satellites'],
                    'satellite_coverage_area': result['satellite_coverage_area'],
                    'pop_density_km2': i,
                    'users_per_km2': users_per_km2,
                    'active_users_km2': active_users_km2,
                    'per_user_capacity': per_user_capacity,
                })

    return output


if __name__ == '__main__':

    CONSTELLATIONS = [
        'Starlink',
        'OneWeb',
        'Kuiper',
    ]

    SCENARIO = [
        ('low', 0.5),
        ('baseline', 1),
        ('high', 2),
    ]

    results = []

    ##generate simulation results for all constellation satellite densities
    for constellation, params in parameters.items():
        for number_of_satellites in range(60, params['number_of_satellites'] + 60, 60):

            data = system_capacity(constellation, number_of_satellites, params, lut)

            results = results + data

    results = pd.DataFrame(results)

    path = os.path.join(RESULTS, 'sim_results.csv')
    results.to_csv(path, index=False)

    ##process global results
    capacity = process_capacity_data(results, CONSTELLATIONS)

    path = os.path.join(INTERMEDIATE, 'global_regional_population_lookup.csv')
    global_data = pd.read_csv(path)

    all_results = []

    for constellation in CONSTELLATIONS:

        for scenario in SCENARIO:

            output = process_mean_results(global_data, capacity, constellation,
                          scenario, parameters)

            all_results = all_results + output

    all_results = pd.DataFrame(all_results)

    if not os.path.exists(RESULTS):
        os.makedirs(RESULTS)

    path = os.path.join(RESULTS, 'global_results.csv')
    all_results.to_csv(path, index=False)

    ##process stochastic results
    path = os.path.join(INTERMEDIATE, 'global_regional_population_lookup.csv')
    global_data = pd.read_csv(path)#[:1]

    all_results = []

    for constellation in CONSTELLATIONS:

        for scenario in SCENARIO:

            if not scenario[0] == 'baseline':
                continue

            output = process_stochastic_results(global_data, results,
                        constellation, scenario, parameters)

            all_results = all_results + output

    all_results = pd.DataFrame(all_results)

    if not os.path.exists(RESULTS):
        os.makedirs(RESULTS)

    path = os.path.join(RESULTS, 'stochastic_user_capacity_results.csv')
    all_results.to_csv(path, index=False)
