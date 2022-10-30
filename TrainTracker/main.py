from mbta_requester import MBTARequester
from utils import loadEnvironmentVariablesFromFile

def main():
	loadEnvironmentVariablesFromFile()
	requesterObject = MBTARequester()
	
	#Question 1:
	print("Question 1: List of Subway Routes")
	print(requesterObject.getAllTrainRouteNames())

if __name__ == "__main__":
	main()