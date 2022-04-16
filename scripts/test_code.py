from unittest import result
import emission_model as em
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
from matplotlib import pyplot
from globalsat.sim import single_satellite_capacity
path = '/home/makavelli/Desktop/GitHub/globalsat/results/'
pd.set_option('mode.chained_assignment', None)

#Cpacity per single satellite
starlink_capacity = single_satellite_capacity(250*10**6,5.1152,8,2)

kuiper_capacity = single_satellite_capacity(250*10**6, 5.1152, 8, 2)

oneweb_capacity = single_satellite_capacity(250*10**6, 5.1152, 8, 2)
print(oneweb_capacity)

#Emission model test
df = em.starlink_emission()
df1 = em.oneweb_emission()
df2 = em.kuiper_emission()

frames = [df, df1, df2]
results = pd.concat(frames)

#Emissions per Mbps
results['Emissions per Mbps'] = ""
for i in range(len(results)):
    try:
        if ([results['Constellation'] == 'starlink']):
            results['Emissions per Mbps'].loc[i] = results['amount'].loc[i] / \
                starlink_capacity
        elif [results['Constellation'] == 'kuiper']:
            results['Emissions per Mbps'].loc[i] = results['amount'].loc[i]/kuiper_capacity
        elif [results['Constellation'] == 'oneweb']:
            results['Emissions per Mbps'].loc[i] = results['amount'].loc[i]/oneweb_capacity
        else:
            pass
        results.to_csv(path+'constellation_emission_results.csv')
    except:
        pass 

#Plotting sample data
palette = sns.color_palette("Paired")
a4_dims = (12, 5)
sns.set_style('darkgrid')
fig, ax = pyplot.subplots(figsize=a4_dims)
ax = sns.barplot(x='Emission type', y='Emissions per Mbps',
                 hue='Constellation', data=results, palette=palette)
plt.ylabel('Emissions/Mbps', fontsize=12)
plt.xlabel('Constellation', fontsize=12)
plt.title("Emissions/Mbps by Constellation", fontsize=12)
plt.tight_layout()
#plt.savefig(path+'constellation_by_emission_per_mbps.jpg', dpi=480)