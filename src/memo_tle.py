import glob, datetime, requests, time
from scipy.stats import norm
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np
from astropy.coordinates import SkyCoord, get_sun
import astropy.time as astrotime
from sgp4.earth_gravity import wgs72
from sgp4.io import twoline2rv
from sgp4.propagation import _gstime
from sgp4.ext import jday

# test on Starlink A
#TLEList = glob.glob('*.tle')
#with open(TLEList[1], 'r') as f: # tle_starlink_a.tle
#    TLELines = f.readlines()
#
#SlinkA = twoline2rv(TLELines[1], TLELines[2], wgs72)
#SlinkAPos, SlinkAVel = SlinkA.propagate(2019, 8, 19, 0, 0, 0)

## retrieve LEO satellites information from satcat
#Sat_df = pd.read_csv('satcat.csv', header=1)
#LEOAltitude = 4000 # km
#SatcatLEOSat_df = Sat_df[Sat_df.apogee < LEOAltitude]

# all LEO, MEO, and GEO fleet
LEOTLE = './190820T1054_LEO-fleet.tle'
GEOTLE = './190906T1630_GEO-fleet.tle'
MEOTLE = './190906T1630_MEO-fleet.tle'
with open(GEOTLE, 'r') as f:
    TLELines = f.readlines()

LEOSats = []
LEOSatsPos = []
LEOSatsVel = []
LEOSatsId = []
for i in range(0, len(TLELines), 2):
    tmpLEOSat = twoline2rv(TLELines[i], TLELines[i+1], wgs72)
    LEOSatsId.append(tmpLEOSat.satnum)
    LEOSats.append(tmpLEOSat)

# # retrieve all LEO TLE data for 33 years
Datetime_df = pd.to_datetime(np.arange(
    '1986-01-01', '2019-09-06', dtype='datetime64[D]'))
#LEOUrl = 'https://www.space-track.org/basicspacedata/query/class/tle/EPOCH/'\
#    +Datetime_df[0].strftime('%Y-%m-%d')\
#    +'--'\
#    +Datetime_df[-1].strftime('%Y-%m-%d')\
#    +'/MEAN_MOTION/>11.25/ECCENTRICITY/<0.25/OBJECT_TYPE/payload/'\
#    +'orderby/NORAD_CAT_ID asc,EPOCH asc/format/tle'
for i in range(0,len(LEOSatsId)):
    print(i, len(LEOSatsId))
    LEOSatId = LEOSatsId[i]
    LEOUrl = 'https://www.space-track.org/basicspacedata/query/class/tle/EPOCH/'\
        +Datetime_df[0].strftime('%Y-%m-%d')\
        +'--'\
        +Datetime_df[-1].strftime('%Y-%m-%d')\
        +'/NORAD_CAT_ID/'+str(LEOSatId)+'/'\
        +'orderby/EPOCH asc/format/tle'
    IdPssQury = {
        'identity': 'seki@kwasan.kyoto-u.ac.jp',
        'password': 'tepWag-zehryw-rizcy8',
        'query': LEOUrl
    }
    response = requests.post('https://www.space-track.org/ajaxauth/login', data=IdPssQury)

    with open('./tle/NORAD_{:05}.tle'.format(LEOSatId), 'w') as f:
        f.writelines(response.text.split('\r'))

    time.sleep(20)

# # plot all LEO sats at the same time
#TestTime = datetime.datetime(2018, 8, 20)
#for i, LEOSat in enumerate(LEOSats):
#    if i % 100 == 0:
#        print(i, len(LEOSats))
#
#    tmpPos, tmpVel = LEOSat.propagate(
#        TestTime.year, TestTime.month, TestTime.day,
#        TestTime.hour, TestTime.minute, TestTime.second)
#    LEOSatsPos.append(list(tmpPos))
#    LEOSatsVel.append(list(tmpVel))
#
#LEOSatsPosArray = np.array(LEOSatsPos)
#LEOSatsVelArray = np.array(LEOSatsVel)
#
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.scatter(
#    LEOSatsPosArray[:,0],
#    LEOSatsPosArray[:,1],
#    LEOSatsPosArray[:,2],
#    'o',s=5)
#ax.set_xlim(-1e4,1e4)
#ax.set_ylim(-1e4,1e4)
#ax.set_zlim(-1e4,1e4)

# # plot the orbits of Starlink constellation
#StarlinkIdArray = SatcatLEOSat_df.loc[
#        SatcatLEOSat_df.name.str.contains('STARLINK')
#        ]['NORAD_id'].values
#Datetime_df = pd.to_datetime(np.arange(
#        '2019-08-19', '2019-08-20', dtype='datetime64[m]'))
#StarlinkSats = [[],[],[]] # id, name, model
#for i, LEOSat in enumerate(LEOSats):
#    LEOSatId = LEOSat.satnum
#    if np.isin(StarlinkIdArray - LEOSatId, 0).sum():
#        StarlinkSats[0].append(LEOSatId)
#        StarlinkSats[1].append(
#            SatcatLEOSat_df[
#                SatcatLEOSat_df.NORAD_id == LEOSatId
#                ].name.values[0]
#            )
#        StarlinkSats[2].append(LEOSat)
#
#StarlinkTimePosVel = np.zeros((
#    len(StarlinkSats[0]),
#    len(Datetime_df),
#    3,2))
#
#for i, model in enumerate(StarlinkSats[2]):
#    print(i)
#    for j, utime in enumerate(Datetime_df):
#        StarlinkTimePosVel[i,j,:,0], StarlinkTimePosVel[i,j,:,1] =\
#            model.propagate(
#                utime.year, utime.month, utime.day,
#                utime.hour, utime.minute, utime.second)
#
#fig = plt.figure(figsize=(6,6))
#ax = fig.add_subplot(111, projection='3d')
#k = 10
#ax.plot(
#    StarlinkTimePosVel[k,:,0,0],
#    StarlinkTimePosVel[k,:,1,0],
#    StarlinkTimePosVel[k,:,2,0],
#    )
#ax.scatter(
#    StarlinkTimePosVel[k,::100,0,0],
#    StarlinkTimePosVel[k,::100,1,0],
#    StarlinkTimePosVel[k,::100,2,0],
#    'o',s=5)
#ax.set_xlim(-1e4,1e4)
#ax.set_ylim(-1e4,1e4)
#ax.set_zlim(-1e4,1e4)
#
