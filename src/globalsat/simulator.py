"""

Simulation manager

"""


class SimulationManager(object):

    def __init__(self, data, parameters):

        self.assets = {}

        for datum in data:
            asset_id = datum['id']
            asset_object = Satellite(datum)
            self.assets[asset_id] = asset_object


class Satellite(object):

    def __init__(self, data):

        self.x = data['x']
        self.y = data['y']
        self.z = data['z']
        self.vx = data['vx']
        self.vy = data['vy']
        self.vz = data['vz']
        self.orbit = data['orbit']
        self.constellation = data['constellation']
        self.age = data['age']
        self.fragility = data['fragility']
        self.exposure = data['exposure']
        self.design = data['design']
        self.operational = None
        self.cost = data['cost']
