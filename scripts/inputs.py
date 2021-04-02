"""
Inputs for Globalsat simulation.

Written by Bonface Osoro & Ed Oughton.

December 2020

"""

parameters = {
    'starlink': {
        'number_of_satellites': 5040,
        'iterations': 100,
        'seed_value': 42,
        'mu': 1, #Mean of distribution
        'sigma': 7.8, #Standard deviation of distribution
        'total_area_earth_km_sq': 510000000, #Area of Earth in km^2
        'altitude_km': 550, #Altitude of starlink satellites in km
        'dl_frequency': 13.5*10**9, #Downlink frequency in Hertz
        'dl_bandwidth': 0.25*10**9, #Downlink bandwidth in Hertz
        'speed_of_light': 3.0*10**8, #Speed of light in vacuum
        'antenna_diameter': 0.7, #Metres
        'antenna_efficiency': 0.6,
        'power': 30, #dBw
        'losses': 4, #dB
        'receiver_gain': 38,
        'rain_attenuation': 0, #Rain Attenuation
        'all_other_losses': 0.53, #All other losses
        'number_of_channels': 8, #Number of channels per satellite
        'overbooking_factor': 20, # 1 in 20 users access the network
    },
    'oneweb': {
        'number_of_satellites': 720,
        'iterations': 100,
        'seed_value': 42,
        'mu': 1, #Mean of distribution
        'sigma': 7.8, #Standard deviation of distribution
        'total_area_earth_km_sq': 510000000, #Area of Earth in km^2
        'altitude_km': 1200, #Altitude of starlink satellites in km
        'dl_frequency': 13.5*10**9, #Downlink frequency in Hertz
        'dl_bandwidth': 0.25*10**9,
        'speed_of_light': 3.0*10**8, #Speed of light in vacuum
        'antenna_diameter': 0.75, #Metres
        'antenna_efficiency': 0.6,
        'power': 30, #dBw
        'losses': 4, #dB
        'receiver_gain': 38,
        'rain_attenuation': 0, #Rain Attenuation
        'all_other_losses': 0.53, #All other losses
        'number_of_channels': 16, #Number of channels per satellite
        'overbooking_factor': 20, # 1 in 20 users access the network
    },
    'kuiper': {
        'number_of_satellites': 3236,
        'iterations': 100,
        'seed_value': 42,
        'mu': 1, #Mean of distribution
        'sigma': 7.8, #Standard deviation of distribution
        'total_area_earth_km_sq': 510000000, #Area of Earth in km^2
        'altitude_km': 610, #Altitude of starlink satellites in km
        'dl_frequency': 17.7*10**9, #Downlink frequency in Hertz
        'dl_bandwidth': 0.25*10**9,
        'speed_of_light': 3.0*10**8, #Speed of light in vacuum
        'antenna_diameter': 1, #Metres
        'antenna_efficiency': 0.6,
        'power': 30, #dBw
        'receiver_gain': 39,
        'rain_attenuation': 0, #Rain Attenuation
        'all_other_losses': 0.53, #All other losses
        'number_of_channels': 8, #Number of channels per satellite
        'overbooking_factor': 20, # 1 in 20 users access the network
    },
    # 'telesat': {
    #     'number_of_satellites': 300,
    #     'iterations': 5,
    #     'seed_value': 42,
    #     'mu': 1, #Mean of distribution
    #     'sigma': 7.8, #Standard deviation of distribution
    #     'total_area_earth_km_sq': 510000000, #Area of Earth in km^2
    #     'portion_of_earth_covered': 0.8, #We assume the poles aren't covered
    #     'altitude_km': 550, #Altitude of starlink satellites in km
    #     'dl_frequency': 13.5*10**9, #Downlink frequency in Hertz
    #     'dl_bandwidth': 0.25*10**9,
    #     'speed_of_light': 3.0*10**8, #Speed of light in vacuum
    #     'antenna_diameter': 0.7, #Metres
    #     'antenna_efficiency': 0.6,
    #     'power': 30, #dBw
    #     'losses': 4, #dB
    # },
}

lut = [
    (5.12, 1.647211),
    (5.96, 1.972253),
    (6.54, 1.972253),
    (6.83, 2.104850),
    (7.5, 2.193247),
    (7.79, 2.281645),
    (7.40, 2.370043),
    (8.0, 2.370043),
    (8.37, 2.458441),
    (8.42, 2.524739),
    (9.26, 2.635236),
    (9.70, 2.745734),
    (10.64, 2.856231),
    (11.98, 3.077225),
    (11.09, 3.386618),
    (11.74, 3.291954),
    (12.16, 3.510192),
    (13.04, 3.620536),
    (13.97, 3.841226),
    (14.8, 4.206428),
    (15.46, 4.338659),
    (15.86, 4.603122),
    (16.54, 4.735354),
    (17.72, 4.936639),
    (18.52, 5.163248),
    (16.97, 5.355556),
    (17.23, 5.065690),
    (18.0, 5.241514),
    (18.58, 5.417338),
    (18.83, 5.593162),
    (19.56, 5.768987),
]
