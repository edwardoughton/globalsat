"""
Risk analysis module.

"""


def assess_risk(system, scenario):

    if scenario == 'baseline':

        for asset in system.assets.values():

            asset = asset.exposure +
