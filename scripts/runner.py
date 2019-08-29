"""

Simulation runner script

"""
import configparser
import csv
import os

from globalsat.simulator import SimulationManager
from globalsat.econ import assess_econ
from globalsat.risk import assess_risk

CONFIG = configparser.ConfigParser()
CONFIG.read(os.path.join(os.path.dirname(__file__), 'script_config.ini'))
BASE_PATH = CONFIG['file_locations']['base_path']

# INTERMEDIATE = os.path.join(BASE_PATH, 'intermediate')



#Import input data




#Functions to write out data
def write_results(network_manager, folder, scenario):
    """
    Write results to .csv file.
    """
    # suffix = _get_suffix(pop_scenario, throughput_scenario, intervention_strategy)
    # if not os.path.exists(folder):
    #     os.mkdir(folder)
    # metrics_filename = os.path.join(folder,
    #     'pcd_metrics_{}.csv'.format(suffix))

    # if year == BASE_YEAR:
    #     metrics_file = open(metrics_filename, 'w', newline='')
    #     metrics_writer = csv.writer(metrics_file)
    #     metrics_writer.writerow(
    #         ('year', 'postcode', 'cost', 'demand', 'capacity',
    #         'capacity_deficit', 'population', 'pop_density'))
    # else:
    #     metrics_file = open(metrics_filename, 'a', newline='')
    #     metrics_writer = csv.writer(metrics_file)

    # for pcd in network_manager.postcode_sectors.values():
    #     demand = pcd.demand
    #     capacity = pcd.capacity
    #     capacity_deficit = capacity - demand
    #     pop = pcd.population
    #     pop_d = pcd.population_density
    #     cost = cost_by_pcd[pcd.id]

    #     metrics_writer.writerow(
    #         (year, pcd.id, cost, demand, capacity,
    #         capacity_deficit, pop, pop_d))

    # metrics_file.close()




if __name__ == '__main__':

    folder = os.path.join(BASE_PATH, '..', 'results')

    START = 0
    END = 10
    TIMESTEP_INCREMENT = 1
    TIMESTEPS = range(START, END + 1, TIMESTEP_INCREMENT)

    ASSETS = [
        {
            'id': 'ABC',
            'x': 1,
            'y': 2,
            'z': 3,
            'vx': 10,
            'vy': 10,
            'vz': 10,
            'orbit': 'geo',
            'constellation': 'oneweb',
            'age': '2',
            'fragility': '??',
            'exposure': 150,
            'design': 'nano',
            'cost': 250000000,
        }
    ]

    PARAMETERS = {
        'iterations': 100
    }

    SCENARIO = [
        ('low'),
        ('baseline'),
        ('high'),
    ]

    for scenario in SCENARIO:
        for timestep in TIMESTEPS:

            if timestep == START:
                system = SimulationManager(ASSETS, PARAMETERS)

            system = assess_risk(system, scenario)

            econ_impacts = assess_econ(system)

        write_results(system, folder, scenario)
