import os
from datetime import datetime, timezone

import requests


API_KEYS = {
    'N2YO': os.environ.get('N2YO_KEY', ''),
}

SATELLITES_IDS = {
    'ISS': 25544,
    'BRISAT': 41591,
    'AQUARIUS': 37673,
    'ARIANE': 25990,
    'TELSTAR4': 23670,
}


def get_tle(norad_id=None, name=None):
    '''Gets satellite's TLE from it's NORAG id:
    https://en.wikipedia.org/wiki/Satellite_Catalog_Number'''
    
    if norad_id is None:
        if name is not None:
            norad_id = SATELLITES_IDS[name]
        else:    
            raise ValueError('NORAD id or satellite\'s name must be given')

    API_NAME = 'N2YO'
    ENDPOINT = 'https://www.n2yo.com/rest/v1/satellite/tle/{}&apiKey={}'

    url = ENDPOINT.format(norad_id, API_KEYS[API_NAME])
    response = requests.get(url).json()

    tle = response['tle']
    line1, line2 = tle.split('\r\n')
    return line1, line2

def get_az_el(lat, lng, alt, norad_id=None, name=None, seconds=1):
    '''Gets satellite's AZ/EL from it's NORAD id:
    https://en.wikipedia.org/wiki/Satellite_Catalog_Number'''

    if norad_id is None:
        if name is not None:
            norad_id = SATELLITES_IDS[name]
        else:
            raise ValueError('NORAD id or satellite\'s name must be given')

    API_NAME = 'N2YO'
    ENDPOINT = 'https://www.n2yo.com/rest/v1/satellite/positions/{}/{}/{}/{}/{}/&apiKey={}'


    url = ENDPOINT.format(norad_id, lat, lng, alt, seconds, API_KEYS[API_NAME])
    response = requests.get(url).json()
    positions = response['positions']

    az = []
    el = []
    dates = []

    for i in range(len(positions)):
        az.append(positions[i]['azimuth'])
        el.append(positions[i]['elevation'])

        timestamp = positions[i]['timestamp']
        date = datetime.utcfromtimestamp(timestamp).replace(tzinfo=timezone.utc)
        dates.append(date)

    return az, el, dates


if __name__ == '__main__':
    print('API_KEYS = {}'.format(API_KEYS))

    id = SATELLITES_IDS['ISS']
    tle = get_tle(id)
    print('tle = {}'.format(tle))
