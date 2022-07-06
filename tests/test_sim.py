import pytest
from globalsat.sim import (
    system_capacity,
    calc_geographic_metrics,
    calc_free_space_path_loss,
    generate_log_normal_dist_value,
    calc_antenna_gain,
    calc_losses,
    calc_eirp,
    calc_received_power,
    calc_noise,
    calc_cnr,
    calc_spectral_efficiency,
    calc_capacity,
    single_satellite_capacity,
    calc_agg_capacity,
    soyuz_fg,
    falcon_9,
    falcon_heavy,
    ariane,
    calc_per_sat_emission
)


def test_system_capacity(setup_params, setup_lut):
    """
    Integration test for main system capacity function.

    """
    number_of_satellites = 10

    results = system_capacity('starlink', number_of_satellites, setup_params, setup_lut)[0]

    assert results['number_of_satellites'] == 10
    assert round(results['distance']) == 10
    assert results['satellite_coverage_area'] == 10
    assert results['iteration'] == 0
    assert round(results['path_loss']) == 136
    assert round(results['antenna_gain']) == 38
    assert round(results['eirp']) == 68
    assert round(results['received_power']) == -41.0
    assert round(results['noise']) == -90
    assert round(results['cnr']) == 49.0
    assert results['spectral_efficiency'] == 5.768987
    assert round(results['channel_capacity']) == 1442
    assert round(results['capacity_kmsq']) == 288


def test_calc_geographic_metrics():
    """
    Unit test for calculating geographic metrics including:

    - Distance between the transmitter and reciever
    - Coverage area for each satellite.

    """
    number_of_satellites = 10

    params = {
        'total_area_earth_km_sq': 100,
        'altitude_km': 10,
    }

    # area_of_earth_covered = total_area_earth_km_sq * portion_of_earth_covered
    # network_density = number_of_satellites / area_of_earth_covered
    # satellite_coverage_area = (area_of_earth_covered / number_of_satellites) / 1000
    # mean_distance_between_assets = math.sqrt((1 / network_density)) / 2
    # distance = math.sqrt((mean_distance_between_assets**2) + (altitude_km**2))

    # 80 km^2 = 100 * 0.8
    # 0.125 satellites km^2 = 10 satellites / 80 km^2
    # 8 km^2 satellite coverage area = 80 km^2 / 10 satellites
    # 1.41 km on average = math.sqrt((1 / 0.125 km^2 )) / (2)
    # 10.1 km = math.sqrt((1.41**2) + (10**2))

    distance, satellite_coverage_area = calc_geographic_metrics(
        number_of_satellites, params
    )

    assert round(distance) == 10
    assert satellite_coverage_area == 10


def test_calc_free_space_path_loss():
    """
    Unit test for calculating the free space path loss.

    """
    distance = 10
    params = {'speed_of_light': 300000000, 'dl_frequency': 13500000000}
    i = 0
    random_variations = [1]

    result, random_variation = calc_free_space_path_loss(
        distance, params, i, random_variations
    )

    assert round(result) == 136


def test_generate_log_normal_dist_value():
    """
    Unit test for generating random values using a lognormal distribution.

    """
    assert round(generate_log_normal_dist_value(13.5, 10, 7.8, 1, 1)[0]) == 2
    assert round(generate_log_normal_dist_value(13.5, 1, 10, None, 1)[0]) == 1


def test_antenna_gain():
    """
    Unit test for calculating the antenna gain.

    """
    c = 3e8 #speed of light m/s
    d = 0.7 #Antenna Diameter in metres
    f = 13500000000 #Frequency in Hertz
    n = 0.6 #Antenna Efficiency

    assert round(calc_antenna_gain(c, d, f, n)) == 38


def test_calc_losses():
    """
    Unit test for estimating the transmission losses

    """
    rain_attenuation = 10
    all_other_losses = 0.53

    result = calc_losses(rain_attenuation, all_other_losses)

    assert result == 10.53


def test_calc_eirp():
    """
    Unit test for calculating the Equivalent Isotropically Radiated Power.

    """
    power = 30 # watts
    antenna_gain = 38 # dB
    # losses = 4 #dB

    assert round(calc_eirp(power, antenna_gain)) == 68


def test_calc_received_power():
    """
    Unit test for calculating received power.

    """
    eirp = 68 # dBi
    path_loss = 136 # dB
    receiver_gain = 37 # dummy values
    losses = 10.57

    assert round(calc_received_power(eirp, path_loss, receiver_gain, losses)) == -42


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


def test_calc_spectral_efficiency(setup_lut):
    """
    Unit test for finding the spectral efficiency.

    """
    #using actual lut
    assert calc_spectral_efficiency(0, setup_lut) == 1.647211 # bits/Hz/s
    assert calc_spectral_efficiency(7.5, setup_lut) == 2.193247 # bits/Hz/s
    assert calc_spectral_efficiency(10.7, setup_lut) == 2.856231 # bits/Hz/s
    assert calc_spectral_efficiency(18.83, setup_lut) == 5.593162 # bits/Hz/s
    assert calc_spectral_efficiency(28, setup_lut) == 5.768987 # bits/Hz/s


def test_calc_capacity():
    """
    Unit test for calculating the channel capacity.

    """
    spectral_efficiency = 1 # bits per Hertz
    dl_bandwidth = 1e6 # Hertz

    assert calc_capacity(spectral_efficiency, dl_bandwidth) == 1 #mbps


def test_calc_agg_capacity():
    """
    Unit test for calculating the aggregate capacity.

    """
    channel_capacity = 100
    number_of_channels = 1
    polarization = 2

    assert calc_agg_capacity(channel_capacity, number_of_channels, polarization) == 200 #mbps


def test_single_satellite_capacity():
    """
    Unit test for calculating satellite capacity

    """
    dl_bandwidth_Hz = 250000000
    spectral_efficiency = 5.1152
    number_of_channels = 8
    polarizations = 2

    capacity = single_satellite_capacity(dl_bandwidth_Hz, spectral_efficiency,
               number_of_channels, polarizations)

    return capacity == 20460.8


def test_soyuz_fg():
    """
    Unit test for calculating soyuz FG emissions.

    """
    hypergolic = 218150
    kerosene = 7360

    emission = soyuz_fg(hypergolic, kerosene) 

    return emission                         #alumina_emission': 586.15       


def test_falcon_heavy():
    """
    Unit test for calculating falcon heavy emission.
    
    """
    kerosene = 1397000

    emissions = falcon_heavy(kerosene) 

    return emissions                 #'alumina_emission': 69850


def test_falcon_9():
    """
    Unit test for calculating falcon 9 emissions.
    
    """
    kerosene = 488370

    emissions = falcon_9(kerosene) 

    return emissions           #'alumina_emission': 24418.5


def test_ariane():
    """
    Unit test for calculating ariane 5 emissions.
    
    """  
    hypergolic = 10000

    solid = 480000

    cryogenic = 184900

    emissions = ariane(hypergolic, solid, cryogenic)

    return emissions               #'alumina_emission': 158410.0


def test_emission_per_sat():
    """
    Unit test for calculating emission for every satellite.
    
    """
    name = "Kuiper"

    fuel_mass = 0

    fuel_mass_1 = 10000

    fuel_mass_2 = 480000

    fuel_mass_3 = 184900

    sat_emissions = calc_per_sat_emission(name, fuel_mass, fuel_mass_1, fuel_mass_2, fuel_mass_3)

    return sat_emissions   #'alumina_emission': 158410.0 for Kuiper.
