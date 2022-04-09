import emission_model as em
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import ScalarFormatter
from matplotlib import pyplot
path = '/home/makavelli/Desktop/GitHub/globalsat/results/'

#Emission model test
df = em.starlink_emission()
df1 = em.oneweb_emission()
df2 = em.kuiper_emission()

frames = [df, df1, df2]
results = pd.concat(frames)
results.to_csv(path+'constellation_emission_results.csv')

#Plotting sample data
palette = sns.color_palette("Paired")
a4_dims = (12, 5)
sns.set_style('darkgrid')
fig, ax = pyplot.subplots(figsize=a4_dims)
ax = sns.barplot(x='Emission type', y='amount',
                 hue='Constellation', data=results, palette=palette)
plt.ylabel('Emissions per satellite', fontsize=12)
plt.xlabel('Constellation', fontsize=12)
plt.title("Constellation by Emission Type",fontsize=12)
plt.tight_layout()
plt.savefig(path+'constellation_by_emission_type.jpg',dpi=480)
