"""
Globalsat simulation model.

Developed by Bonface Osaro and Ed Oughton.

December 2022

"""
import math
import numpy as np
from itertools import tee
from collections import OrderedDict


def system_capacity(constellation, number_of_satellites, params, lut):
    """
    Find the system capacity.

    Parameters
    ----------
    constellation : string
        Consetellation selected for assessment.
    number_of_satellites : int
        Number of satellites in the contellation being simulated.
    params : dict
        Contains all simulation parameters.
    lut : list of tuples
        Lookup table for CNR to spectral efficiency.

    Returns
    -------
    results : list of dicts
        System capacity results generated by the simulation.

    """
    results = []

    distance, satellite_coverage_area_km = calc_geographic_metrics(
        number_of_satellites, params
        )

    random_variations = generate_log_normal_dist_value(
            params['dl_frequency'],
            params['mu'],
            params['sigma'],
            params['seed_value'],
            params['iterations']
        )

    for i in range(0, params['iterations']):

        path_loss, random_variation = calc_free_space_path_loss(
            distance, params, i, random_variations
        )

        antenna_gain = calc_antenna_gain(
            params['speed_of_light'],
            params['antenna_diameter'],
            params['dl_frequency'],
            params['antenna_efficiency']
        )

        eirp = calc_eirp(params['power'], antenna_gain)

        losses = calc_losses(params['earth_atmospheric_losses'], params['all_other_losses'])

        noise = calc_noise()

        received_power = calc_received_power(eirp, path_loss, params['receiver_gain'], losses)

        cnr = calc_cnr(received_power, noise)

        spectral_efficiency = calc_spectral_efficiency(cnr, lut)

        channel_capacity = calc_capacity(spectral_efficiency, params['dl_bandwidth'])

        agg_capacity = calc_agg_capacity(channel_capacity, params['number_of_channels'], 
                       params['polarization'])

        sat_capacity = single_satellite_capacity(params['dl_bandwidth'],
                       spectral_efficiency, params['number_of_channels'],
                       params['polarization'])

        results.append({
            'constellation': constellation,
            'number_of_satellites': number_of_satellites,
            'distance': distance,
            'satellite_coverage_area': satellite_coverage_area_km,
            'iteration': i,
            'path_loss': path_loss,
            'random_variation': random_variation,
            'antenna_gain': antenna_gain,
            'eirp': eirp,
            'received_power': received_power,
            'noise': noise,
            'cnr': cnr,
            'spectral_efficiency': spectral_efficiency,
            'channel_capacity': channel_capacity,
            'aggregate_capacity': agg_capacity,
            'capacity_kmsq': agg_capacity / satellite_coverage_area_km,
            'capacity_per_single_satellite': sat_capacity,
        })

    return results


def calc_geographic_metrics(number_of_satellites, params):
    """
    Calculate geographic metrics, including (i) the distance between the transmitter
    and reciever, and (ii) the coverage area for each satellite.

    Parameters
    ----------
    number_of_satellites : int
        Number of satellites in the contellation being simulated.
    params : dict
        Contains all simulation parameters.

    Returns
    -------
    distance : float
        The distance between the transmitter and reciever in km.
    satellite_coverage_area_km : float
        The area which each satellite covers on Earth's surface in km.

    """
    area_of_earth_covered = params['total_area_earth_km_sq']

    network_density = number_of_satellites / area_of_earth_covered

    satellite_coverage_area_km = (area_of_earth_covered / number_of_satellites) #/ 1000

    mean_distance_between_assets = math.sqrt((1 / network_density)) / 2

    distance = math.sqrt(((mean_distance_between_assets)**2) + ((params['altitude_km'])**2))

    return distance, satellite_coverage_area_km


