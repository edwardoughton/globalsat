"""
Parameters for Globalsat constellations.

Written by Bonface Osoro & Ed Oughton.

December 2020

"""

parameters = {
    'starlink': {
        'number_of_satellites': 6000,
        'iterations': 5,
        'seed_value': 42,
        'mu': 1, #Mean of distribution
        'sigma': 7.8, #Standard deviation of distribution
        'total_area_earth_km_sq': 510000000, #Area of Earth in km^2
        'portion_of_earth_covered': 0.8, #We assume the poles aren't covered
        'altitude_km': 550, #Altitude of starlink satellites in km
        'dl_frequency': 13.5*10**9, #Downlink frequency in Hertz
        'dl_bandwidth': 0.25*10**9, #Downlink bandwidth in Hertz
        'speed_of_light': 3.0*10**8, #Speed of light in vacuum
        'antenna_diameter': 0.7, #Metres
        'antenna_efficiency': 0.6,
        'power': 30, #dBw
        'losses': 4, #dB
    },
    'oneweb': {
        'number_of_satellites': 600,
        'iterations': 5,
        'seed_value': 42,
        'mu': 1, #Mean of distribution
        'sigma': 7.8, #Standard deviation of distribution
        'total_area_earth_km_sq': 510000000, #Area of Earth in km^2
        'portion_of_earth_covered': 0.8, #We assume the poles aren't covered
        'altitude_km': 550, #Altitude of starlink satellites in km
        'dl_frequency': 13.5*10**9, #Downlink frequency in Hertz
        'dl_bandwidth': 0.25*10**9,
        'speed_of_light': 3.0*10**8, #Speed of light in vacuum
        'antenna_diameter': 0.7, #Metres
        'antenna_efficiency': 0.6,
        'power': 30, #dBw
        'losses': 4, #dB
    },
    'telesat': {
        'number_of_satellites': 300,
        'iterations': 5,
        'seed_value': 42,
        'mu': 1, #Mean of distribution
        'sigma': 7.8, #Standard deviation of distribution
        'total_area_earth_km_sq': 510000000, #Area of Earth in km^2
        'portion_of_earth_covered': 0.8, #We assume the poles aren't covered
        'altitude_km': 550, #Altitude of starlink satellites in km
        'dl_frequency': 13.5*10**9, #Downlink frequency in Hertz
        'dl_bandwidth': 0.25*10**9,
        'speed_of_light': 3.0*10**8, #Speed of light in vacuum
        'antenna_diameter': 0.7, #Metres
        'antenna_efficiency': 0.6,
        'power': 30, #dBw
        'losses': 4, #dB
    },
}
