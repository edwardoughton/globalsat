from aifc import Aifc_read
from sunau import Au_read
import numpy as np

equator = 0                   #Reference point
earth_radius_equator = 6378   #Radius of the earth at the equator in km
earth_radius_poles = 6357     # Radius of the earth at the poles in km

def coverage_area(latitude_interval):
    coverage_data = []
    for angles in range(0,90,latitude_interval): #np.sin(np.radians(60))
        latitude2 = angles
        numerator = (((earth_radius_equator**2)*(np.cos(np.radians(angles))))
                     ** 2 + ((earth_radius_poles**2)*(np.sin(np.radians(angles))))**2)
        denominator = ((earth_radius_poles*(np.cos(np.radians(angles))))
                       ** 2)+((earth_radius_poles*(np.sin(np.radians(angles))))**2)
        radius_at_latitude = np.sqrt(numerator/denominator)
        latitude_change = angles-equator
        area = 2*np.pi*radius_at_latitude*((np.sin(np.radians(latitude2)))-(np.sin(np.radians(equator))))
        circle_area_at_latitude = 4*np.pi*radius_at_latitude**2
        coverage_data.append({'Equator':equator,'Instantenous angle': angles,
                                'Area of a circle at the latitude':
                                circle_area_at_latitude})
    print(coverage_data)
    return coverage_data 
