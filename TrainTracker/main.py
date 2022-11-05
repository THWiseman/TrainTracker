from utils import loadEnvironmentVariablesFromFile
from transit_requester import TransitRequester
from questions import doQuestionOne, doQuestionTwo, doQuestionThree

def main():
	loadEnvironmentVariablesFromFile()
	requesterObject = TransitRequester()
	doQuestionOne(requesterObject)
	doQuestionTwo(requesterObject)
	doQuestionThree(requesterObject)

if __name__ == "__main__":
	main()