def calc_free_space_path_loss(distance, params, i, random_variations):
    """
    Calculate the free space path loss in decibels.

    FSPL(dB) = 20log(d) + 20log(f) + 32.44

    Where distance (d) is in km and frequency (f) is MHz.

    Parameters
    ----------
    distance : float
        Distance between transmitter and receiver in metres.
    params : dict
        Contains all simulation parameters.
    i : int
        Iteration number.
    random_variation : list
        List of random variation components.

    Returns
    -------
    path_loss : float
        The free space path loss over the given distance.
    random_variation : float
        Stochastic component.
    """
    frequency_MHz = params['dl_frequency'] / 1e6

    path_loss = 20*math.log10(distance) + 20*math.log10(frequency_MHz) + 32.44

    random_variation = random_variations[i]

    return path_loss + random_variation, random_variation


def generate_log_normal_dist_value(frequency, mu, sigma, seed_value, draws):
    """
    Generates random values using a lognormal distribution, given a specific mean (mu)
    and standard deviation (sigma).

    Original function in pysim5G/path_loss.py.

    The parameters mu and sigma in np.random.lognormal are not the mean and STD of the
    lognormal distribution. They are the mean and STD of the underlying normal distribution.

    Parameters
    ----------
    frequency : float
        Carrier frequency value in Hertz.
    mu : int
        Mean of the desired distribution.
    sigma : int
        Standard deviation of the desired distribution.
    seed_value : int
        Starting point for pseudo-random number generator.
    draws : int
        Number of required values.

    Returns
    -------
    random_variation : float
        Mean of the random variation over the specified itations.

    """
    if seed_value == None:
        pass
    else:
        frequency_seed_value = seed_value * frequency * 100
        np.random.seed(int(str(frequency_seed_value)[:2]))

    normal_std = np.sqrt(np.log10(1 + (sigma/mu)**2))
    normal_mean = np.log10(mu) - normal_std**2 / 2

    random_variation  = np.random.lognormal(normal_mean, normal_std, draws)

    return random_variation


def calc_antenna_gain(c, d, f, n):
    """
    Calculates the antenna gain.

    Parameters
    ----------
    c : float
        Speed of light in meters per second (m/s).
    d : float
        Antenna diameter in meters.
    f : int
        Carrier frequency in Hertz.
    n : float
        Antenna efficiency.

    Returns
    -------
    antenna_gain : float
        Antenna gain in dB.

    """
    #Define signal wavelength
    lambda_wavelength = c / f

    #Calculate antenna_gain
    antenna_gain = 10 * (math.log10(n*((np.pi*d) / lambda_wavelength)**2))

    return antenna_gain


def calc_eirp(power, antenna_gain):
    """
    Calculate the Equivalent Isotropically Radiated Power.

    Equivalent Isotropically Radiated Power (EIRP) = (
        Power + Gain
    )

    Parameters
    ----------
    power : float
        Transmitter power in watts.
    antenna_gain : float
        Antenna gain in dB.
    losses : float
        Antenna losses in dB.

    Returns
    -------
    eirp : float
        eirp in dB.

    """
    eirp = power + antenna_gain

    return eirp


def calc_losses(earth_atmospheric_losses, all_other_losses):
    """
    Estimates the transmission signal losses.

    Parameters
    ----------
    earth_atmospheric_losses : int
        Signal losses from rain attenuation.
    all_other_losses : float
        All other signal losses.

    Returns
    -------
    losses : float
        The estimated transmission signal losses.

    """
    losses = earth_atmospheric_losses + all_other_losses

    return losses


def calc_received_power(eirp, path_loss, receiver_gain, losses):
    """
    Calculates the power received at the User Equipment (UE).

    Parameters
    ----------
    eirp : float
        The Equivalent Isotropically Radiated Power in dB.
    path_loss : float
        The free space path loss over the given distance.
    receiver_gain : float
        Antenna gain at the receiver.
    losses : float
        Transmission signal losses.

    Returns
    -------
    received_power : float
        The received power at the receiver in dB.

    """
    received_power = eirp + receiver_gain - path_loss - losses

    return received_power


