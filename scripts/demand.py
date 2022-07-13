def demand_model(monthly_traffic_GB, percent_of_traffic):
    """
    Calculate the demand density per area (Mbps/km2):

    Parameters
    ----------
    params : dict.
        Contains all simulation parameters.

    Returns
    -------
    results : float
            demand density_mbps_sqkm.

    """
    area_km = 1
    adoption_rate = 0.1
    population_density = 5
    active_users_per_sqkm = population_density * (adoption_rate / 100)
    hourly_MB = (monthly_traffic_GB / 30) * 1000 * percent_of_traffic
    hourly_mbps = hourly_MB * (8 / 3600)
    hourly_active_user_density = (active_users_per_sqkm * percent_of_traffic) / area_km
    demand_density_mbps_sqkm = hourly_active_user_density / hourly_mbps

    return demand_density_mbps_sqkm
