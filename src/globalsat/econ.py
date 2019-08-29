"""

Economic assessment module

"""

def assess_econ(system):

    results = []

    for asset in system.assets.values():
        if asset.operational == 0:
            results.append({
                'id': asset.id,
                'x': asset.x,
                'y': asset.y,
                'z': asset.z,
                'vx': asset.vx,
                'vy': asset.vy,
                'vz': asset.vz,
                'orbit': asset.orbit,
                'constellation': asset.constellation,
                'age': asset.age,
                'fragility': asset.fragility,
                'design': asset.design,
                'operational': asset.operational,
                'cost': asset.cost,
            })

    return results
