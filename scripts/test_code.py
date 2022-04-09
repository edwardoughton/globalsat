import emission_model as em
import pandas as pd
path = '/home/makavelli/Desktop/GitHub/globalsat/results/'

'''a = em.per_sat_emission('starlink')
a.to_csv(path+'constellation_emission_results.csv')'''

df = em.starlink_emission()
df1 = em.oneweb_emission()
df2 = em.kuiper_emission()

frames = [df, df1, df2]
results = pd.concat(frames)
results.to_csv(path+'constellation_emission_results.csv')