import math
import numpy as np
import pandas as pd
import globalsat.sim as gb
from random import gauss
from inputs import parameters, lut


def uncertain_capacity():

    results = []

    earth_atmospheric_losses_std = 3
    distance_std = 5
    antenna_efficiency_std = 0.1
    receiver_gain_std = 5
    antenna_diameter_std = 0.1
    downlink_frequency_std = 0.1
    N = 1000
    for n in range(N):
        for key, item in parameters.items():

            earth_atmospheric_losses = gauss(item["earth_atmospheric_losses"], 
                                       earth_atmospheric_losses_std)

            receiver_gain = gauss(item["receiver_gain"], receiver_gain_std)

            antenna_efficiency = gauss(item["antenna_efficiency"], antenna_efficiency_std)

            antenna_diameter = gauss(item["antenna_diameter"], antenna_diameter_std)

            downlink_frequency = gauss(item["dl_frequency"], downlink_frequency_std)

            constellation = item["name"]

            distance, satellite_coverage_area_km = gb.calc_geographic_metrics(
                                                   item["number_of_satellites"], item)

            distance_km = gauss(distance, distance_std)                                       
            

            path_loss = gb.calc_space_path_loss(distance_km, item)                                       

            losses = gb.calc_losses(earth_atmospheric_losses, 
                     item["all_other_losses"])

            antenna_gain = gb.calc_antenna_gain(item["speed_of_light"],
                           antenna_diameter, downlink_frequency,
                           antenna_efficiency)

            eirp = gb.calc_eirp(item["power"], antenna_gain) 

            noise = gb.calc_noise()  

            received_power = gb.calc_received_power(eirp, path_loss, 
                             receiver_gain, losses)

            cnr = gb.calc_cnr(received_power, noise)

            spectral_efficiency = gb.calc_spectral_efficiency(cnr, lut)
            
            channel_capacity = gb.calc_capacity(spectral_efficiency, item["dl_bandwidth"])

            agg_capacity = gb.calc_agg_capacity(channel_capacity, 
                           item["number_of_channels"], item["polarization"])

            sat_capacity = gb.single_satellite_capacity(item["dl_bandwidth"],
                           spectral_efficiency, item["number_of_channels"], 
                           item["polarization"])

            
            results.append({"constellation": constellation, "losses": losses, 
                            "path_loss": path_loss, "antenna_gain": antenna_gain, 
                            "earth_atmospheric_losses": earth_atmospheric_losses,
                            "distance": distance, 
                            "satellite_coverage_area_km": satellite_coverage_area_km, 
                            "eirp": eirp, "noise": noise,
                            "received_power": received_power, "cnr":cnr, 
                            "spectral_efficiency":spectral_efficiency,
                            "channel_capacity": channel_capacity,
                            "aggregate_capacity": agg_capacity,
                            "sat_capacity": sat_capacity})

    df = pd.DataFrame.from_dict(results)
    df.to_csv("uncertainity_results.csv")

    return df
uncertain_capacity()