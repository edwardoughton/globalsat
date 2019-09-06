import glob, datetime, requests, time
from scipy.stats import norm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord, get_sun
import astropy.time as astrotime
from scipy.spatial.transform import Rotation
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from sgp4.propagation import _gstime
from sgp4.ext import jday

# test on Starlink A
TLEList = glob.glob('*.tle')
with open(TLEList[1], 'r') as f: # tle_starlink_a.tle
    TLELines = f.readlines()

SlinkA = twoline2rv(TLELines[1], TLELines[2], wgs72)
SlinkAPos, SlinkAVel = SlinkA.propagate(2019, 8, 19, 0, 0, 0)

## retrieve LEO satellites information from satcat
Sat_df = pd.read_csv('satcat.csv', header=1)
LEOAltitude = 4000 # km
SatcatLEOSat_df = Sat_df[Sat_df.apogee < LEOAltitude]

# all LEO fleet at 2019 Aug 20 10:54UT
LEOTLE = './190820T1054_LEO-fleet.tle'
with open(LEOTLE, 'r') as f:
    TLELines = f.readlines()

LEOSats = []
LEOSatsPos = []
LEOSatsVel = []
LEOSatsId = []
for i in range(0, len(TLELines), 2):
    tmpLEOSat = twoline2rv(TLELines[i], TLELines[i+1], wgs72)
    LEOSatsId.append(tmpLEOSat.satnum)
    LEOSats.append(tmpLEOSat)

# # retrieve all LEO TLE data from 2009-01-01 to 2019-08-20
Datetime_df = pd.to_datetime(np.arange(
    '2009-01-01', '2019-08-20', dtype='datetime64[D]'))
#LEOUrl = 'https://www.space-track.org/basicspacedata/query/class/tle/EPOCH/'\
#    +Datetime_df[0].strftime('%Y-%m-%d')\
#    +'--'\
#    +Datetime_df[-1].strftime('%Y-%m-%d')\
#    +'/MEAN_MOTION/>11.25/ECCENTRICITY/<0.25/OBJECT_TYPE/payload/'\
#    +'orderby/NORAD_CAT_ID asc,EPOCH asc/format/tle'
for i in range(217,len(LEOSatsId)):
    print(i)
    LEOSatId = LEOSatsId[i]
    LEOUrl = 'https://www.space-track.org/basicspacedata/query/class/tle/EPOCH/'\
        +Datetime_df[0].strftime('%Y-%m-%d')\
        +'--'\
        +Datetime_df[-1].strftime('%Y-%m-%d')\
        +'/NORAD_CAT_ID/'+str(LEOSatId)+'/'\
        +'orderby/EPOCH asc/format/tle'
    IdPssQury = {
        'identity': ' ',
        'password': ' ',
        'query': LEOUrl
    }
    response = requests.post('https://www.space-track.org/ajaxauth/login', data=IdPssQury)

    with open('./tle/NORAD_{}.tle'.format(LEOSatId), 'w') as f:
        f.writelines(response.text.split('\r'))

    time.sleep(20)

# # plot all LEO sats at the same time
TestTime = datetime.datetime(2018, 8, 20)
for i, LEOSat in enumerate(LEOSats):
    if i % 100 == 0:
        print(i, len(LEOSats))

    tmpPos, tmpVel = LEOSat.propagate(
        TestTime.year, TestTime.month, TestTime.day,
        TestTime.hour, TestTime.minute, TestTime.second)
    LEOSatsPos.append(list(tmpPos))
    LEOSatsVel.append(list(tmpVel))

LEOSatsPosArray = np.array(LEOSatsPos)
LEOSatsVelArray = np.array(LEOSatsVel)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(
    LEOSatsPosArray[:,0],
    LEOSatsPosArray[:,1],
    LEOSatsPosArray[:,2],
    'o',s=5)
ax.set_xlim(-1e4,1e4)
ax.set_ylim(-1e4,1e4)
ax.set_zlim(-1e4,1e4)

# # plot the orbits of Starlink constellation
StarlinkIdArray = SatcatLEOSat_df.loc[
        SatcatLEOSat_df.name.str.contains('STARLINK')
        ]['NORAD_id'].values
Datetime_df = pd.to_datetime(np.arange(
        '2019-08-19', '2019-08-20', dtype='datetime64[m]'))
StarlinkSats = [[],[],[]] # id, name, model
for i, LEOSat in enumerate(LEOSats):
    LEOSatId = LEOSat.satnum
    if np.isin(StarlinkIdArray - LEOSatId, 0).sum():
        StarlinkSats[0].append(LEOSatId)
        StarlinkSats[1].append(
            SatcatLEOSat_df[
                SatcatLEOSat_df.NORAD_id == LEOSatId
                ].name.values[0]
            )
        StarlinkSats[2].append(LEOSat)

StarlinkTimePosVel = np.zeros((
    len(StarlinkSats[0]),
    len(Datetime_df),
    3,2))

for i, model in enumerate(StarlinkSats[2]):
    print(i)
    for j, utime in enumerate(Datetime_df):
        StarlinkTimePosVel[i,j,:,0], StarlinkTimePosVel[i,j,:,1] =\
            model.propagate(
                utime.year, utime.month, utime.day,
                utime.hour, utime.minute, utime.second)

fig = plt.figure(figsize=(6,6))
ax = fig.add_subplot(111, projection='3d')
k = 10
ax.plot(
    StarlinkTimePosVel[k,:,0,0],
    StarlinkTimePosVel[k,:,1,0],
    StarlinkTimePosVel[k,:,2,0],
    )
ax.scatter(
    StarlinkTimePosVel[k,::100,0,0],
    StarlinkTimePosVel[k,::100,1,0],
    StarlinkTimePosVel[k,::100,2,0],
    'o',s=5)
ax.set_xlim(-1e4,1e4)
ax.set_ylim(-1e4,1e4)
ax.set_zlim(-1e4,1e4)

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
