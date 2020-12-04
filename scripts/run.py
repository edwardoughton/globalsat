"""
Simulation runner script

"""
import configparser
import csv
import os
import pandas as pd
from itertools import tee

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')
RESULTS = os.path.join(BASE_PATH, '..', 'results')

def get_results(data, max_capacity, parameters, scenario):
    """
    Process results.

    """
    output = []

    adoption_rate = scenario[1]
    overbooking_factor = parameters['overbooking_factor']

    for idx, item in data.iterrows():

        users_per_km2 = item['pop_density_km2'] * (adoption_rate / 100)

        active_users_km2 = users_per_km2 / overbooking_factor

        if active_users_km2 > 0:
            per_user_capacity = max_capacity / active_users_km2
        else:
            per_user_capacity = 0

        output.append({
            'iso3': item['iso3'],
            'GID_id': item['regions'],
            'population': item['population'],
            'area_m': item['area_m'],
            'pop_density_km2': item['pop_density_km2'],
            'scenario': scenario[0],
            'adoption_rate': adoption_rate,
            'users_per_km2': users_per_km2,
            'active_users_km2': active_users_km2,
            'per_user_capacity': per_user_capacity,
        })

    return output


if __name__ == '__main__':

    path = os.path.join(INTERMEDIATE, 'global_regional_population_lookup.csv')
    data = pd.read_csv(path)#[:1]

    MAX_CAPACITY = 200

    PARAMETERS = {
        'overbooking_factor': 20
    }

    SCENARIO = [
        ('low', 5),
        ('baseline', 10),
        ('high', 20),
    ]

    all_results = []

    for scenario in SCENARIO:

        results = get_results(data, MAX_CAPACITY, PARAMETERS, scenario)

        all_results = all_results + results

    all_results = pd.DataFrame(all_results)

    if not os.path.exists(RESULTS):
        os.makedirs(RESULTS)

    path = os.path.join(RESULTS, 'results.csv')
    all_results.to_csv(path, index=False)
