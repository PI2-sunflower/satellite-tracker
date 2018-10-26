import numpy as np


def degrees_to_radians(degrees):
    radians = (degrees * np.pi) / 180.0
    return radians


def azimuth_to_theta(az):
    '''input:  azimuth (degrees)
       output: angle in radians (radians).

       The output is an angle in the clockwise direction from north.'''
    az = degrees_to_radians(az)
    theta = np.pi / 2.0 - az
    return theta


def elevation_to_radius(el):
    '''input:  azimuth (degrees) in the interval [-90, 90]
       output: angle in radians (radians)'''

    if abs(el) > 90.0:
        raise ValueError('Elevation {} is not in [-90.0, +90.0]'.format(el))

    radius = 90.0 - el
    return radius

def km_to_meters(x):
    METERS_IN_A_KILOMETER = 1000.0
    return x * METERS_IN_A_KILOMETER


def is_point_visible(y):
    return y >= 0.0
