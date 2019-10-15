import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter
from lifelines import CoxTimeVaryingFitter
from scipy.interpolate import interp1d

"""
Cox analysis
"""
subCoxDf = CoxDf[['norad_id', 'event', 'start', 'stop', 'pr100', 'pr60_100']]
ctv = CoxTimeVaryingFitter()
ctv.fit(subCoxDf, id_col='norad_id', event_col='event',
        start_col='start', stop_col='stop', show_progress=True)
ctv.print_summary()
base_haz = pd.concat([
    ctv.baseline_cumulative_hazard_.iloc[0:1],
    ctv.baseline_cumulative_hazard_.diff().iloc[1:]])

fig = plt.figure()
ax = fig.add_subplot()
base_haz.plot(ax=ax)
ax.set_title(str(subtrgtEventsDf.loc[i]['Launch Date'])+' to the present')
ax.set_xlabel('day')
g_pr100 = interp1d(SbtrcttmpCoxDf['stop'], SbtrcttmpCoxDf['pr100'])
g_pr60_100 = interp1d(SbtrcttmpCoxDf['stop'], SbtrcttmpCoxDf['pr60_100'])
fluences_array = np.array([
    g_pr100(base_haz.index[:-1]),
    g_pr60_100(base_haz.index[:-1])]).T
haz = base_haz.iloc[:-1]*ctv.predict_partial_hazard(fluences_array).values
np.exp(-haz.cumsum()).plot(ax=ax) # survivability curve



"""
Cox time-varying fit
"""
StartCycle22 = pd.Timestamp(1986,1,1)
EndCycle22 = pd.Timestamp(1997,1,1)
StartCycle23 = pd.Timestamp(1997,1,1)
EndCycle23 = pd.Timestamp(2009,1,1)
StartCycleAll = pd.Timestamp(1986,1,1)
EndCycleAll = pd.Timestamp(2018,1,1)

StartCycle = StartCycleAll
EndCycle = EndCycleAll

# load events
EventsDf = pd.read_excel('./data/failure/seki10_events.xlsx')
EventsDf.sort_values(by='Catalogue Number', inplace=True)
trgtEventsDf = EventsDf[(EventsDf['Launch Date'] < EndCycle)&\
                        (EventsDf['Launch Date'] > StartCycle)]
subtrgtEventsDf = trgtEventsDf[['Catalogue Number', 'duration', 'event', 'Launch Date']]

# load covariate
elpr8600Df = pd.read_csv('./data/goes/elpr_1986-2000.csv', index_col=0)
elpr8600Df.index = pd.to_datetime(elpr8600Df.index)
elpr0110Df = pd.read_csv('./data/goes/elpr_2001-2010.csv', index_col=0)
elpr0110Df.index = pd.to_datetime(elpr0110Df.index)
el1118Df = pd.read_csv('./data/goes/el_2011-2018.csv', index_col=0)
el1118Df.index = pd.to_datetime(el1118Df.index)
pr1118Df = pd.read_csv('./data/goes/pr_2011-2018.csv', index_col=0)
pr1118Df.index = pd.to_datetime(pr1118Df.index)

# fluence
el2_8618Df = pd.concat([
    elpr8600Df.e2_flux_ic,
    elpr0110Df.e2_flux_ic,
    (el1118Df.E2E_COR_FLUX+el1118Df.E2W_COR_FLUX)*0.5
    ])*pd.Timedelta(1, unit='D').total_seconds()
el2_8618Df.dropna(inplace=True)

pr1_8618Df = pd.concat([
    elpr8600Df.p1_flux_ic,
    elpr0110Df.p1_flux_ic,
    (pr1118Df.ZPGT1E+pr1118Df.ZPGT1W)*0.5
    ])*pd.Timedelta(1, unit='D').total_seconds()
pr1_8618Df.dropna(inplace=True)

