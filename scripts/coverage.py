import numpy as np
import math as mt

equator = 0  # Reference point
earth_radius_equator = 6378.137  # Radius of the earth at the equator in km
earth_radius_poles = 6356.752     # Radius of the earth at the poles in km


def coverage_area(latitude_interval):
    coverage_data = []
    for angles in range(0, 91, latitude_interval):  
        latitude2 = angles
        numerator = (((earth_radius_equator**2)*(np.cos(np.radians(angles))))
                     ** 2)+(((earth_radius_poles**2)*(np.sin(np.radians(angles))))**2)
        denominator = ((((earth_radius_equator)*(np.cos(np.radians(angles))))
                        ** 2)+(((earth_radius_poles)*(np.sin(np.radians(angles))))**2))
        radius_at_latitude = np.sqrt(numerator/denominator)
        latitude_change = angles-equator
        eccentricity = 1-((earth_radius_poles**2)/(radius_at_latitude**2)) #Compute eccentricity
        area = 4*np.pi*radius_at_latitude**2  #Circular area at given latitude
        if eccentricity != 0:
            earth_surface_area_at_latitude = (2*radius_at_latitude**2)*(
                1+(((1-(eccentricity**2))/eccentricity)*(mt.atanh(eccentricity))))#surface area of the earth at given latitude
            coverage_data.append({'Equator': equator, 'User latitude': angles,
                                  'Radius_at_latitude': radius_at_latitude,
                                  'Area of a circle at the latitude':
                                  earth_surface_area_at_latitude, 'Surface_area': area})
        else:
            pass
    return coverage_data
