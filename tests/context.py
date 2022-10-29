import os
import sys

#This file gives .py files in the tests directory the context they need to import files from TrainTracker. 

sys.path.insert(0,os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))