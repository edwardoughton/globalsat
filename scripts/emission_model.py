import pandas as pd

path = '/home/makavelli/Desktop/GitHub/globalsat/results/'

def soyuz_FG(hypergolic, kerosene):
    alumina_emission = (hypergolic*1*0.001)+(kerosene*1*0.05)
    sulphur_emission = (hypergolic*0.7*0.001)+(kerosene*0.7*0.001)
    carbon_emission = (hypergolic*0.252*1)+(kerosene*0.352*1) + \
        (hypergolic*0.378*1.57)+(kerosene*0.528*1.57)
    cfc_gases = (hypergolic*0.016*0.7)+(kerosene*0.016*0.7)+(hypergolic*0.003*0.7) + \
        (kerosene*0.003*0.7)+(hypergolic*0.001*0.7)+(kerosene*0.001*0.7)
    particulate_matter = (hypergolic*0.001*0.22)+(kerosene *0.001*0.22)+(hypergolic*0.001*1)+(kerosene*0.05*1)
    photo_oxidation = (hypergolic*0.378*0.0456)+(kerosene *0.528*0.0456)+(hypergolic*0.001*1)+(kerosene*0.001*1)
    return {'Aluminium Oxides': [alumina_emission, 'name'], 'Sulphur Oxides': [sulphur_emission, 'name'],
            'Carbon Oxides': [carbon_emission, 'name'], 'Cfc Gases': [cfc_gases, 'name'], 'Particulate Matter':
            [particulate_matter, 'name'], 'Photochemical Oxidation': [photo_oxidation, 'name'], }

def falcon_9(kerosene):
    alumina_emission = (kerosene*0.05)
    sulphur_emission = (kerosene*0.001*0.7)
    carbon_emission = (kerosene*0.352*1)+(0.528*kerosene*1.57)
    cfc_gases = (kerosene*0.016*0.7)+(kerosene*0.003*0.7)+(kerosene*0.001*0.7)
    particulate_matter = (kerosene*0.001*0.22)+(kerosene*0.05*1)
    photo_oxidation = (kerosene*0.0456*0.528)+(kerosene*0.001*1)
    return {'Aluminium Oxides': [alumina_emission, 'name'], 'Sulphur Oxides':
            [sulphur_emission, 'name'], 'Carbon Oxides': [carbon_emission, 'name'],
            'Cfc Gases': [cfc_gases, 'name'], 'Particulate Matter': [particulate_matter,
            'name'], 'Photochemical Oxidation': [photo_oxidation, 'name']}

def falcon_heavy(kerosene):
    alumina_emission = (kerosene*0.05)
    sulphur_emission = (kerosene*0.001*0.7)
    carbon_emission = (kerosene*0.352*1)+(0.528*kerosene*1.57)
    cfc_gases = (kerosene*0.016*0.7)+(kerosene*0.003*0.7)+(kerosene*0.001*0.7)
    particulate_matter = (kerosene*0.001*0.22)+(kerosene*0.05*1)
    photo_oxidation = (kerosene*0.0456*0.528)+(kerosene*0.001*1)
    return {'Aluminium Oxides': [alumina_emission, 'name'], 'Sulphur Oxides': [sulphur_emission, 'name'],
            'Carbon Oxides': carbon_emission, 'Cfc Gases': cfc_gases, 'Particulate Matter':
            [particulate_matter, 'name'], 'Photochemical Oxidation': [photo_oxidation, 'name']}

