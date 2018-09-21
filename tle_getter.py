import os

import requests


API_KEYS = {
    'N2YO': os.environ.get('N2YO_KEY', ''),
}

SATELLITES_IDS = {
    'ISS': 25544,
    'BRISAT': 41591,
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

if __name__ == '__main__':
    print('API_KEYS = {}'.format(API_KEYS))

    id = SATELLITES_IDS['ISS']
    tle = get_tle(id)
    print('tle = {}'.format(tle))
