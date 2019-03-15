import json
import requests
from math import radians, sin, cos, acos
from geopy.geocoders import Nominatim

earthRadius = 6371#km (taken from https://en.wikipedia.org/wiki/Great-circle_distance)

def geodesic_distance(lattitude, longitude):#calculate distance between 2 points on the surface of the sphere of the earth. Takes input as 2, lists of size 2 for 2 points. Formula from https://en.wikipedia.org/wiki/Great-circle_distance
	lattitudeRads = [radians(i) for i in lattitude]
	longitudeRads = [radians(i) for i in longitude]

	centralAngle = acos((sin(lattitudeRads[0])*sin(lattitudeRads[1])) + (cos(lattitudeRads[0])*cos(lattitudeRads[1])*cos(abs(longitudeRads[1]-longitudeRads[0]))))
	distance = earthRadius * centralAngle

	return distance

def closest_plane(lattitude, longitude):
	api = "https://opensky-network.org/api/states/all"

	response = requests.get(url=api)
	data = response.json()['states']

	LattitudeList = [lattitude, '']
	LongitudeList = [longitude, '']

	closest = [data[0], 10000000]

	for plane in data:
		try:
			LattitudeList[1] = plane[6]
			LongitudeList[1] = plane[5]

			distance = geodesic_distance(LattitudeList, LongitudeList)

			if distance<closest[1]:
				closest[0]=plane
				closest[1]=distance

		except:
			pass

	geolocator = Nominatim(user_agent="Closest Plane Finder")
	LatLongString = str(lattitude) + ", " + str(longitude)
	location = geolocator.reverse(LatLongString)

	print("\nClosest plane to", lattitude, "N", longitude, "E (" + location.address + ")")
	print("---------------------------------------------------")
	print("Distance:", closest[1], "km")
	print("Callsign:", closest[0][1])
	print("Lattitude and Longitude:", closest[0][6], "N,", closest[0][5], "E")
	print("Altitude:", closest[0][13], "m")
	print("Country of origin:", closest[0][2])
	print("ICA024 ID:", closest[0][0])

lattitude = float(input("Lattitude: "))
longitude = float(input("Longitude: "))

closest_plane(lattitude, longitude)

input("")
