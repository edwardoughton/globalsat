import datetime
from scipy.stats import norm
import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord
import astropy.time as astrotime
from scipy.spatial.transform import Rotation
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from sgp4.propagation import _gstime
from sgp4.ext import jday

"""

SatModel: Satellite data structure
- input: TLE data
- output: data structure

physical_quantity
- input: date and time
- output: (x,y,z) position in km, (Vx,Vy,Vz) velocity in km per sec, and time.
-- cooridination is TEME (True equator and mean equinox of date)
-- (before 2009-01-01) SGP4 prediction based on TLE data on 2009 Jan 01
-- (from 2009-01-01 to 2019-08-19) SGP4
-- (after 2019-08-19) SGP4 prediction based on TLE data on 2019 Aug 19

example

> tmpsat = SatModel(TLEdatum)
> tmpsatPosVelTime = tmpsat.physical_quantity(dumtime)
> SunPos = get_sun(astrotime.Time(dumtime))

Then, compare SunPos with tmpsatPosVelTime['pos_itrs'].gcrs

"""
class SatModel:
    def __init__(self, TLEData):
        with open(TLEData, 'r') as f:
            self.TLELines = f.readlines()

        ObsDatetimeList = []
        self.ModelList = []
        for i in range(0, len(self.TLELines), 2):
            tmpModel = twoline2rv(self.TLELines[i], self.TLELines[i+1], wgs72)
            self.ModelList.append(tmpModel)
            ObsDatetimeList.append(tmpModel.epoch)

        self.ObsDatetimeDf = pd.to_datetime(ObsDatetimeList)
        self.satnum = tmpModel.satnum
        self.DatetimeTypes = (
                astrotime,
                datetime.datetime,
                pd.Timestamp)

    def physical_quantity(self, Datetime):
        if type(Datetime) not in self.DatetimeTypes:
            return print(
                'The type of arg should be\n\
                astropy.time or\n\
                datetime.datetime or\n\
                pd.Timestamp')

        ObsIndex = abs(self.ObsDatetimeDf - Datetime).argmin()
        tmpModel = self.ModelList[ObsIndex]
        pos_teme, vel_teme = tmpModel.propagate(
                Datetime.year, Datetime.month, Datetime.day,
                Datetime.hour, Datetime.minute, Datetime.second)
        jd = jday(
                Datetime.year, Datetime.month, Datetime.day,
                Datetime.hour, Datetime.minute, Datetime.second)
        thGMST = _gstime(jd)
        rot3 = Rotation.from_euler('z', -thGMST, degrees=False)
        posX_itrs, posY_itrs, posZ_itrs = rot3.apply(pos_teme)
        pos_itrs = SkyCoord(
                x=posX_itrs, y=posY_itrs, z=posZ_itrs,
                frame='itrs', unit='km', representation_type='cartesian',
                obstime=Datetime)

        return {'time':Datetime,
                'pos_teme': pos_teme,
                'vel_teme': vel_teme,
                'pos_itrs': pos_itrs,
                }

"""
Fragility curve
F(a) = PHI(ln(a/Ce)/Ze)
- a: event severity
- Ce: free parameter 1
- Ze: free parameter 2
- PHI: standard normal cumulative distribution function

"""
def Frglty(a, Ce, Ze):
    return norm.cdf(np.log(a/Ce)/Ze)


"""
MEMO

RA angle: right ascension
DEC angle: declination
ITRS (International Terrestrial Reference System):
- x-axis: intersection btwn IERS reference meridian (Greenwich) and equator
- z-axis: referenced polar rotation axis
GCRS (Geocentric Celestial Reference System):
- x-axis: vernal equinox (J2000 FK5?)
- z-axis: perpendicular to Sun-Earth ecliptic plane

"""
