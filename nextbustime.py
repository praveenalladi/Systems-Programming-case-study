import requests
import sys
import time

# need to have each: route, stop & direction
if len(sys.argv) != 4:
    sys.exit("Please be sure to enter a route, stop, and direction.")

route = sys.argv[1]
stop = sys.argv[2]
direction = sys.argv[3]

url = "http://svc.metrotransit.org/NexTrip/"

# reqop --> to call the correct Request operation from Metro transit web services
# first get route Id and then use that to get direction id
# use the two to get stop id and use teh three to get time
# GetRoutes operation - http://svc.metrotransit.org/NexTrip/Routes
# GetDirections operation - http://svc.metrotransit.org/NexTrip/Directions/{ROUTE}
# GetStops operation - http://svc.metrotransit.org/NexTrip/Stops/{ROUTE}/{DIRECTION}
# GetTimepointDepartures operation - http://svc.metrotransit.org/NexTrip/{ROUTE}/{DIRECTION}/{STOP}
# arg --> to get get the appropriate value(route,stop, direction)


def getdatafrommetro(reqop, key, value, arg):

    resp = requests.get(url + reqop + "?format=json")
    data = resp.json()

    # default in case of invalid input
    dataID = -1

    while True:
        try: sys.exit(reqop + str(resp.status_code))

        except:
            for item in data:
                if item[key].lower().find(arg) > -1:
                    dataID = item[value]
                    break
            return dataID


routeID = getdatafrommetro("Routes", "Description", "Route", route)

if len(routeID) < 0:
    sys.exit(route + " is not a valid route.")

reqop = routeID
directionID = getdatafrommetro("Directions/" + reqop, "Text", "Value", direction)

if len(directionID) < 0:
    sys.exit(route + " does not go " + direction + ".")

reqop += "/" + directionID
stopID = getdatafrommetro("Stops/" + reqop, "Text", "Value", stop)

if len(stopID) < 0:
    sys.exit(stop + " is not along " + route + " going " + direction + ".")

reqop += "/" + stopID

timeID = getdatafrommetro(reqop, "RouteDirection", "DepartureTime", direction)

if timeID != -1:
    # Get 10 digit timestamp from response, subtract from current time, and divide by 60 to get minutes
    time = int((float(timeID[6:16]) - time.time()) // 60)
    if time > 1:
        print(str(time) + " minutes")
    else:
        print ("1 minute or less")