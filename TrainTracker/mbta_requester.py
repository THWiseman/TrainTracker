import os
import requests
import json
from collections import defaultdict

class MBTARequester:
    def __init__(self):
        self.apiKey = os.getenv('MBTA_API_KEY')
        self.apiEndpoint = os.getenv('MBTA_API_ENDPOINT')
        self.headerDict = {"x-api-key" : self.apiKey} #We can use this dict as an HTTP header when sending requests.
        self.routeToStops = None
        self.stopToRoutes = None

    def getAllTrainRouteNames(self):
        '''
        Queries the MBTA API to get the name of each subway route.
        Returns: 
            route_names (List of String) : A list of the 'long_name' for each subway route. 
        '''
        routeEndpoint = self.apiEndpoint + "/routes/"
        filterParams = {
            "filter[type]" : "0,1",  # 0 and 1 represent 'Light Rail' and 'Heavy Rail' according to the API spec. 
            "fields[route]" : "long_name" # filter the request to only ask for the 'long_name' field. 
        }
        response = requests.get(routeEndpoint, headers=self.headerDict, params=filterParams)
        responseDict = json.loads(response.text)
        route_names = []
        for trainRoute in responseDict["data"]:
            route_names.append(trainRoute["attributes"]["long_name"])
        return route_names

    def getAllTrainRouteIds(self):
        routeEndpoint = self.apiEndpoint + "/routes/"
        filterParams = {
            "filter[type]" : "0,1",  # 0 and 1 represent 'Light Rail' and 'Heavy Rail' according to the API spec. 
        }
        response = requests.get(routeEndpoint, headers=self.headerDict, params=filterParams)
        responseDict = json.loads(response.text)
        route_ids = []
        for trainRoute in responseDict["data"]:
            route_ids.append(trainRoute["id"])
        return route_ids

    def getAllStopsOnRoute(self, routeId):
        '''
        Queries the MBTA API to get the name of each stop on the specified route.
        Parameters:
            routeId (string) : Unique identifier for an MBTA route. Looks like 'Red' or Green Line B'. Consult MBTA docs or API for full list.
        Returns:
            stop_names (list of string) : A list containing the name of each stop on the specified route. 
        '''
        stopEndpoint = self.apiEndpoint + "/stops/"
        filterParams = {
            "filter[route]" : f"{routeId}",
            "fields[stop]" : "name"
        }

        response = requests.get(stopEndpoint, headers=self.headerDict, params=filterParams)
        responseDict = json.loads(response.text)
        stop_names = []
        for stop in responseDict["data"]:
            stop_names.append(stop["attributes"]["name"])
        return stop_names

    def buildRouteAndStopRelationships(self):
        '''
        This funciton performs multiple queries on the MBTA API to store the many-to-many relationship between routes and stops as two member dictionaries.
        self.routeToStops (dict[str, list[str]): A dictionary where each key is a route and each value is a list of stops on that route.
        self.stopToRoutes (dictpstr, list[str]): A dictionary where each key is a stop and each value is a list of routes that that stop is on. 
        '''
        print("Building route and stop relationships. This could take a second...")
        self.routeToStops = defaultdict(list)
        self.stopToRoutes = defaultdict(list)
        routeIds = self.getAllTrainRouteIds() #get the unique ID for every route in the system.

        for route in routeIds:
            stopsOnRoute = self.getAllStopsOnRoute(route)
            self.routeToStops[route] = stopsOnRoute
            for stop in stopsOnRoute:
                self.stopToRoutes[stop].append(route)

    def prettyPrintResponse(self, response):
        '''
        Prints python response objects to the console in a human readable format. Helper function for debugging.
        Parameters:
            response (reqeusts.Response object) : A Python response object obtained with something like requests.get().
        '''
        print("Status Code: ", response.status_code)
        jsonData = json.loads(response.text)
        print(json.dumps(jsonData, indent=2))

    def getRouteToStopsDict(self):
        if(self.routeToStops == None):
            self.buildRouteAndStopRelationships()
        return self.routeToStops
    
    def getStopToRoutesDict(self):
        if(self.stopToRoutes == None):
            self.buildRouteAndStopRelationships()
        return self.stopToRoutes

    def __str__(self):
        return f"MBTA Requester object using API Key {self.apiKey}"

        


