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
    #calc_received_power = eirp+path_loss+receiver_gain+losses

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
    #calc_capacity = spectral_efficiency*dl_bandwidth/1e6

    assert calc_capacity(spectral_efficiency, dl_bandwidth) == 1 #mbps


def test_calc_agg_capacity():
    """
    Unit test for calculating the aggregate capacity.

    """
    channel_capacity = 100
    number_of_channels = 1
    polarization = 2
    #calc_agg_capacity = channel_capacity*number_of_channels*polarization

    assert calc_agg_capacity(channel_capacity, number_of_channels, polarization) == 200 #mbps


def test_single_satellite_capacity():
    """
    Unit test for calculating satellite capacity

    """
    dl_bandwidth_Hz = 250000000
    spectral_efficiency = 5.1152
    number_of_channels = 8
    polarizations = 2
    #capacity = (dl_bandwidth_Hz/1000000)*spectral_efficiency*number_of_channels*polarizations

    capacity = single_satellite_capacity(dl_bandwidth_Hz, spectral_efficiency,
               number_of_channels, polarizations)

    assert capacity == 20460.8


def test_soyuz_fg():
    """
    Unit test for calculating soyuz FG emissions.

    """
    hypergolic = 218150
    kerosene = 7360
    #emission['alumina_emission'] = (hypergolic*1*0.001) + (kerosene*1*0.05)
    # emission["sulphur_emission"] = (hypergolic*0.7*0.001) + (kerosene*0.7*0.001)
    # emission["carbon_emission"] = (hypergolic*0.252*1) + (kerosene*0.352*1)
    # emission["cfc_gases"] = (hypergolic*0.016*0.7) + (kerosene*0.016*0.7) 
                            #  + (hypergolic*0.003*0.7) + (kerosene*0.003*0.7) 
                            # + (hypergolic*0.001*0.7) + (kerosene*0.001*0.7)
    # emission["particulate_matter"] = (hypergolic*0.001*0.22) + (kerosene *0.001*0.22) 
                                    # + (hypergolic*0.001*1) + (kerosene*0.05*1)
    # emission["photo_oxidation"] = (hypergolic*0.378*0.0456) + (kerosene *0.528*0.0456) 
                                # + (hypergolic*0.001*1) + (kerosene*0.001*1)

    emission = soyuz_fg(hypergolic, kerosene)
    assert emission['alumina_emission'] == 586.15   
    assert emission["sulphur_emission"] == 157.857
    assert emission["carbon_emission"] == 57564.520000000004
    assert emission["cfc_gases"] == 3157.1399999999994
    assert emission["particulate_matter"] == 635.7622
    assert emission["photo_oxidation"] == 4162.923167999999                         


def test_falcon_9():
    """
    Unit test for calculating falcon heavy emission.

    """
    kerosene = 488370
    #emission['alumina_emission'] = (kerosene*0.05)
    # emission["sulphur_emission"] = (kerosene*0.001*0.7)
    # emission["carbon_emission"] = (kerosene*0.352*1)
    # emission["cfc_gases"] = (kerosene*0.016*0.7) + (kerosene*0.003*0.7) 
                              #+ (kerosene*0.001*0.7)
    # emission["particulate_matter"] = (kerosene*0.001*0.22) + (kerosene*0.05*1)
    # emission["photo_oxidation"] = (kerosene*0.0456*0.528) + (kerosene*0.001*1)

    emission = falcon_9(kerosene)
    assert emission['alumina_emission'] == 24418.5                  
    assert emission["sulphur_emission"] == 341.859
    assert emission["carbon_emission"] == 171906.24
    assert emission["cfc_gases"] == 6837.18
    assert emission["particulate_matter"] == 24525.9414
    assert emission["photo_oxidation"] == 12246.756816000003