pr5_8618Df = pd.concat([
    elpr8600Df.p2_flux_ic,
    elpr0110Df.p2_flux_ic,
    (pr1118Df.ZPGT5E+pr1118Df.ZPGT5W)*0.5
    ])*pd.Timedelta(1, unit='D').total_seconds()
pr5_8618Df.dropna(inplace=True)

pr10_8618Df = pd.concat([
    elpr8600Df.p3_flux_ic,
    elpr0110Df.p3_flux_ic,
    (pr1118Df.ZPGT10E+pr1118Df.ZPGT10W)*0.5
    ])*pd.Timedelta(1, unit='D').total_seconds()
pr10_8618Df.dropna(inplace=True)

pr30_8618Df = pd.concat([
    elpr8600Df.p4_flux_ic,
    elpr0110Df.p4_flux_ic,
    (pr1118Df.ZPGT30E+pr1118Df.ZPGT30W)*0.5
    ])*pd.Timedelta(1, unit='D').total_seconds()
pr30_8618Df.dropna(inplace=True)

pr50_8618Df = pd.concat([
    elpr8600Df.p5_flux_ic,
    elpr0110Df.p5_flux_ic,
    (pr1118Df.ZPGT50E+pr1118Df.ZPGT50W)*0.5
    ])*pd.Timedelta(1, unit='D').total_seconds()
pr50_8618Df.dropna(inplace=True)

pr60_8618Df = pd.concat([
    elpr8600Df.p6_flux_ic,
    elpr0110Df.p6_flux_ic,
    (pr1118Df.ZPGT60E+pr1118Df.ZPGT60W)*0.5
    ])*pd.Timedelta(1, unit='D').total_seconds()
pr60_8618Df.dropna(inplace=True)

pr100_8618Df = pd.concat([
    elpr8600Df.p7_flux_ic,
    elpr0110Df.p7_flux_ic,
    (pr1118Df.ZPGT100E+pr1118Df.ZPGT100W)*0.5
    ])*pd.Timedelta(1, unit='D').total_seconds()
pr100_8618Df.dropna(inplace=True)

#el2_8618Df = (el2_8618Df - el2_8618Df.mean())/el2_8618Df.std()
#pr1_8618Df = (pr1_8618Df - pr1_8618Df.mean())/pr1_8618Df.std()
#pr5_8618Df = (pr5_8618Df - pr5_8618Df.mean())/pr5_8618Df.std()
#pr10_8618Df = (pr10_8618Df - pr10_8618Df.mean())/pr10_8618Df.std()
#pr30_8618Df = (pr30_8618Df - pr30_8618Df.mean())/pr30_8618Df.std()
#pr50_8618Df = (pr50_8618Df - pr50_8618Df.mean())/pr50_8618Df.std()
#pr60_8618Df = (pr60_8618Df - pr60_8618Df.mean())/pr60_8618Df.std()
#pr100_8618Df = (pr100_8618Df - pr100_8618Df.mean())/pr100_8618Df.std()

f_el2 = interp1d(
        (el2_8618Df.index-el2_8618Df.index[0]\
            ).values.astype('timedelta64[D]').astype('f'),
        el2_8618Df.values)
f_pr1 = interp1d(
        (pr1_8618Df.index-pr1_8618Df.index[0]\
            ).values.astype('timedelta64[D]').astype('f'),
        pr1_8618Df.values)
f_pr5 = interp1d(
        (pr5_8618Df.index-pr5_8618Df.index[0]\
            ).values.astype('timedelta64[D]').astype('f'),
        pr5_8618Df.values)
f_pr10 = interp1d(
        (pr10_8618Df.index-pr10_8618Df.index[0]\
            ).values.astype('timedelta64[D]').astype('f'),
        pr10_8618Df.values)
f_pr30 = interp1d(
        (pr30_8618Df.index-pr30_8618Df.index[0]\
            ).values.astype('timedelta64[D]').astype('f'),
        pr30_8618Df.values)
