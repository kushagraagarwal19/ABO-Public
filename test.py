import googlemaps
from datetime import datetime
import json

gmaps = googlemaps.Client(key='AIzaSyDZhjxJiq0hcDiB1MDGBAO12RBB7tBIB5k')

# Geocoding an address
# geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')

# print geocode_result

# Look up an address with reverse geocoding
# reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))

# print reverse_geocode_result

# Request directions via public transit
# now = datetime.now()
# directions_result = gmaps.directions("Sydney Town Hall",
#                                      "Parramatta, NSW",
#                                      mode="transit",
#                                      departure_time=now)

# print directions_result

origins = [(40.690604, -73.940121)]
# destinations = [(43.012486, -83.6964149), {"lat": 42.8863855, "lng": -78.8781627}]

destinations = [(40.690276, -73.941392), (43.012486, -83.6964149)]
matrix = gmaps.distance_matrix(origins, destinations)


if 'distance' not in matrix['rows'][0]['elements'][0]:
    print "LOL"
    print matrix
else:
    print matrix['rows'][0]['elements'][0]['distance']['text']
    print matrix

print json.dumps(matrix)