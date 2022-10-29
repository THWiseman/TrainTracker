from mbta_requester import MBTARequester
import os
from dotenv import load_dotenv

def main():
	load_dotenv()
	requesterObject = MBTARequester()
	print(requesterObject)

if __name__ == "__main__":
	main()