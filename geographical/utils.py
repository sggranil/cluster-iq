import requests
from django.conf import settings

def geocode_address(address):
    url = settings.GOOGLE_MAP_API_URL
    params = {
        'address': f'{address}, {settings.CITY}',
        'key': settings.GOOGLE_MAP_API_KEY
    }

    response = requests.get(url, params=params)
    result = response.json()

    if response.status_code == 200 and result['status'] == 'OK':
        location = result['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        return lat, lng
    else:
        return None, None
