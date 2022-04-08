import emission_model as em
import pandas as pd
path = '/home/makavelli/Desktop/GitHub/globalsat/results/'

a = em.per_sat_emission('oneweb')
a.to_csv(path+'nn.csv')