def calc_noise():
    """
    Estimates the potential noise.

    Terminal noise can be calculated as:

    “K (Boltzmann constant) x T (290K) x bandwidth”.

    The bandwidth depends on bit rate, which defines the number
    of resource blocks. We assume 50 resource blocks, equal 9 MHz,
    transmission for 1 Mbps downlink.

    Required SNR (dB)
    Detection bandwidth (BW) (Hz)
    k = Boltzmann constant
    T = Temperature (Kelvins) (290 Kelvin = ~16 degrees celcius)
    NF = Receiver noise figure (dB)

    NoiseFloor (dBm) = 10log10(k * T * 1000) + NF + 10log10BW

    NoiseFloor (dBm) = (
        10log10(1.38 x 10e-23 * 290 * 1x10e3) + 1.5 + 10log10(10 x 10e6)
    )

    Parameters
    ----------
    bandwidth : int
        The bandwidth of the carrier frequency (MHz).

    Returns
    -------
    noise : float
        Received noise at the UE receiver in dB.

    """
    k = 1.38e-23 #Boltzmann's constant k = 1.38×10−23 joules per kelvin
    t = 290 #Temperature of the receiver system T0 in kelvins
    b = 0.25 #Detection bandwidth (BW) in Hz

    noise = (10*(math.log10((k*t*1000)))) + (10*(math.log10(b*10**9)))

    return noise


def calc_cnr(received_power, noise):
    """
    Calculate the Carrier-to-Noise Ratio (CNR).

    Returns
    -------
    received_power : float
        The received signal power at the receiver in dB.
    noise : float
        Received noise at the UE receiver in dB.

    Returns
    -------
    cnr : float
        Carrier-to-Noise Ratio (CNR) in dB.

    """
    cnr = received_power - noise

    return cnr


def calc_spectral_efficiency(cnr, lut):
    """
    Given a cnr, find the spectral efficiency.

    Parameters
    ----------
    cnr : float
        Carrier-to-Noise Ratio (CNR) in dB.
    lut : list of tuples
        Lookup table for CNR to spectral efficiency.

    Returns
    -------
    spectral_efficiency : float
        The number of bits per Hertz able to be transmitted.

    """
    for lower, upper in pairwise(lut):

        lower_cnr, lower_se  = lower
        upper_cnr, upper_se  = upper

        if cnr >= lower_cnr and cnr < upper_cnr:
            spectral_efficiency = lower_se
            return spectral_efficiency

        highest_value = lut[-1]

        if cnr >= highest_value[0]:
            spectral_efficiency = highest_value[1]
            return spectral_efficiency

        lowest_value = lut[0]

        if cnr < lowest_value[0]:
            spectral_efficiency = lowest_value[1]
            return spectral_efficiency


def calc_capacity(spectral_efficiency, dl_bandwidth):
    """
    Calculate the channel capacity.

    Parameters
    ----------
    spectral_efficiency : float
        The number of bits per Hertz able to be transmitted.
    dl_bandwidth: float
        The channel bandwidth in Hetz.

    Returns
    -------
    channel_capacity : float
        The channel capacity in Mbps.

    """
    channel_capacity = spectral_efficiency * dl_bandwidth / (10**6)

    return channel_capacity


def single_satellite_capacity(dl_bandwidth, spectral_efficiency,
    number_of_channels, polarization):
    """
    Calculate the capacity of each satellite.

    Parameters
    ----------
    dl_bandwidth :
        Bandwidth in MHz.
    spectral_efficiency :
        Spectral efficiency 64QAM equivalent to 5.1152, assuming every constellation uses 64QAM
    number_of_channels :
        ...
    number_of_channels :
        ...

    Returns
    -------
    sat_capacity : ...
        Satellite capacity.

    """
    sat_capacity = (dl_bandwidth/1000000)*spectral_efficiency*number_of_channels*polarization

    return sat_capacity

def calc_agg_capacity(channel_capacity, number_of_channels, polarization):
    """
    Calculate the aggregate capacity.

    Parameters
    ----------
    channel_capacity : float
        The channel capacity in Mbps.
    number_of_channels : int
        The number of user channels per satellite.

    Returns
    -------
    agg_capacity : float
        The aggregate capacity in Mbps.

    """
    agg_capacity = channel_capacity * number_of_channels * polarization

    return agg_capacity


