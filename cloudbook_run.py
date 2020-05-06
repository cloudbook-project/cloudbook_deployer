# cloudbook_run.py

# This file retrieves the agent_0 information to call main() function in du_0 to launch the user program.

# Usage:
#   python3 cloudbook_run.py -project_folder <project_folder>



#####   IMPORTS   #####
import loader
import os
import sys
import platform
from pathlib import Path
import requests



#####   MAIN   #####
if __name__ == "__main__":

	# Process input parameters
	project_folder = ""
	num_param = len(sys.argv)
	for i in range(1, len(sys.argv)):
		if sys.argv[i]=="-project_folder":
			project_folder=	sys.argv[i+1]
			i = i+1

	if project_folder=="":
		print ("option -project_folder missing")
		sys.exit(0)

	# Variable for the path to cloudbook
	if platform.system()=="Windows":
		cloudbook_path = os.environ['HOMEDRIVE'] + os.environ['HOMEPATH'] + os.sep + "cloudbook"
	else:
		cloudbook_path = os.environ['HOME'] + os.sep + "cloudbook"

	# The path to the necessary folders
	project_path = cloudbook_path + os.sep + project_folder
	agents_grant_path = project_path + os.sep + "distributed" + os.sep + "agents_grant.json"
	running_path = project_path + os.sep + "distributed" + os.sep + "RUNNING"
	cloudbookjson_path = project_path + os.sep + "distributed" + os.sep + "cloudbook.json"

	# Load agent_0 ip and port
	agent0_ip_and_port = ""
	try:
		agents_grant_dict = loader.load_dictionary(agents_grant_path)
		agent0_ip_and_port = agents_grant_dict['agent_0']['IP']+":"+str(agents_grant_dict['agent_0']['PORT'])
		print("Detected agent_0 is available at:", agent0_ip_and_port)
	except:
		print("\nERROR: IP or port for agent_0 is unknown, and execution could not start. See agents_grant.json\n")
		os._exit(1)

	# Create RUNNING file
	Path(running_path).touch(exist_ok=True)

	# Launch the user program by sending a request to the agent_0, which starts the main() function
	response = requests.Session().get("http://" + agent0_ip_and_port + "/invoke?invoked_function=du_0.main")
	print("The program has ended.")

	# Remove RUNNING and cloudbook.json files (user program has ended)
	if os.path.exists(running_path):
		os.remove(running_path)
	if os.path.exists(cloudbookjson_path):
		os.remove(cloudbookjson_path)

	# Print the result returned by main() function in the user program
	try:
		readed_response = response.json()
	except:
		print("The program did not return anything.")
		os.exit(0)
	
	try:
		print(eval(readed_response))
	except:
		print(readed_response)
