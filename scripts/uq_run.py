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

    distance, satellite_coverage_area_km = gb.calc_geographic_metrics(
                                           item["number_of_satellites"], item)

    path_loss = (20*math.log10(distance) 
                + 20*math.log10(item["dl_frequency_Hz"]/1e9)) + 92.45

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
                    "sat_capacity": sat_capacity})

    df = pd.DataFrame.from_dict(results)
    df.to_csv("uq_results.csv")