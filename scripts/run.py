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

RESULTS = os.path.join(BASE_PATH, '..', 'results')


if __name__ == '__main__':

    results = []

    for constellation, params in parameters.items():

        for number_of_satellites in range(60, params['number_of_satellites'] + 60, 60):

            data = system_capacity(constellation, number_of_satellites, params, lut)

            results = results + data

    results = pd.DataFrame(results)

    path = os.path.join(RESULTS, 'sim_results.csv')
    results.to_csv(path, index=False)
