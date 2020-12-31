from pytest import fixture


@fixture(scope='function')
def setup_params():
    return {
        'iterations': 1,
        'seed_value': 1,
        'mu': 2,
        'sigma': 1,
        'total_area_earth_km_sq': 100, #Area of Earth in km^2
        'portion_of_earth_covered': 0.8, #We assume the poles aren't covered
        'altitude_km': 10, #Altitude of starlink satellites in km
        'dl_frequency': 13.5*10**9, #Downlink frequency in Hertz
        'dl_bandwidth': 0.25*10**9,
        'speed_of_light': 3.0*10**8, #Speed of light in vacuum
        'antenna_diameter': 0.7, #Metres
        'antenna_efficiency': 0.6,
        'power': 30, #dBw
        'losses': 4, #dB
    }