f_pr50 = interp1d(
        (pr50_8618Df.index-pr50_8618Df.index[0]\
            ).values.astype('timedelta64[D]').astype('f'),
        pr50_8618Df.values)
f_pr60 = interp1d(
        (pr60_8618Df.index-pr60_8618Df.index[0]\
            ).values.astype('timedelta64[D]').astype('f'),
        pr60_8618Df.values)
f_pr100 = interp1d(
        (pr100_8618Df.index-pr100_8618Df.index[0]\
            ).values.astype('timedelta64[D]').astype('f'),
        pr100_8618Df.values)


fluence_start = el2_8618Df.index[0]

# make time table
dT = pd.Timedelta('1 days')
YtoD = pd.Timedelta('1 y').total_seconds()/pd.Timedelta('1 day').total_seconds()
subtrgtEventsDf['Event_Date'] = subtrgtEventsDf['Launch Date'] +\
        pd.to_timedelta(subtrgtEventsDf['duration'], unit='Y')
whereCensor = np.where(subtrgtEventsDf['Event_Date'] > pd.Timestamp(2018,12,31))[0]
subtrgtEventsDf.iloc[whereCensor,[-1]] = pd.Timestamp(2018,12,31)
subtrgtEventsDf.iloc[whereCensor,[-4]] =\
        (subtrgtEventsDf['Event_Date']-subtrgtEventsDf['Launch Date']
            ).iloc[whereCensor].astype('timedelta64[s]')/24/3600/YtoD

#Columns = ['norad_id', 'start','stop',
#        'el2','pr1','pr5','pr10','pr30',
#        'pr50','pr60', 'pr100',
#        'event']
Columns = ['norad_id', 'start','stop',
        'el2','pr1_5','pr5_10','pr10_30','pr30_50',
        'pr50_60','pr60_100', 'pr100',
        'event']
CoxDf = pd.DataFrame(columns=Columns, data=np.zeros((1,len(Columns))), index=['nan'])
for i in subtrgtEventsDf.index:
    print(i, subtrgtEventsDf.index[-1])
    LaunchDuration = (subtrgtEventsDf.loc[i]['Launch Date'] - fluence_start
            ).total_seconds()/pd.Timedelta('1 day').total_seconds()
    EventDuration = (subtrgtEventsDf.loc[i]['Event_Date'] - fluence_start
            ).total_seconds()/pd.Timedelta('1 day').total_seconds()
    ReferDuration = np.arange(LaunchDuration, EventDuration, 1)
    StartStops = np.arange(LaunchDuration, EventDuration, dT.days)
    tmpCoxDf = pd.DataFrame(columns=['start'], data=StartStops)
    el2_cumsum = np.cumsum(f_el2(ReferDuration))
    pr1_cumsum = np.cumsum(f_pr1(ReferDuration))
    pr5_cumsum = np.cumsum(f_pr5(ReferDuration))
    pr10_cumsum = np.cumsum(f_pr10(ReferDuration))
    pr30_cumsum = np.cumsum(f_pr30(ReferDuration))
    pr50_cumsum = np.cumsum(f_pr50(ReferDuration))
    pr60_cumsum = np.cumsum(f_pr60(ReferDuration))
    pr100_cumsum = np.cumsum(f_pr100(ReferDuration))
    tmpCoxDf = tmpCoxDf.assign(
        norad_id = subtrgtEventsDf.loc[i]['Catalogue Number'],
        stop = np.append(StartStops[1:], EventDuration),
        el2 = np.append(el2_cumsum[dT.days::dT.days], el2_cumsum[-1]),
        pr1 = np.append(pr1_cumsum[dT.days::dT.days], pr1_cumsum[-1]),
        pr5 = np.append(pr5_cumsum[dT.days::dT.days], pr5_cumsum[-1]),
        pr10 = np.append(pr10_cumsum[dT.days::dT.days], pr10_cumsum[-1]),
        pr30 = np.append(pr30_cumsum[dT.days::dT.days], pr30_cumsum[-1]),
        pr50 = np.append(pr50_cumsum[dT.days::dT.days], pr50_cumsum[-1]),
        pr60 = np.append(pr60_cumsum[dT.days::dT.days], pr60_cumsum[-1]),
        pr100 = np.append(pr100_cumsum[dT.days::dT.days], pr100_cumsum[-1]),
        event = 0
        )
    tmpCoxDf.iloc[-1, -1] = subtrgtEventsDf.loc[i]['event']
    tmpCoxDf[['start', 'stop']] -= LaunchDuration

    SbtrcttmpCoxDf = tmpCoxDf[['norad_id', 'start', 'stop', 'event']]
    SbtrcttmpCoxDf = SbtrcttmpCoxDf.assign(
        el2 = tmpCoxDf.el2,
        pr1_5 = tmpCoxDf.pr1 - tmpCoxDf.pr5,
        pr5_10 = tmpCoxDf.pr5 - tmpCoxDf.pr10,
        pr10_30 = tmpCoxDf.pr10 - tmpCoxDf.pr30,
        pr30_50 = tmpCoxDf.pr30 - tmpCoxDf.pr50,
        pr50_60 = tmpCoxDf.pr50 - tmpCoxDf.pr60,
        pr60_100 = tmpCoxDf.pr60 - tmpCoxDf.pr100,
        pr100 = tmpCoxDf.pr100
        )

