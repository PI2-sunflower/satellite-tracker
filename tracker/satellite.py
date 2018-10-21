from datetime import datetime, timedelta, timezone

from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
from sgp4.model import Satellite
import pymap3d as pm
from tracker.conversions import km_to_meters
from math import ceil
import numpy as np

METERS_IN_A_KILOMETER = 1000.0


class Satellite:
    '''This is a wrapper of sgp4.model.satellite and pymap3d modules.'''

    def __init__(self, tle_line1, tle_line2):
        self.satellite = twoline2rv(tle_line1, tle_line2, wgs84)

    def propagate(self, date):
        '''Returns satellite's position vector and the velocity vector,
        in meters, at the given datetime.

        Output format: (r, v)
        r : Position vector, a tuple of 3 floats (x, y, z)
            Measures the satellite position in **meters** from the center
            of the earth.
            This position vector uses the Earth-centered inertial (ECI) frame.
        v : Velocity vector, a tuple of 3 floats (dx, dy, dz)
            Measures the rate at which the three position vector parameters
            are changing, expressed in **meters** per second'''

        if not isinstance(date, datetime):
            raise ValueError('date should be a datetime object')

        if not (date.tzinfo == timezone.utc):
            raise ValueError('Time must be in UTC')

        date_at = date.year, date.month, date.day, date.hour, date.minute, \
                  date.second + (date.microsecond / 1000000.0)

        r, v = self.satellite.propagate(*date_at)
        assert self.satellite.error == 0

        to_meters = lambda x: tuple(km_to_meters(y) for y in x)
        vectors = tuple(to_meters(vector) for vector in (r, v))
        return vectors


    def propagate_positions_step(self, start=None, count=20, step=1):
        '''Uses self.propagate to propaate satellite in the 'count' points
        starting at 'start', where which point is separated by 'step'
        seconds'''

        if not isinstance(step, int):
            raise ValueError('step must be int')
        if step < 1:
            raise ValueError('step must be >= 1')
        if count < 1:
            raise ValueError('count must be >= 1')

        if start is None:
            start = datetime.now(timezone.utc)

        position_time = lambda x, y: (x.propagate(y)[0], y)
        dates = [start + timedelta(seconds=step * i) for i in range(count)]
        positions = tuple(position_time(self, at) for at in dates)
        return positions

    def propagate_positions(self, start, end, count=20):
        '''Uses self.propagate to propaate satellite in the 'count' points
        starting at 'start', ending at 'ending' '''

        if not isinstance(count, int):
            raise ValueError('count must be int')
        if count < 1:
            raise ValueError('count must be >= 1')

        step = ceil((end - start).seconds / count)
        print('STEP = {}'.format(step))

        position_time = lambda x, y: (x.propagate(y)[0], y)

        dates = []
        for i in range(count):
            date = start + timedelta(seconds=step * i)
            if date > end:
                break
            dates.append(date)

        positions = tuple(position_time(self, at) for at in dates)
        return positions

    def get_observer_azimuth_elevation(self, observer_latitude,
                          observer_longitude, observer_altitude, date=None):
        '''Returns the satellite directions (azimuth, elevation) for the given
        observer's positions'''

        if date is None:
            date = datetime.now(timezone.utc)

        eci_position = self.propagate(date)[0]
        aer_position = pm.eci2aer(eci_position, observer_latitude,
                                  observer_longitude, observer_altitude, date)

        az = aer_position[0][0]
        el = aer_position[1][0]
        return az, el