def ariane(hypergolic, solid, cryogenic):
    alumina_emission = (solid*0.33*1)+(hypergolic*0.001*1)
    sulphur_emission = (solid*0.005*0.7)+(cryogenic*0.001*0.7) + \
        (hypergolic*0.001*0.7)+(solid*0.15*0.88)
    carbon_emission = (solid*0.108*1)+(hypergolic*0.252) + \
        (solid*0.162*1.57)+(hypergolic*0.378*1.57)
    cfc_gases = (solid*0.08*0.7)+(cryogenic*0.016*0.7)+(hypergolic*0.016*0.7)+(solid*0.015*0.7)+(cryogenic*0.003*0.7) + \
        (hypergolic*0.003*0.7)+(solid*0.005*0.7) + \
        (cryogenic*0.001*0.7)+(hypergolic*0.001*0.7)+(solid*0.15*0.7)
    particulate_matter = (solid*0.005*0.22)+(cryogenic*0.001*0.22) + \
        (hypergolic*0.001*0.22)+(solid*0.33*1)+(hypergolic*0.001*1)
    photo_oxidation = (solid*0.162*0.0456)+(hypergolic*0.378*0.0456) + \
        (solid*0.005*1)+(cryogenic*0.001*1)+(hypergolic*0.001*1)
    return {'Aluminium Oxides': [alumina_emission, 'name'], 'Sulphur Oxides': [sulphur_emission, 'name'],
            'Carbon Oxides': [carbon_emission, 'name'], 'Cfc Gases': [cfc_gases, 'name'], 'Particulate Matter':
            [particulate_matter, 'name'], 'Photochemical Oxidation': [photo_oxidation, 'name']}

def per_sat_emission(name):
    data = None 
    if name == 'starlink':
        sat_numb = 60                      #number of satellites per launch
        fuel_mass = 488370                 #mass of fuel per launch
        fuel_per_sat = fuel_mass/sat_numb  #fuel per satellite
        emission = falcon_9(fuel_per_sat)  #emission per satellite
        emission_results = pd.DataFrame(data=[*emission.items()], columns=['Emission type', 'amount']) #convert to dataframe
        # create a dataframe from the main
        df = pd.DataFrame(emission_results['Emission type'])
        df2 = pd.DataFrame(emission_results["amount"].to_list(), columns=[
            'amount', 'Constellation']) #split the list inside the dataframe cells
        dfs = pd.concat([df, df2], axis=1) #merge the two dataframes
        dfs['Constellation'] = name        #assign the constellation name
        data = dfs
    elif name == 'kuiper':
        sat_numb = 60
        # masses of hypergolic, solid and cryogenic fuels
        m1, m2, m3 = 10000, 480000, 184900
        fm_hyp, fm_sod, fm_cry = m1/sat_numb, m2/sat_numb, m3 / \
            sat_numb  # mass per fuel type per satellite
        emission = ariane(fm_hyp, fm_sod, fm_cry) #emission per satellite per fuel type
        emission_results = pd.DataFrame(data=[*emission.items()], columns=['Emission type',
                        'amount'])
        df = pd.DataFrame(emission_results['Emission type'])
        df2 = pd.DataFrame(emission_results["amount"].to_list(), columns=['amount',
            'Constellation'])
        dfk = pd.concat([df, df2], axis=1)
        dfk['Constellation'] = name
        data = dfk
    elif name == 'oneweb':
        sat_numb = 36
        m1, m2 = 7360, 218150
        fm_hyp, fm_ker = m1/sat_numb, m2/sat_numb
        emission = soyuz_FG(fm_hyp, fm_ker)
        emission_results = pd.DataFrame(
            data=[*emission.items()], columns=['Emission type', 'amount'])
        df = pd.DataFrame(emission_results['Emission type'])
        df2 = pd.DataFrame(emission_results["amount"].to_list(), columns=[
            'amount', 'Constellation'])
        dfw = pd.concat([df, df2], axis=1)
        dfw['Constellation'] = name
        data = dfw 
    else:
        print('Invalid Constellation name')
    return data

#starlink emission
def starlink_emission():
    starlink_data = per_sat_emission('starlink')
    return starlink_data

#oneweb emission
def oneweb_emission():
    oneweb_data = per_sat_emission('oneweb')
    return oneweb_data

#kuiper emission
def kuiper_emission():
    kuiper_data = per_sat_emission('kuiper')
    return kuiper_data