def single_satellite_capacity(dl_bandwidth, spectral_efficiency, number_of_channels,polarization):
    """
    Calculate the capacity by each satellite

    Parameters
    ----------
    dl_bandwidth : float
        Bandwidth in MHz.
    spectra_efficiency : float
        Spectral efficiency 64QAM equivalent to 5.1152.
    number_of_channels : int
        Number of channels for each constellation.
    polarization : int
        Number of polarizations.

    Returns
    -------
    sat_capacity : float
        Capacity of a single satellite.

    """
    sat_capacity = (dl_bandwidth/1000000)*spectral_efficiency*number_of_channels*polarization

    return sat_capacity

def pairwise(iterable):
    """
    Return iterable of 2-tuples in a sliding window.

    Parameters
    ----------
    iterable: list
        Sliding window

    Returns
    -------
    list of tuple
        Iterable of 2-tuples

    Example
    -------
    >>> list(pairwise([1,2,3,4]))
        [(1,2),(2,3),(3,4)]

    """
    a, b = tee(iterable)
    next(b, None)

    return zip(a, b)


def soyuz_fg(hypergolic, kerosene):
    """
    Calculate the emissions of the 6 compounds for Soyuz FG rocket vehicle.

    Parameters
    ----------
    hypergolic : float
        Hypergolic fuel used by the rocket in kilograms.
    kerosene : float
        Kerosene fuel used by the rocket in kilograms.
    
    Returns
    -------
    my_dict : dict
        A dict containing all estimated emissions.

    """
    emissions_dict = {}

    emissions_dict['alumina_emission'] = (hypergolic*1*0.001) + (kerosene*1*0.05)

    emissions_dict['sulphur_emission'] = (hypergolic*0.7*0.001) + (kerosene*0.7*0.001)

    emissions_dict['carbon_emission'] = (hypergolic*0.252*1) + (kerosene*0.352*1)

    emissions_dict['cfc_gases'] = (hypergolic*0.016*0.7) + (kerosene*0.016*0.7) \
                                  + (hypergolic*0.003*0.7) + (kerosene*0.003*0.7) \
                                  + (hypergolic*0.001*0.7) + (kerosene*0.001*0.7)

    emissions_dict['particulate_matter'] = (hypergolic*0.001*0.22) + (kerosene *0.001*0.22) \
                                           + (hypergolic*0.001*1) + (kerosene*0.05*1)

    emissions_dict['photo_oxidation'] = (hypergolic*0.378*0.0456) + (kerosene *0.528*0.0456) \
                                        + (hypergolic*0.001*1) + (kerosene*0.001*1)

    return emissions_dict


def falcon_9(kerosene):
    """
    calculate the emissions of the 6 compounds for Falcon 9 rocket vehicle.

    Parameters
    ----------
    kerosene: float
        Kerosene fuel used by the rocket in kilograms.
    
    Returns
    -------
    alumina_emission, sulphur_emission, carbon_emission, cfc,gases,
        particulate_matter, photo_oxidation: list.

    """
    emission_dict = {}

    emission_dict['alumina_emission'] = (kerosene*0.05)
    
    emission_dict['sulphur_emission'] = (kerosene*0.001*0.7)
    
    emission_dict['carbon_emission'] = (kerosene*0.352*1)

    emission_dict['cfc_gases'] = (kerosene*0.016*0.7) + (kerosene*0.003*0.7) \
                                 + (kerosene*0.001*0.7)

    emission_dict['particulate_matter'] = (kerosene*0.001*0.22) + (kerosene*0.05*1)

    emission_dict['photo_oxidation'] = (kerosene*0.0456*0.528) + (kerosene*0.001*1)

    return emission_dict


def falcon_heavy(kerosene):
    """
    calculate the emissions of the 6 compounds for Falcon Heavy rocket vehicle.

    Parameters
    ----------
    kerosene: float
        Kerosene fuel used by the rocket in kilograms.
    
    Returns
    -------
    alumina_emission, sulphur_emission, carbon_emission, cfc,gases,
        particulate_matter, photo_oxidation: list.

    """
    emission_dict = {} 

    emission_dict['alumina_emission'] = kerosene*0.05
   
    emission_dict['sulphur_emission'] = (kerosene*0.001*0.7)
    
    emission_dict['carbon_emission'] = (kerosene*0.352*1)

    emission_dict['cfc_gases'] = (kerosene*0.016*0.7) + (kerosene*0.003*0.7) \
                                 + (kerosene*0.001*0.7)

    emission_dict['particulate_matter'] = (kerosene*0.001*0.22) + (kerosene*0.05*1)

    emission_dict['photo_oxidation'] = (kerosene*0.0456*0.528) + (kerosene*0.001*1)

    return emission_dict


