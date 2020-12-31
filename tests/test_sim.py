import pytest
from globalsat.sim import (
    system_capacity,
    calc_geographic_metrics,
    calc_free_space_path_loss,
    generate_log_normal_dist_value,
    calc_antenna_gain,
    calc_eirp,
    calc_received_power,
    calc_noise,
    calc_cnr,
    calc_spectral_efficiency,
    calc_capacity,
)


def test_system_capacity(setup_params):
    """
    Integration test for main system capacity function.

    """
    number_of_satellites = 10

    results = system_capacity(number_of_satellites, setup_params)[0]

    assert results['number_of_satellites'] == 10
    assert round(results['distance']) == 10
    assert results['satelite_coverage_area'] == 8
    assert results['iteration'] == 0
    assert round(results['path_loss']) == 136
    assert round(results['antenna_gain']) == 38
    assert round(results['eirp']) == 64
    assert round(results['received_power']) == -72
    assert round(results['noise']) == -90
    assert round(results['cnr']) == 18
    assert results['spectral_efficiency'] == 4.936639
    assert round(results['capacity']) == 1234
    assert round(results['capacity_kmsq']) == 154


def test_calc_geographic_metrics():
    """
    Unit test for calculating geographic metrics including:

    - Distance between the transmitter and reciever
    - Coverage area for each satellite.

    """
    number_of_satellites = 10

    params = {
        'total_area_earth_km_sq': 100,
        'portion_of_earth_covered': 0.8,
        'altitude_km': 10,
    }

    # area_of_earth_covered = total_area_earth_km_sq * portion_of_earth_covered
    # network_density = number_of_satellites / area_of_earth_covered
    # satelite_coverage_area = area_of_earth_covered / number_of_satellites
    # mean_distance_between_assets = math.sqrt((1 / network_density)) / 2
    # distance = math.sqrt((mean_distance_between_assets**2) + (altitude_km**2))

    # 80 km^2 = 100 * 0.8
    # 0.125 satellites km^2 = 10 satellites / 80 km^2
    # 8 km^2 satellite coverage area = 80 km^2 / 10 satellites
    # 1.41 km on average = math.sqrt((1 / 0.125 km^2 )) / (2)
    # 10.1 km = math.sqrt((1.41**2) + (10**2))

    distance, satelite_coverage_area = calc_geographic_metrics(number_of_satellites, params)

    assert round(distance) == 10
    assert satelite_coverage_area == 8


def test_calc_free_space_path_loss():
    """
    Unit test for calculating the free space path loss.

    """
    distance = 10
    params = {'speed_of_light': 300000000, 'dl_frequency': 13500000000}
    i = 0
    random_variations = [1]

    result = calc_free_space_path_loss(distance, params, i, random_variations)

    assert round(result) == 136


def test_generate_log_normal_dist_value():
    """
    Unit test for generating random values using a lognormal distribution.

    """
    assert round(generate_log_normal_dist_value(13.5, 2, 1, 1, 1)[0]) == 1


def test_antenna_gain():
    """
    Unit test for calculating the antenna gain.

    """
    c = 3e8 #speed of light m/s
    d = 0.7 #Antenna Diameter in metres
    f = 13500000000 #Frequency in Hertz
    n = 0.6 #Antenna Efficiency

    assert round(calc_antenna_gain(c, d, f, n)) == 38


def test_calc_eirp():
    """
    Unit test for calculating the Equivalent Isotropically Radiated Power.

    """
    power = 40 # watts
    antenna_gain = 38 # dB
    losses = 4 #dB

    assert round(calc_eirp(power, antenna_gain, losses)) == 74


def test_calc_received_power():
    """
    Unit test for calculating received power.

    """
    eirp = 74 # dBi
    path_loss = 136 # dB

    assert round(calc_received_power(eirp, path_loss)) == -62


def test_calc_noise():
    """
    Unit test for calculating receiver noise.

    """
    assert round(calc_noise()) == -90


def test_calc_cnr():
    """
    Unit test for calculating the Carrier-to-Noise Ratio (CNR).

    """
    received_power = -62 # dB
    noise = -90 # dB

    assert round(calc_cnr(received_power, noise)) == 28


def test_calc_spectral_efficiency():
    """
    Unit test for finding the spectral efficnecy.

    """
    cnr = 28 #dB

    assert calc_spectral_efficiency(cnr) == 5.900855 # bits/Hz/s


def test_calc_capacity():
    """
    Unit test for finding the spectral efficnecy.

    """
    spectral_efficiency = 1 # bits per Hertz
    dl_bandwidth = 1e6 # Hertz

    assert calc_capacity(spectral_efficiency, dl_bandwidth) == 1 #mbps