#    tmpCoxDf[['el2', 'pr1', 'pr5', 'pr10',
#        'pr30','pr50', 'pr60', 'pr100']] =\
#        np.log10(tmpCoxDf[['el2', 'pr1', 'pr5', 'pr10',
#            'pr30','pr50', 'pr60', 'pr100']])
#    CoxDf = pd.concat([CoxDf, tmpCoxDf], axis=0)
    SbtrcttmpCoxDf[['el2', 'pr1_5', 'pr5_10', 'pr10_30',
        'pr30_50','pr50_60', 'pr60_100', 'pr100']] =\
        np.log10(SbtrcttmpCoxDf[['el2', 'pr1_5', 'pr5_10', 'pr10_30',
            'pr30_50','pr50_60', 'pr60_100', 'pr100']])
    CoxDf = pd.concat([CoxDf, SbtrcttmpCoxDf], axis=0)

CoxDf.drop('nan', axis=0, inplace=True)
CoxDf.dropna(inplace=True)
#CoxDf.to_csv('log_1d_all_CoxDf.csv')

subCoxDf = CoxDf[['norad_id', 'event', 'start', 'stop', 'pr100']]
ctv = CoxTimeVaryingFitter()
ctv.fit(subCoxDf, id_col='norad_id', event_col='event',
        start_col='start', stop_col='stop', show_progress=True)
ctv.print_summary()


"""
proton & electron data downloading
"""
# run ../../../plt_elpr.py 2001-01-01T00:00 2010-12-31T23:59 e2_flux_ic
wndw = int(24*(60/5))
elprDavgDf = elpr_df.rolling(wndw, min_periods=1).mean()[wndw-1::wndw]
elprDavgDf.index = elprDavgDf.index.values.astype('datetime64[D]')
elprDavgDf.to_csv('elpr_1986-2000.csv')
# There is somtimes a gap.
# 2015-05-03 23:45:00.000
# 2015-05-03 23:50:00.000
# 2015-05-03 23:55:00.000
# 2015-05-05 00:00:00.000
# 2015-05-05 00:05:00.000



"""
KM fit
"""
EventsDf = pd.read_excel('./data/failure/caster09_events.xlsx')
KMDf = EventsDf[['Catalogue Number', 'duration', 'event']]
kmf = KaplanMeierFitter()
kmf.fit(KMDf.duration, event_observed=KMDf.event)
fig = plt.figure()
ax = fig.add_subplot()
kmf.plot(ax=ax)

