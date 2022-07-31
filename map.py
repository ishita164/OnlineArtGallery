import googlemaps

print("Hello!!")

API_KEY = 'AIzaSyCDYJEJlMP4KZT503pTGlTOGg4OSpOfgmk'
map_client = googlemaps.Client(API_KEY)

def get_place_info(location_name):
    try:
        # location_name = 'Lanxess Arena Köln'
        response = map_client.places(query=location_name)
        results = response.get('results')[0]
        return results
    except Exception as e:
        print(e)
        return None

print(get_place_info('New York'))