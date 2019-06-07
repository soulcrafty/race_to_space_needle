import urllib.request
import polyline
from geojson import LineString, Feature, FeatureCollection
import json

#strava routes call , called ONCE
#"https://www.strava.com/api/v3/athletes/1109637/routes?access_token=d36427f914bafb2c9b8c423f1362d3b8e3d50609"

#route call , called for every element in ROUTES
#"https://www.strava.com/api/v3/routes/19221055?access_token=d36427f914bafb2c9b8c423f1362d3b8e3d50609"

#google directions api call
# "https://maps.googleapis.com/maps/api/directions/json?origin= " + origin_coordinates +  "&destination="+ destination_coordinates + "&key=AIzaSyBJ1VnvYHG4YqemW5W2XouFtDYtO_0Qc3s";


#google call directions departure time
#https://maps.googleapis.com/maps/api/directons/json?origin=Brooklyn&destination=Queens&departure_time=1343641500&mode=transit&key=YOUR_API_KEY
#times must be given in integer form, which is seconds since midnight, January 1st, 1970 UTC . You can also use a value of "now" but value must be current time or in the future
STRAVA_ACCESS_TOKEN = 'd1a1599a2ba3335e3108179763d50f0652b20849'
GOOGLE_MAPS_ACCESS_TOKEN = 'AIzaSyBJ1VnvYHG4YqemW5W2XouFtDYtO_0Qc3s'

STRAVA_BASE_URL = 'https://www.strava.com/api/v3/'
STRAVA_URL_ATHLETES = 'athletes/'
STRAVA_ATHLETE_ID = '1109637/'
STRAVA_URL_ROUTES_SLASH = 'routes/'
STRAVA_URL_ROUTES_NOSLASH = 'routes'
STRAVA_URL_PERPAGE = '?per_page=200&'
STRAVA_URL_ACCESS_TOKEN_NOQ = "access_token=" + STRAVA_ACCESS_TOKEN
STRAVA_URL_ACCESS_TOKEN = "?access_token=" + STRAVA_ACCESS_TOKEN

getAthleteRoutesUrl = STRAVA_BASE_URL + STRAVA_URL_ATHLETES + STRAVA_ATHLETE_ID + STRAVA_URL_ROUTES_NOSLASH + STRAVA_URL_PERPAGE + STRAVA_URL_ACCESS_TOKEN_NOQ
GOOGLE_MAPS_BASE_URL = "https://maps.googleapis.com/maps/api/directions/json?origin="

GOOGLE_MAPS_DESTINATION_URL = '&destination='
GOOGLE_MAPS_KEY_URL = "&key="
GOOGLE_DEPARTURE_URL = "&departure_time="

class DepartObj : 
		def __init__(self, depart_name, weekday, morneven, is_base_time, time_asint):
			self.depart_name = depart_name
			self.weekday = weekday
			self.morneven = morneven
			self.is_base_time = is_base_time
			self.time_asint = time_asint

weekday_morning = DepartObj('data_weekday_morning', True, 'MORNING', False, 1591110000) #6/2/2020 8:00 am PST. , 3PM GMT
weekday_evening = DepartObj('data_weekday_evening', True, 'EVENING', False, 1591142400) #6/2/20 5:00 pst, 6/3/2020 12:am midnight GMT
weekend_morning = DepartObj('data_weekend_morning', False, 'MORNING', False, 1591455600) #6/6/20 8:00 am pst, 3pm GMT
weekend_evening = DepartObj('data_weekend_evening', False, 'EVENING', False, 1591488000) #6/6/20 5:00 pm pst, 12:00 am midnight 6/7/20 GMT

departure_times = [weekday_morning, weekday_evening, weekend_morning, weekend_evening]

#container for the detailed routes with full polyline
routes_container = []

#getting the full polyline from a summary list of routes
routes = urllib.request.urlopen(getAthleteRoutesUrl)
routes_data = json.loads(routes.read().decode(routes.info().get_param('charset') or 'utf-8'))

for route in routes_data:
	#print(route['id'])
	route_id = route['id']
	routeDetailUrl = STRAVA_BASE_URL + STRAVA_URL_ROUTES_SLASH + str(route_id) + STRAVA_URL_ACCESS_TOKEN 
	routes_detail = urllib.request.urlopen(routeDetailUrl) #api call
	data = json.loads(routes_detail.read().decode(routes_detail.info().get_param('charset')or'utf-8'))
	routes_container.append(data)

for route in routes_container:

	decoded_polyline = polyline.decode(route['map']['polyline'])
	route['strava_decoded_polyline'] = decoded_polyline
	origin = str(decoded_polyline[0][0]) + "," + str(decoded_polyline[0][1])
	destination = str(decoded_polyline[len(decoded_polyline) -1][0]) + "," + str(decoded_polyline[len(decoded_polyline)-1][1])
	
	route['google_traffic_data'] = [];
	for i in departure_times : 

		google_maps_url = GOOGLE_MAPS_BASE_URL + origin + GOOGLE_MAPS_DESTINATION_URL + destination + GOOGLE_DEPARTURE_URL + str(i.time_asint) + GOOGLE_MAPS_KEY_URL + GOOGLE_MAPS_ACCESS_TOKEN
		google_maps_routes= urllib.request.urlopen(google_maps_url)
		valid_data = json.loads(google_maps_routes.read().decode(google_maps_routes.info().get_param('charset')or'utf-8'));
		route['google_traffic_data'].append(valid_data) 
		route['google_decoded_polyline'] = polyline.decode(route['google_traffic_data'][0]['routes'][0]['overview_polyline']['points'])

for route in routes_container:

	big_strava = route['strava_decoded_polyline']
	for i in big_strava:
			lst = list(i)
			temp = lst[0]
			lst[0] = lst[1]
			lst[1] = temp
			big_strava[big_strava.index(i)] = lst

	big_goog = route['google_decoded_polyline']
	for i in big_goog: 
			lst = list(i)
			temp = lst[0]
			lst[0] = lst[1]
			lst[1] = temp
			big_goog[big_goog.index(i)] = lst

for route in routes_container: 
	route['strava_features'] = Feature(geometry = LineString(route['strava_decoded_polyline']), properties = {"name": "line"})
	route['google_features']= Feature(geometry = LineString(route['google_decoded_polyline']), properties={"name":"line"})

with open('stravagoog_route_data.json', 'w') as outfile: 
		json.dump(routes_container, outfile)





