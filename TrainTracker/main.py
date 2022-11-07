from utils import loadEnvironmentVariablesFromFile
import os
from transit_requester import TransitRequester
from questions import doQuestionOne, doQuestionTwo, doQuestionThree

def main():
	loadEnvironmentVariablesFromFile()

	requesterObject = TransitRequester( #build a requester object that uses the MBTA api. 
        os.getenv('MBTA_API_KEY'),
        os.getenv('MBTA_API_ENDPOINT'))

	doQuestionOne(requesterObject)
	doQuestionTwo(requesterObject)
	doQuestionThree(requesterObject)

if __name__ == "__main__":
	main()