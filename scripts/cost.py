import numpy as np
import pandas as pd


def cost_model(satellite_launch_cost, ground_station_cost, spectrum_cost, regulation_fees, \
    digital_infrastructure_cost, ground_station_energy, subscriber_acquisition, \
    staff_costs, research_development, maintenance, discount_rate, assessment_period):
    """
    Calculate the total cost of ownership(TCO):

    Parameters
    ----------
    params : dict.
        Contains all simulation parameters.

    Returns
    -------
    results : float
            The total cost of ownership.

    """

    capex = satellite_launch_cost + ground_station_cost + spectrum_cost + regulation_fees \
            + digital_infrastructure_cost #Addition of all capital expenditure

    opex_costs = ground_station_energy + subscriber_acquisition + staff_costs \
                 + research_development + maintenance #Addition of all recurrent expenditures

    year_costs = []
    for time in np.arange(1, assessment_period):  #Discounted for the years
        yearly_opex = opex_costs/(((discount_rate/100) + 1)**time)
        year_costs.append(yearly_opex)

    total_cost_ownership = capex + sum(year_costs) + opex_costs

    return total_cost_ownership