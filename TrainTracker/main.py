from mbta_requester import MBTARequester
from questions import doQuestionOne, doQuestionTwo, doQuestionThree, buildRouteConnectionGraph
from utils import loadEnvironmentVariablesFromFile


def main():
	loadEnvironmentVariablesFromFile()
	requesterObject = MBTARequester()

	#doQuestionOne(requesterObject)
	#doQuestionTwo(requesterObject)
	doQuestionThree(requesterObject)

if __name__ == "__main__":
	main()