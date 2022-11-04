def doQuestionOne(requesterObject):
	'''
	Answers question one in the takehome: List all of the long names of each subway route.
	Parameters: requesterObject that can be used to query the MBTA API.
	There were two ways to go about doing this question: Download all the results and then filter locally,
	or instead rely on the server API to filter before results are received. There are pros and cons to each
	approach, and I chose to filter using the server API.
	Pros to using the server API to filter:
		-Less data needs to be transmitted across the network, leading to a faster response.
		-No data needs to be stored or manipulated locally. This has two advantages: 
			-Less memory/CPU required by the server.
			-Less bugprone code. By not storing, mutating, and filtering any data locally, there is less chance
			of something incorrectly altering the data before we use it. This punts the responsiblity to the API,
			which has been much more rigourously tested than this python script. 
	Pros to downloading all data and filtering locally:
		-More flexibility with how we want to search/filter the response since we're not limited by the API.
			-For example, we can use familiar custom/python functions to filter/search data rather than hardcoding queries 
			to the MBTA API specification. This might make our code more reusable across different APIs.
		-Potentially fewer API requests in total, depending on how much we use the stored data.
		-Ability to store a complete copy of the API route data in our own database or memory.
			-Once the data is stored locally, we can use it as a cache to potentially prevent future API requests
			-We can access the data even if the API goes down temporarily.
	'''
	input("Press enter to see a list of all subway routes.")
	print("All subway routes in Boston: ")
	print(requesterObject.getAllTrainRouteNames())

def doQuestionTwo(requesterObject):
	'''
	Answers question two on the takehome. 
	Parameters: 
		requesterObject (MBTARequester): Object that can be used to query the MBTA API.
	'''
	input("Press enter to see the routes with the most and fewest stops.")
	longestRoute = None
	numStopsOnLongestRoute = None
	shortestRoute = None
	numStopsOnShortestRoute = None
	routeToStopsDict = requesterObject.getRouteToStopsDict()
	for route in routeToStopsDict.keys(): #Iterate through all routes and find which ones are the longest and shortest. 
		numStops = len(requesterObject.routeToStops[route])
		if(longestRoute == None or numStops > numStopsOnLongestRoute):
			longestRoute = route
			numStopsOnLongestRoute = numStops
		if(shortestRoute == None or numStops < numStopsOnShortestRoute):
			shortestRoute = route
			numStopsOnShortestRoute = numStops
	print(f"The longest route is {longestRoute} with {numStopsOnLongestRoute} stops.")
	print(f"The shortest route is {shortestRoute} with {numStopsOnShortestRoute} stops.")
	input("Press enter to see a list of the stops that connect two or more routes.")
	stopToRoutesDict = requesterObject.getStopToRoutesDict()
	for stop in stopToRoutesDict.keys(): #Iterate through all stops and find which ones are on more than one route. 
		if(len(requesterObject.stopToRoutes[stop]) > 1):
			print(f"The stop {stop} connects: {requesterObject.stopToRoutes[stop]}")

def isValidStopName(requesterObject, stopName):
	for stop in requesterObject.stopToRoutes.keys():
		if(stopName == stop):
			return True
	return False

def getStopFromUserInput(requesterObject):
	while(True):
		userInput = input("Subway stop or EXIT:")
		if(userInput.lower() == "exit"):
			print("Terminating program")
			exit(0)
		if(isValidStopName(requesterObject, userInput)):
			return userInput
		else:
			print("Invalid input. Try again.")

def getListOfRoutesThatConnectTwoStops(requesterObject, stopA, stopB):
	'''
	Helper function for question three. This function will use the dictionaries of the requester object to determine
	which route(s) connect stopA and stopB.
	'''

def buildRouteConnectionGraph(requesterObject):
    '''
    Here we build a graph where each node is a subway route, and each edge is a stop that connects two routes.
    We assume that each edge is bidirectional, i.e. if you can get from Route A to Route B through stop X, you can
    also get from Route B to Route A through the same stop. 
    We'll represent the graph as a dictionary, where each key is a route and each value is a list of routes that the key is 
    directly connected to. We wont be storing data about the stops that connect the routes for the sake of simplicity.
    Parameters: 
        requesterObject (MBTARequester): Object that can be used to query the MBTA API.
    Returns: 
        routeConnectionGraph dict[str,list[str]]: A dictionary that represents the connections between subway routes. 
    '''
    routeConnectionGraph = dict() #initialize the routeConnectionGraph with key/value pairs of routeId/empty list. 
    routeIds = requesterObject.getAllTrainRouteIds()
    for route in routeIds:
        routeConnectionGraph[route] = []
        
    stopToRoutesDict = requesterObject.getStopToRoutesDict()

    for stop in stopToRoutesDict.keys(): #Iterate through all stops and find which ones are on more than one route.
        routesOnStop = stopToRoutesDict[stop] #the routes associated with this stop
        if(len(routesOnStop) > 1): #if a stop is on more than one route, create graph edges between each of those routes
            for route in routesOnStop:
                routeConnectionGraph[route] = routeConnectionGraph[route] + routesOnStop
    
    for route in routeConnectionGraph:
        routeConnectionGraph[route] = [*set(routeConnectionGraph[route])] #remove all duplicates from the list
        isNotSelf = lambda x: x is not route
        routeConnectionGraph[route] = [ x for x in routeConnectionGraph[route] if x is not route ] #remove all references to self from the list. 

    print(routeConnectionGraph)
        


def doQuestionThree(requesterObject):
	'''
	Answers question two on the takehome. 
	Parameters: 
		requesterObject (MBTARequester): Object that can be used to query the MBTA API.
	'''
	print("Enter the name of two subway stops. I'll tell you which route(s) you'll need to get from stop A to stop B")
	continueInputLoop = True
	while(continueInputLoop):
		print("Enter the name for stop A:")
		stopA = getStopFromUserInput(requesterObject)
		print("Enter the name for stop B:")
		stopB = getStopFromUserInput(requesterObject)
		print(f"Stop A: {stopA}  Stop B: {stopB}")
	

