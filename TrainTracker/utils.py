from dotenv import load_dotenv
import os

def loadEnvironmentVariablesFromFile():
    '''
    Helper function to load environment variables from file.
    Looks for a file named .env in the same directory that this .py file is in.
    Then, loads the environment variables from this file into the current context.
    These will be accessible through functions like os.getenv().
    '''
    pathToThisDirectory = os.path.abspath(os.path.dirname(__file__))
    pathToEnvironmentFile = os.path.join(pathToThisDirectory, '.env')
    load_dotenv(pathToEnvironmentFile)