def test_falcon_heavy():
    """
    Unit test for calculating falcon 9 emissions.

    """
    kerosene = 1397000
    #emission['alumina_emission'] = (kerosene*0.05)
    # emission["sulphur_emission"] = (kerosene*0.001*0.7)
    # emission["carbon_emission"] = (kerosene*0.352*1)
    # emission["cfc_gases"] = (kerosene*0.016*0.7) + (kerosene*0.003*0.7) 
                              #+ (kerosene*0.001*0.7)
    # emission["particulate_matter"] = (kerosene*0.001*0.22) + (kerosene*0.05*1)
    # emission["photo_oxidation"] = (kerosene*0.0456*0.528) + (kerosene*0.001*1)

    emission = falcon_heavy(kerosene)
    assert emission['alumina_emission'] == 69850.0          
    assert emission["sulphur_emission"] == 977.9
    assert emission["carbon_emission"] == 491744.0
    assert emission["cfc_gases"] == 19558.0
    assert emission["particulate_matter"] == 70157.34
    assert emission["photo_oxidation"] == 35032.289600000004


def test_ariane():
    """
    Unit test for calculating ariane 5 emissions.

    """
    hypergolic = 10000
    solid = 480000
    cryogenic = 184900
    #emission['alumina_emission'] = (solid*0.33*1) + (hypergolic*0.001*1)
    # emission["sulphur_emission"] = (solid*0.005*0.7) + (cryogenic*0.001*0.7) 
                                    # + (hypergolic*0.001*0.7)+(solid*0.15*0.88)
    # emission["carbon_emission"] = (solid*0.108*1) + (hypergolic*0.252)
    # emission["cfc_gases"] = (solid*0.08*0.7) + (cryogenic*0.016*0.7) 
                            #  + (hypergolic*0.016*0.7) + (solid*0.015*0.7) 
                            #  + (cryogenic*0.003*0.7) + (hypergolic*0.003*0.7) 
                            #  + (solid*0.005*0.7) + (cryogenic*0.001*0.7) 
                            #  + (hypergolic*0.001*0.7) + (solid*0.15*0.7)
    # emission["particulate_matter"] = (solid*0.005*0.22) + (cryogenic*0.001*0.22) 
                                    #   + (hypergolic*0.001*0.22) + (solid*0.33*1) 
                                    #   + (hypergolic*0.001*1)
    # emission["photo_oxidation"] = (solid*0.162*0.0456) + (hypergolic*0.378*0.0456) 
                                #    + (solid*0.005*1) + (cryogenic*0.001*1) 
                                #    + (hypergolic*0.001*1)

    emission = ariane(hypergolic, solid, cryogenic)
    assert emission['alumina_emission'] == 158410.0               
    assert emission["sulphur_emission"] == 65176.43
    assert emission["carbon_emission"] == 54360.0
    assert emission["cfc_gases"] == 86728.6
    assert emission["particulate_matter"] == 158980.878
    assert emission["photo_oxidation"] == 6313.124


