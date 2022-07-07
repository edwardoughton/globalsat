import numpy as np
import pandas as pd
from random import gauss
from inputs import parameters, lut

def uq_inputs_generator():

    uq_parameters = []

    N = 5 #Number of datapoints to generate

    for number in range(N):
        for key, item in parameters.items():
            number_of_satellites = item["number_of_satellites"]
            name = item["name"]
            iterations = item['iterations']
            seed_value = item['seed_value']
            mu = item['mu']
            sigma = item['sigma']
            total_area_earth_km_sq = item["total_area_earth_km_sq"]
            altitude_km = gauss(item["altitude_km"], 5)
            dl_frequency_Hz = gauss(item["dl_frequency"], 0.1)
            dl_bandwidth_Hz = item["dl_bandwidth"]
            speed_of_light = item["speed_of_light"]
            antenna_diameter_m = gauss(item["antenna_diameter"], 0.2)
            antenna_efficiency = gauss(item["antenna_efficiency"], 0.1)
            power_dBw = item["power"]
            receiver_gain_dB = gauss(item["receiver_gain"], 5)
            earth_atmospheric_losses_dB = gauss(item["earth_atmospheric_losses"], 3)
            all_other_losses_dB = gauss(item["all_other_losses"], 0.2)
            number_of_channels = item["number_of_channels"]
            polarization = item["polarization"]
            fuel_mass_kg = item["fuel_mass"]
            fuel_mass_1_kg = item["fuel_mass_1"]
            fuel_mass_2_kg = item["fuel_mass_2"]
            fuel_mass_3_kg = item["fuel_mass_3"]
            satellite_launch_cost = gauss(item["satellite_launch_cost"], 10000000)
            ground_station_cost = gauss(item["ground_station_cost"], 5000000)
            spectrum_cost = gauss(item["spectrum_cost"], 20000000)
            regulation_fees = gauss(item["regulation_fees"], 2000000)
            digital_infrastructure_cost = gauss(item["digital_infrastructure_cost"], 1000000)
            ground_station_energy = gauss(item["ground_station_energy"], 1000000)
            subscriber_acquisition = gauss(item["subscriber_acquisition"], 10000000)
            staff_costs = gauss(item["staff_costs"], 10000000)
            research_development = gauss(item["research_development"], 1000000)
            maintenance = gauss(item["maintenance"], 1000000)
            discount_rate = item["discount_rate"]
            assessment_period_year = item["assessment_period"]

            uq_parameters.append({"constellation": name, 
                                  "iterations": iterations,
                                  "seed_value": seed_value,
                                  "mu": mu,
                                  "sigma": sigma,
                                  "number_of_satellites": number_of_satellites,
                                  "total_area_earth_km_sq": total_area_earth_km_sq,
                                  "coverage_area_per_sat_sqkm": total_area_earth_km_sq/number_of_satellites,
                                  "altitude_km": altitude_km,
                                  "dl_frequency_Hz": dl_frequency_Hz,
                                  "dl_bandwidth_Hz": dl_bandwidth_Hz,
                                  "speed_of_light": speed_of_light,
                                  "antenna_diameter_m": antenna_diameter_m,
                                  "antenna_efficiency": antenna_efficiency,
                                  "power_dBw": power_dBw,
                                  "receiver_gain_dB": receiver_gain_dB,
                                  "earth_atmospheric_losses_dB": earth_atmospheric_losses_dB,
                                  "all_other_losses_dB": all_other_losses_dB,
                                  "number_of_channels": number_of_channels,
                                  "polarization": polarization,
                                  "fuel_mass_kg": fuel_mass_kg,
                                  "fuel_mass_1_kg": fuel_mass_1_kg,
                                  "fuel_mass_2_kg": fuel_mass_2_kg,
                                  "fuel_mass_3_kg": fuel_mass_3_kg,
                                  "satellite_launch_cost": satellite_launch_cost,
                                  "ground_station_cost": ground_station_cost,
                                  "spectrum_cost": spectrum_cost,
                                  "regulation_fees": regulation_fees,
                                  "digital_infrastructure_cost": digital_infrastructure_cost,
                                  "ground_station_energy": ground_station_energy,
                                  "subscriber_acquisition": subscriber_acquisition,
                                  "staff_costs": staff_costs,
                                  "research_development": research_development,
                                  "maintenance": maintenance,
                                  "discount_rate": discount_rate,
                                  "assessment_period_year": assessment_period_year})
    
    df = pd.DataFrame.from_dict(uq_parameters)
    df.to_csv("uq_parameters.csv")
            
    return df.shape
uq_inputs_generator()