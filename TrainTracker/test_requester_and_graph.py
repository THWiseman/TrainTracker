import pytest
import os
from TrainTracker.transit_requester import TransitRequester
from TrainTracker.utils import loadEnvironmentVariablesFromFile
from TrainTracker.questions import findShortestPathBFS, isValidStopName, buildRouteConnectionGraph

class TestTransitRequester:
    '''
    This class will run a few tests to make sure our TransitRequester class is working properly. 
    We're not testing the external API here, and we're aware that the results of that API may change over time.
    This mostly serves as a sanity check that we didn't break anything when adding features to the class.
    '''
    def test_load_env(self): #Test to make sure loading environment variables from file is working
        loadEnvironmentVariablesFromFile()
        assert os.getenv('MBTA_API_ENDPOINT') == "https://api-v3.mbta.com"

    def test_construction(self): #Test to make sure the transit requester object is properly initialized
        self.requesterObject = TransitRequester()
        assert self.requesterObject.__str__() == "Transit Requester object using API Endpoint https://api-v3.mbta.com"
        assert self.requesterObject.routeToStops == None
        assert self.requesterObject.stopToRoutes == None

    def test_basic_api_request(self): #Test that we can successfully make a basic API call. We're not trying to test the external API here, so we just call something simple. 
        self.requesterObject = TransitRequester()
        routes = self.requesterObject.getAllTrainRouteNames()
        assert 'Red Line' in routes
    
    def test_route_relationship_builder(self):
        self.requesterObject = TransitRequester()
        self.requesterObject.buildRouteAndStopRelationships()
        stopToRoutes = self.requesterObject.stopToRoutes
        routeToStops = self.requesterObject.routeToStops
        assert len(stopToRoutes.keys()) > len(routeToStops.keys()) #There should always be strictly more stops than routes, or else something is wrong. 
        assert 'Kendall/MIT' in routeToStops['Red'] #Make sure the red line is a route from Kendall/MIT
        assert 'Red' in stopToRoutes['Kendall/MIT'] #Make sure that Kendall/MIT is on the red line

    def test_result_caching(self):
        self.requesterObject = TransitRequester()
        assert self.requesterObject.stopToRoutes == None
        self.requesterObject.getStopToRoutesDict() #Make sure that after we call the getter that the results stay cached as a member variable
        assert self.requesterObject.stopToRoutes != None
        assert 'Cleveland Circle' in self.requesterObject.stopToRoutes.keys()
        assert 'Green-C' in self.requesterObject.stopToRoutes['Cleveland Circle']

class TestQuestions:
    '''
    This class will make sure that the input validation and graph building/traversal functions are working as expected.
    These aren't rigourous unit tests meant to handle every edge case, but rather tests of essential functionality to make sure
    that stuff is working as expected during development. 
    '''
    def test_input_validation(self):
        self.requesterObject = TransitRequester()
        invalidInputs = ["", None, "12345", 0, "0", -1, "-1", 1, "1", dict(), "\n", "\t", 'Redd Line', 'OOrange']
        for input in invalidInputs:
            assert isValidStopName(self.requesterObject, input) == False
        validInputs = ["Kendall/MIT", "Central", "Cleveland Circle", "Fenway"]
        for input in validInputs:
            assert isValidStopName(self.requesterObject,input)
    
    def test_build_graph(self):
        self.requesterObject = TransitRequester()
        graph = buildRouteConnectionGraph(self.requesterObject)
        assert 'Red' in graph.keys()
        assert 'Orange' in graph['Red']
        assert 'Kendall/MIT' not in graph.keys()

    def test_bfs_traversal(self):
        #Can we handle cycles in the graph?
        graph = {
            "1" : ["2", "3"],
            "2" : ["1", "3"],
            "3" : ["1", "2"]
        } 
        assert findShortestPathBFS(graph, "1", "2") == ["1", "2"]

        #Can we handle an empty graph?
        graph = {} 
        assert findShortestPathBFS(graph, "1", "2") == []

        #Can we handle when start and stop are the same?
        graph = {
            "1" : ["2", "3"],
            "2" : ["1", "3"],
            "3" : ["1", "2"]
        }
        assert findShortestPathBFS(graph, "1", "1") == ["1"]

        #Can we find the shortest path when it requires multiple hops?
        graph = {
            "1" : ["2", "3"],
            "2" : ["4"],
            "3" : ["1"],
            "4" : ["2", "5"],
            "5" : ["4"]
        }
        assert findShortestPathBFS(graph, "1", "5") == ["1", "2", "4", "5"]

        #Can we handle the case where no path exists?
        graph = {
            "1" : ["2", "3"],
            "2" : ["1"],
            "3" : ["1"],
            "4" : ["5"],
            "5" : ["4"]
        }
        assert findShortestPathBFS(graph, "1", "5") == []