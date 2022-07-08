"""
Simulation run script for Globalsat.

Written by Bonface Osoro & Ed Oughton.

December 2022

"""
from __future__ import division
import configparser
import os
import math
from numpy import savez_compressed
import pandas as pd

import globalsat.sim as gb
from inputs import lut
from cost import cost_model

#Import the data.

data_path = "/Users/osoro/Codebase/globalsat/data/"
df = pd.read_csv(data_path + "uq_parameters.csv")
uq_dict = df.to_dict('records') #Convert the csv to list

path = "/Users/osoro/Codebase/globalsat/results/"
results = []
for item in uq_dict:
    constellation = item["constellation"]

    number_of_satellites = item["number_of_satellites"]

    random_variations = gb.generate_log_normal_dist_value(
        item['dl_frequency_Hz'],
        item['mu'],
        item['sigma'],
        item['seed_value'],
        item['iterations'])

    distance, satellite_coverage_area_km = gb.calc_geographic_metrics(
                                           item["number_of_satellites"], item)

    path_loss = 20*math.log10(distance) + 20*math.log10(item['dl_frequency_Hz']/1e9) + 92.45

    losses = gb.calc_losses(item["earth_atmospheric_losses_dB"], 
                     item["all_other_losses_dB"])

    antenna_gain = gb.calc_antenna_gain(item["speed_of_light"],
                           item["antenna_diameter_m"], item["dl_frequency_Hz"],
                           item["antenna_efficiency"]) 

    eirp = gb.calc_eirp(item["power_dBw"], antenna_gain)

    noise = gb.calc_noise()

    received_power = gb.calc_received_power(eirp, path_loss, 
                             item["receiver_gain_dB"], losses)

    cnr = gb.calc_cnr(received_power, noise)

    spectral_efficiency = gb.calc_spectral_efficiency(cnr, lut)
            
    channel_capacity = gb.calc_capacity(spectral_efficiency, item["dl_bandwidth_Hz"])

    agg_capacity = gb.calc_agg_capacity(channel_capacity, 
                   item["number_of_channels"], item["polarization"])

    sat_capacity = gb.single_satellite_capacity(item["dl_bandwidth_Hz"],
                   spectral_efficiency, item["number_of_channels"], 
                   item["polarization"])

    emission_dict = gb.calc_per_sat_emission(item["constellation"], item["fuel_mass_kg"],
                    item["fuel_mass_1_kg"], item["fuel_mass_2_kg"], item["fuel_mass_3_kg"])

    total_cost_ownership = cost_model(item["satellite_launch_cost"], item["ground_station_cost"], 
                           item["spectrum_cost"], item["regulation_fees"], 
                           item["digital_infrastructure_cost"], item["ground_station_energy"], 
                           item["subscriber_acquisition"], item["staff_costs"], 
                           item["research_development"], item["maintenance"], 
                           item["discount_rate"], item["assessment_period_year"])             
    cost_per_capacity = total_cost_ownership / sat_capacity* number_of_satellites

    aluminium_oxide_emissions = emission_dict['alumina_emission']
    sulphur_oxide_emissions = emission_dict['sulphur_emission']
    carbon_oxide_emissions = emission_dict['carbon_emission']
    cfc_gases_emissions = emission_dict['cfc_gases']
    particulate_matter_emissions = emission_dict['particulate_matter']
    photochemical_oxidation_emissions = emission_dict['photo_oxidation']
    total_emissions = aluminium_oxide_emissions + sulphur_oxide_emissions \
                      + carbon_oxide_emissions + cfc_gases_emissions \
                      + particulate_matter_emissions \
                      + photochemical_oxidation_emissions


    results.append({"constellation": constellation, 
                    "signal_path": distance,
                    "satellite_coverage_area_km": satellite_coverage_area_km,
                    "path_loss": path_loss,
                    "losses": losses,
                    "antenna_gain": antenna_gain,
                    "eirp_dB": eirp,
                    "noise": noise,
                    "received_power_dB": received_power,
                    "cnr": cnr,
                    "spectral_efficiency": spectral_efficiency,
                    "channel_capacity": channel_capacity,
                    "agg_capacity": agg_capacity,
                    "capacity_per_single_satellite": sat_capacity,
                    "capacity_per_area_mbps/sqkm": agg_capacity/item["coverage_area_per_sat_sqkm"],
                    "total_cost_ownership": total_cost_ownership,
                    "cost_per_capacity": cost_per_capacity,
                    "aluminium_oxide_emissions": aluminium_oxide_emissions,
                    "sulphur_oxide_emissions": sulphur_oxide_emissions,
                    "carbon_oxide_emissions": carbon_oxide_emissions,
                    "cfc_gases_emissions": cfc_gases_emissions,
                    "particulate_matter_emissions": particulate_matter_emissions,
                    "photochemical_oxidation_emissions": photochemical_oxidation_emissions,
                    "total_emissions_t": total_emissions})

    df = pd.DataFrame.from_dict(results)
    df.to_csv(path + "uq_results.csv")