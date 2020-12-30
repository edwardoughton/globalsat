import pytest
from globalsat.sim import antenna_gain


def test_antenna_gain():

    d = 0.7 #float(input("Enter Antenna Diameter in metres: "))
    f = 13.5 #float(input("Enter the signal frequency in GHz: "))
    n = 0.6 #float(input("Enter the Antenna Efficiency: "))'''
    # GT=37.7

    #100 dollars for the whole market
    assert antenna_gain(d, f, n) == 37.7
