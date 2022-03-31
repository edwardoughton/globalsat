import numpy as np
import math
import pandas as pd

def soyuz_FG(hypergolic,kerosene):
    alumina_emission = (hypergolic*1*0.001)+(kerosene*1*0.05)
    sulphur_emission = (hypergolic*0.7*0.001)+(kerosene*0.7*0.001)
    carbon_emission = (hypergolic*0.252*1)+(kerosene*0.352*1)+(hypergolic*0.378*1.57)+(kerosene*0.528*1.57)
    cfc_gases = (hypergolic*0.016*0.7)+(kerosene*0.016*0.7)+(hypergolic*0.003*0.7)+(kerosene*0.003*0.7)+(hypergolic*0.001*0.7)+(kerosene*0.001*0.7)
    particulate_matter = (hypergolic*0.001*0.22)+(kerosene*0.001*0.22)+(hypergolic*0.001*1)+(kerosene*0.05*1)
    photo_oxidation = (hypergolic*0.378*0.0456)+(kerosene*0.528*0.0456)+(hypergolic*0.001*1)+(kerosene*0.001*1)
    return {'Aluminium Oxides': alumina_emission, 'Sulphur Oxides': sulphur_emission, 'Carbon Oxides': carbon_emission, 'Cfc Gases': cfc_gases, 'Particulate Matter': particulate_matter, 'Photochemical Oxidation': photo_oxidation}

def falcon_9(kerosene):
    alumina_emission = (kerosene*0.05)
    sulphur_emission = (kerosene*0.001*0.7)
    carbon_emission = (kerosene*0.352*1)+(0.528*kerosene*1.57)
    cfc_gases = (kerosene*0.016*0.7)+(kerosene*0.003*0.7)+(kerosene*0.001*0.7)
    particulate_matter = (kerosene*0.001*0.22)+(kerosene*0.05*1)
    photo_oxidation = (kerosene*0.0456*0.528)+(kerosene*0.001*1)
    return {'Aluminium Oxides': alumina_emission, 'Sulphur Oxides': sulphur_emission, 'Carbon Oxides': carbon_emission, 'Cfc Gases': cfc_gases, 'Particulate Matter': particulate_matter, 'Photochemical Oxidation': photo_oxidation}

def falcon_heavy(kerosene):
    alumina_emission = (kerosene*0.05)
    sulphur_emission = (kerosene*0.001*0.7)
    carbon_emission = (kerosene*0.352*1)+(0.528*kerosene*1.57)
    cfc_gases = (kerosene*0.016*0.7)+(kerosene*0.003*0.7)+(kerosene*0.001*0.7)
    particulate_matter = (kerosene*0.001*0.22)+(kerosene*0.05*1)
    photo_oxidation = (kerosene*0.0456*0.528)+(kerosene*0.001*1)
    return {'Aluminium Oxides': alumina_emission, 'Sulphur Oxides': sulphur_emission, 'Carbon Oxides': carbon_emission, 'Cfc Gases': cfc_gases, 'Particulate Matter': particulate_matter, 'Photochemical Oxidation': photo_oxidation}

def ariane(hypergolic,solid,cryogenic):
    alumina_emission = (solid*0.33*1)+(hypergolic*0.001*1)
    sulphur_emission = (solid*0.005*0.7)+(cryogenic*0.001*0.7)+(hypergolic*0.001*0.7)+(solid*0.15*0.88)
    carbon_emission = (solid*0.108*1)+(hypergolic*0.252)+(solid*0.162*1.57)+(hypergolic*0.378*1.57)
    cfc_gases = (solid*0.08*0.7)+(cryogenic*0.016*0.7)+(hypergolic*0.016*0.7)+(solid*0.015*0.7)+(cryogenic*0.003*0.7)+(hypergolic*0.003*0.7)+(solid*0.005*0.7)+(cryogenic*0.001*0.7)+(hypergolic*0.001*0.7)+(solid*0.15*0.7)
    particulate_matter = (solid*0.005*0.22)+(cryogenic*0.001*0.22)+(hypergolic*0.001*0.22)+(solid*0.33*1)+(hypergolic*0.001*1)
    photo_oxidation = (solid*0.162*0.0456)+(hypergolic*0.378*0.0456)+(solid*0.005*1)+(cryogenic*0.001*1)+(hypergolic*0.001*1)
    return {'Aluminium Oxides': alumina_emission, 'Sulphur Oxides': sulphur_emission, 'Carbon Oxides': carbon_emission, 'Cfc Gases': cfc_gases, 'Particulate Matter': particulate_matter, 'Photochemical Oxidation': photo_oxidation}