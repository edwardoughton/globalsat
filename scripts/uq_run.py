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

df = pd.read_csv("uq_parameters.csv")
uq_dict = df.to_dict('records') #Convert the csv to list

results = []
for item in uq_dict:
    constellation = item["constellation"]

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


    results.append({"constellation": constellation, 
                    "signal_path": distance,
                    "satellite_coverage_area_km": satellite_coverage_area_km,
                    "path_loss": path_loss,
                    "losses": losses,
                    "antenna_gain": antenna_gain,
                    "cnr": cnr,
                    "spectral_efficiency": spectral_efficiency,
                    "channel_capacity": channel_capacity,
                    "agg_capacity": agg_capacity,
                    "sat_capacity": sat_capacity,
                    "capacity_per_single_satellite": sat_capacity,
                    "aluminium_oxide_emissions_t":emission_dict['alumina_emission']/1000,
                    "sulphur_oxide_emissions_t": emission_dict['sulphur_emission']/1000,
                    "carbon_oxide_emissions_t": emission_dict['carbon_emission']/1000,
                    "cfc_gases_emissions_t": emission_dict['cfc_gases']/1000,
                    "particulate_matter_emissions_t": emission_dict['particulate_matter']/1000,
                    "photochemical_oxidation_emissions_t": emission_dict['photo_oxidation']/1000,
                    "total_emissions_t": ((emission_dict['alumina_emission'])
                                       + (emission_dict['sulphur_emission'])
                                       + (emission_dict['carbon_emission'])
                                       + (emission_dict['cfc_gases']) 
                                       + (emission_dict['particulate_matter'])
                                       + (emission_dict['photo_oxidation']))/1000})

    df = pd.DataFrame.from_dict(results)
    df.to_csv("uq_results.csv")