def ariane(hypergolic, solid, cryogenic):
    """
    calculate the emissions of the 6 compounds for Ariane 5 space.

    Parameters
    ----------
    hypergolic: float
        Hypergolic fuel used by the rocket in kilograms.
    solid: float
        solid fuel used by the rocket in kilograms.
    cryogenic: float
        cryogenic fuel used by the rocket in kilograms.
    
    Returns
    -------
    alumina_emission, sulphur_emission, carbon_emission, cfc,gases,
        particulate_matter, photo_oxidation: list.

    """
    emission_dict = {}

    emission_dict['alumina_emission'] = (solid*0.33*1) + (hypergolic*0.001*1)

    emission_dict['sulphur_emission'] = (solid*0.005*0.7) + (cryogenic*0.001*0.7) \
                                        + (hypergolic*0.001*0.7)+(solid*0.15*0.88)

    emission_dict['carbon_emission'] = (solid*0.108*1) + (hypergolic*0.252)

    emission_dict['cfc_gases'] = (solid*0.08*0.7) + (cryogenic*0.016*0.7) \
                                 + (hypergolic*0.016*0.7) + (solid*0.015*0.7) \
                                 + (cryogenic*0.003*0.7) + (hypergolic*0.003*0.7) \
                                 + (solid*0.005*0.7) + (cryogenic*0.001*0.7) \
                                 + (hypergolic*0.001*0.7) + (solid*0.15*0.7)

    emission_dict['particulate_matter'] = (solid*0.005*0.22) + (cryogenic*0.001*0.22) \
                                          + (hypergolic*0.001*0.22) + (solid*0.33*1) \
                                          + (hypergolic*0.001*1)

    emission_dict['photo_oxidation'] = (solid*0.162*0.0456) + (hypergolic*0.378*0.0456) \
                                       + (solid*0.005*1) + (cryogenic*0.001*1) \
                                       + (hypergolic*0.001*1)

    return emission_dict


def calc_per_sat_emission(name, fuel_mass, fuel_mass_1, fuel_mass_2, fuel_mass_3):
    """
    calculate the emissions of the 6 compounds for each of the satellites 
    of the three constellations based on the rocket vehicle used.

    Parameters
    ----------
    name: string
        Name of the constellation.
    fuel_mass: int
        mass of kerosene used by the rockets in kilograms.
    fuel_mass_1: int
        mass of hypergolic fuel used by the rockets in kilograms.
    fuel_mass_2: int
        mass of solid fuel used by the rockets in kilogram.
    fuel_mass_3: int
        mass of cryogenic fuel used by the rockets in kilogram.
    
    Returns
    -------
    al, sul, cb, cfc, pm, phc: dict.
    """

    if name == 'Starlink':
        emission_dict = falcon_9(fuel_mass)  # Emission per satellite

    elif name == 'Kuiper':
        fm_hyp, fm_sod, fm_cry = fuel_mass_1, fuel_mass_2, fuel_mass_3   
        emission_dict = ariane(fm_hyp, fm_sod, fm_cry)

    elif name == 'OneWeb':
        fm_hyp, fm_ker = fuel_mass_1, fuel_mass_2
        emission_dict = soyuz_fg(fm_hyp, fm_ker)

    else:
        print('Invalid Constellation name')

    return emission_dict


def pairwise(iterable):
    """
    Return iterable of 2-tuples in a sliding window.

    Parameters
    ----------
    iterable: list
        Sliding window

    Returns
    -------
    list of tuple
        Iterable of 2-tuples

    Example
    -------
    >>> list(pairwise([1,2,3,4]))
        [(1,2),(2,3),(3,4)]

    """
    a, b = tee(iterable)
    next(b, None)

    return zip(a, b)
