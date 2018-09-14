import os

import requests


API_KEYS = {
    'N2YO': os.environ.get('N2YO_KEY', ''),
}

SATELLITES_IDS = {
    'ISS': 25544,
}


def get_tle(id):
    '''Gets satellite's TLE from it's NORAG id:
    https://en.wikipedia.org/wiki/Satellite_Catalog_Number'''

    API_NAME = 'N2YO'
    ENDPOINT = 'https://www.n2yo.com/rest/v1/satellite/tle/{}&apiKey={}'

    url = ENDPOINT.format(id, API_KEYS[API_NAME])
    print('url = {}'.format(url))

    response = requests.get(url).json()
    tle = response['tle']
    return tle

if __name__ == '__main__':
    print('API_KEYS = {}'.format(API_KEYS))

    id = SATELLITES_IDS['ISS']
    tle = get_tle(id)
    print('tle = {}'.format(tle))
