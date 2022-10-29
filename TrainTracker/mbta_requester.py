import os
from dotenv import load_dotenv

class MBTARequester:
    def __init__(self):
        self.loadEnvironmentVariables()
        self.apiKey = os.getenv('MBTA_API_KEY')

    def __str__(self):
        return f"MBTA Requester object using API Key {self.apiKey}"

    def loadEnvironmentVariables(self):
        '''
        Looks for a file named .env in the same directory that this .py file is in.
        Then, assuming that .env file is a correctly formatted environment variable file,
        this will load the contents into the current context, accessible through
        functions like os.environ.get().
        '''
        pathToThisDirectory = os.path.abspath(os.path.dirname(__file__))
        pathToEnvironmentFile = os.path.join(pathToThisDirectory, '.env')
        load_dotenv(pathToEnvironmentFile)

