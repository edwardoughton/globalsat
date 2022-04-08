import pandas as pd
import numpy as np
import emission_model as em

path = '/home/makavelli/Documents/GitHub Codes/Results/'

def per_sat_emission(name):
    data = None
    if name == 'starlink':
        sat_numb = 60
        fuel_mass = 488370
        fuel_per_sat = fuel_mass/sat_numb
        emission = em.falcon_9(fuel_per_sat)
        emission_results = pd.DataFrame(data=[*emission.items()], columns=['compound','amount'])
        df = pd.DataFrame(emission_results['compound'])
        df2 = pd.DataFrame(emission_results["amount"].to_list(), columns=['amount','constellation'])
        df3 = pd.concat([df, df2], axis=1)
        df3['constellation'] = name
        data = df3
    elif name == 'kuiper':
        sat_numb = 60
        m1, m2, m3 = 10000, 480000, 184900 #masses of hypergolic, solid and crayogenic fuels
        fm_hyp, fm_sod,fm_cry = m1/sat_numb , m2/sat_numb , m3/sat_numb #mass per fuel type per satellite
        emission = em.ariane(fm_hyp,fm_sod,fm_cry)
        emission_results = pd.DataFrame(data=[*emission.items()], columns=['compound',
                        'amount'])
        df = pd.DataFrame(emission_results['compound'])
        df2 = pd.DataFrame(emission_results["amount"].to_list(), columns=['amount',
                        'constellation'])
        df3 = pd.concat([df, df2], axis=1)
        df3['constellation'] = name
        data = df3
    elif name == 'oneweb':
        sat_numb = 36
        m1, m2 = 7360, 218150
        fm_hyp, fm_ker = m1/sat_numb, m2/sat_numb
        emission = em.soyuz_FG(fm_hyp,fm_ker)
        emission_results = pd.DataFrame(data=[*emission.items()], columns=['compound','amount'])
        df = pd.DataFrame(emission_results['compound'])
        df2 = pd.DataFrame(emission_results["amount"].to_list(), columns=['amount','constellation'])
        df3 = pd.concat([df, df2], axis=1)
        df3['constellation'] = name
        data = df3
    else:
        print('Invalid Constellation name')  
    return data
per_sat_emission('starlink')