import requests
import sys
import time

# need to have each: route, stop & direction
if len(sys.argv) != 4:
    sys.exit("Please be sure to enter a route, stop, and direction.")

route = sys.argv[1]
stop = sys.argv[2]
direction = sys.argv[3]

# route = input("Input Route :- ")
# stop = input("Input destination stop : - ")
# direction = input("Input direction :- ")

url = "http://svc.metrotransit.org/NexTrip/"

# reqop--> to call the correct Request operation from Metro transit web services
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
    dataid = -1

    while True:
        try:
            sys.exit(reqop + str(resp.status_code))
        except:
            for item in data:

                if item[key].lower().find(arg.lower()) > -1:
                    dataid = item[value]
                    break
            return dataid


routeid = getdatafrommetro("Routes", "Description", "Route", route)

if len(routeid) < 0:
    sys.exit(route + " is not a valid route.")

reqop = routeid
directionid = getdatafrommetro("Directions/" + reqop, "Text", "Value", direction)

if len(directionid) < 0:
    sys.exit(route + " does not go " + direction + ".")

reqop += "/" + directionid
stopid = getdatafrommetro("Stops/" + reqop, "Text", "Value", stop)

if len(stopid) < 0:
    sys.exit(stop + " is not along " + route + " going " + direction + ".")

reqop += "/" + stopid

timeid = getdatafrommetro(reqop, "RouteDirection", "DepartureTime", direction)

if timeid != -1:
    # Get 10 digit timestamp from response, subtract from current time, and divide by 60 to get minutes
    time = int((float(timeid[6:16]) - time.time()) // 60)
    if time > 1:
        print(str(time) + " minutes")
    else:
        print("1 minute or less")
else:
    print("Last bus for the day has already left")
