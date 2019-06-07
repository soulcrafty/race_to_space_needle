import urllib.request
import polyline
from geojson import LineString, Feature, FeatureCollection
import json

class DepartObj : 
		def __init__(self, weekday, morneven, is_base_time, time_asint):
			self.weekday = weekday
			self.morneven = morneven
			self.is_base_time = is_base_time
			self.time_asint = time_asint

base_time = DepartObj(True, 'MORNING', True, 1591092000) #6/2/2020 3:00 AM pst, 10 AM GMT
weekday_morning = DepartObj(True, 'MORNING', False, 1591110000) #6/2/2020 8:00 am PST. , 3PM GMT
weekday_evening = DepartObj(True, 'EVENING', False, 1591142400) #6/2/20 5:00 pst, 6/3/2020 12:am midnight GMT
weekend_morning = DepartObj(False, 'MORNING', False, 1591455600) #6/6/20 8:00 am pst, 3pm GMT
weekend_evening = DepartObj(False, 'EVENING', False, 1591488000) #6/6/20 5:00 pm pst, 12:00 am midnight 6/7/20 GMT

#departure_times = [base_time, weekday_morning, weekday_evening, weekend_morning, weekend_evening]
departure_times = [Ωweekday_morning]


kennydale_polyline = "a}_aHt_|hVCkM?uJAeY?}N?sBkGRuA@cDEwKUYA]NkBKiAGmKe@_FOkA@mDJgDDoCHsB@c@?cBMiB[u@Us@[}BiAiAq@oLiGiB}@yAo@oBe@aBQk@Em@?{@BqAJ}AVkFpAiB`@kARoALkCJiHCqIGeFCeCGmHc@{AKkAQ}Bq@sAm@aAk@eAo@yBcBuFkEoCuBeCcB{LwHgHwE}CsBuBoAqAm@iBs@gBi@kAYuB]{Ca@mAWiA]iAk@e@]}@w@q@{@_AyAw@gBk@mBsAmGo@qCY_A{@gCkA}By@qA]e@aByAsAy@eCiAwLaG{BcAmFgCmCoAqBcA[OIUKO_B{@uCyAcA_@kEcAiBa@}@UcAUg@Eg@@_ALi@PYNo@f@{@`Ag@bA_@hA[|AMpAEdA@fBXhFBn@CVD~@LpCLnCVrF`ArTfAvK^|IB|CHj@G|BKbBQfBcAxIUtBMpBEbCBnCJnAZhCvCnQvAvIdAvHT`C\\vFBvC?xAEhBE|@QtBkBpVQjCa@hEUvBw@zDq@dCo@hBi@nAm@nAm@dAyCxEsAvBcAnBe@lAqIjWmDzKwAtD_DrHy@lB{AtDcCxG_BpFgAtEeFnSgA~Di@dBW|@sAdDiChGqA|Dg@zC]bCKrAK~C?hBRnFPpB`@zCdAhElD|Ip@~Bd@xA^tAX~AVhBVhDD|@B|DAvAGlM_@`j@gBdgCC`JApIAvLCtQGzFMlJC`N@pG@nE?t@?jP@dJCjCCfAMrAU~Ak@zBy@rBoAdB]ZiAv@iAv@iC|AqBnAs@h@e@f@e@p@Q`@k@zAMf@SjAGf@Gr@G^Kx@AbADvBj@hFVbC?d@GlAI`@[|@c@n@c@`@SLm@Rc@Hm@HoBXaCl@WN}@ZoAh@k@^a@To@`@eAv@UPuAzAiAvAkFlHiCtDwDfFu@|@o@n@M?GBkAv@qB|AqCzBsBrAsAfAaAx@iCtBeA|@JXFRNd@|C`K~@vCPj@_BxAuDhDyAvAqKhJ{F`FgDzCW\\eC~E_JvQuGpMkCnF}EtJwApC_@Tc@JaAAyACUDMFKNW]IY"
kennydale_origin = "47.5184119,-122.2093877"
kennydale_destination = "47.6197735,-122.3487767"

routes_container = []

for i in departure_times : 
	kennydale_api_call = "https://maps.googleapis.com/maps/api/directions/json?origin=" + kennydale_origin +  "&destination="+ kennydale_destination + "&departure_time=" + str(i.time_asint) + "&key=AIzaSyBJ1VnvYHG4YqemW5W2XouFtDYtO_0Qc3s"
	print(kennydale_api_call)
	routes = urllib.request.urlopen(kennydale_api_call)
	routes_data = json.loads(routes.read().decode(routes.info().get_param('charset') or 'utf-8'))
	routes_container.append(routes_data)

#sanity check
for e in routes_container : 
	if(routes_container[0]['routes'][0]['overview_polyline']['points'] == routes_container[routes_container.index(e)]['routes'][0]['overview_polyline']['points']):
		print('pass' + ' _ total est time : ' + str(routes_container[routes_container.index(e)]['routes'][0]['legs'][0]['duration_in_traffic']['value']))
	else:
		print(e + "_failed")


with open('kennydale_route_data.json', 'w') as outfile: 
		json.dump(routes_container, outfile)
#google_obj['routes'][0]['legs'][0]['steps'][0].   #we need to traverse all element of the 'steps' array to make sure all corrdinates are equal across all 5 depart timescfd4


#for t in departure_time : 
#	t.time_as_int

#60 routes x 1 MapsAPI call per route NO Traffic -- OR 60 Routes x 5 = 300 API API calls, assumes all 5 routes  overlap 100%