def test_emission_per_sat():
    """
    Unit test for calculating emission for every satellite.

    """

    fuel_mass = 488370
    fuel_mass_1 = 0
    fuel_mass_2 = 0
    fuel_mass_3 = 0
    #emission['alumina_emission'] = (kerosene*0.05)
    # emission["sulphur_emission"] = (kerosene*0.001*0.7)
    # emission["carbon_emission"] = (kerosene*0.352*1)
    # emission["cfc_gases"] = (kerosene*0.016*0.7) + (kerosene*0.003*0.7) 
                              #+ (kerosene*0.001*0.7)
    # emission["particulate_matter"] = (kerosene*0.001*0.22) + (kerosene*0.05*1)
    # emission["photo_oxidation"] = (kerosene*0.0456*0.528) + (kerosene*0.001*1)

    sat_emissions = calc_per_sat_emission("Starlink", fuel_mass, fuel_mass_1, fuel_mass_2, fuel_mass_3)
    assert sat_emissions['alumina_emission'] == 24418.5   #'alumina_emission': 158410.0 for Kuiper.
    assert sat_emissions["sulphur_emission"] == 341.859
    assert sat_emissions["carbon_emission"] == 171906.24
    assert sat_emissions["cfc_gases"] == 6837.18
    assert sat_emissions["particulate_matter"] == 24525.9414
    assert sat_emissions["photo_oxidation"] == 12246.756816000003
    
    fuel_mass = 218150
    fuel_mass_1 = 7360
    fuel_mass_2 = 0
    fuel_mass_3 = 0
    #emission['alumina_emission'] = (hypergolic*1*0.001) + (kerosene*1*0.05)
    # emission["sulphur_emission"] = (hypergolic*0.7*0.001) + (kerosene*0.7*0.001)
    # emission["carbon_emission"] = (hypergolic*0.252*1) + (kerosene*0.352*1)
    # emission["cfc_gases"] = (hypergolic*0.016*0.7) + (kerosene*0.016*0.7) 
                            #  + (hypergolic*0.003*0.7) + (kerosene*0.003*0.7) 
                            # + (hypergolic*0.001*0.7) + (kerosene*0.001*0.7)
    # emission["particulate_matter"] = (hypergolic*0.001*0.22) + (kerosene *0.001*0.22) 
                                    # + (hypergolic*0.001*1) + (kerosene*0.05*1)
    # emission["photo_oxidation"] = (hypergolic*0.378*0.0456) + (kerosene *0.528*0.0456) 
                                # + (hypergolic*0.001*1) + (kerosene*0.001*1)

    sat_emissions = calc_per_sat_emission("OneWeb", fuel_mass, fuel_mass_1, fuel_mass_2, fuel_mass_3)
    assert sat_emissions['alumina_emission'] == 7.36 
    assert sat_emissions["sulphur_emission"] == 5.152
    assert sat_emissions["carbon_emission"] == 1854.72
    assert sat_emissions["cfc_gases"] == 103.04
    assert sat_emissions["particulate_matter"] == 8.9792
    assert sat_emissions["photo_oxidation"] == 134.222848

    fuel_mass = 0
    fuel_mass_1 = 10000
    fuel_mass_2 = 480000
    fuel_mass_3 = 184900
    #emission['alumina_emission'] = (solid*0.33*1) + (hypergolic*0.001*1)
    # emission["sulphur_emission"] = (solid*0.005*0.7) + (cryogenic*0.001*0.7) 
                                    # + (hypergolic*0.001*0.7)+(solid*0.15*0.88)
    # emission["carbon_emission"] = (solid*0.108*1) + (hypergolic*0.252)
    # emission["cfc_gases"] = (solid*0.08*0.7) + (cryogenic*0.016*0.7) 
                            #  + (hypergolic*0.016*0.7) + (solid*0.015*0.7) 
                            #  + (cryogenic*0.003*0.7) + (hypergolic*0.003*0.7) 
                            #  + (solid*0.005*0.7) + (cryogenic*0.001*0.7) 
                            #  + (hypergolic*0.001*0.7) + (solid*0.15*0.7)
    # emission["particulate_matter"] = (solid*0.005*0.22) + (cryogenic*0.001*0.22) 
                                    #   + (hypergolic*0.001*0.22) + (solid*0.33*1) 
                                    #   + (hypergolic*0.001*1)
    # emission["photo_oxidation"] = (solid*0.162*0.0456) + (hypergolic*0.378*0.0456) 
                                #    + (solid*0.005*1) + (cryogenic*0.001*1) 
                                #    + (hypergolic*0.001*1)

    sat_emissions = calc_per_sat_emission("Kuiper", fuel_mass, fuel_mass_1, fuel_mass_2, fuel_mass_3)
    assert sat_emissions['alumina_emission'] == 158410.0 
    assert sat_emissions["sulphur_emission"] == 65176.43
    assert sat_emissions["carbon_emission"] == 54360.0
    assert sat_emissions["cfc_gases"] == 86728.6
    assert sat_emissions["particulate_matter"] == 158980.878
    assert sat_emissions["photo_oxidation"] == 6313.124