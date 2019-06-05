import json
import loader
import operator
import platform
import os
import sys

"""
	
#example of du_list.json
dus = {"du_0":{"cost":0, "size":280},
"du_1":{"cost":0, "size":260},
"du_2":{"cost":0, "size":300},
"du_3":{"cost":0, "size":310},
"du_4":{"cost":0, "size":90},
"du_5":{"cost":0, "size":120},
"du_6":{"cost":0, "size":50},
"du_7":{"cost":0, "size":210}
}

#example of agent_with_grant
agents = { "agent_id_0": "LOW",
"agent_id_1": "LOW",
"agent_id_2": "HIGH",
"agent_id_3": "MEDIUM",
"agent_id_4": "HIGH",
"agent_id_5": "MEDIUM",
}

	#example of what deployer returns:
	{
	"du_0": {"agent_id_0", "agent_id_1", "agent_id_3"},
	"du_0": {"agent_id_0", "agent_id_2", "agent_id_5"}
	}
"""





def assign_dus_to_machines(circle_agents, agents_with_grant, dus, configuration = None):
	print ("ENTER in assign_dus_to_machines()...")	
	#dus_sorted=sort_dus(dus) # this is a list of tuples
	#agents_sorted_by_grant=sort_agents(agents_with_grant) # this is a list of tuples

	#print "sorted dus: ",dus_sorted
	#print "sorted agents: ",agents_sorted_by_grant
	

	#Assign agents to dus.
	#In this case, we're assigning agents to DUs by looking to the most optimal performance.
	#We assume that LOW means 100 points, MEDIUM 200 points and HIGH 300 points.
	#Each DU has a number of performance points assigned. When we distribute DUs amongs agents, we substract the performance of 
	# every agent to the performance of every DU, assigning it when the value is closest to zero. We do this in every case.
	#With this method we are always assigning every DU to an agent, no matter if there are more DUs that agents.
	
	result = {}
	total_dus=len(dus)
	print "  there are ", total_dus," DUs"
	print "  dus", dus
	print "  agents",agents_with_grant


	for a in agents_with_grant:
		if agents_with_grant[a]=="HIGH":
			agents_with_grant[a]=500
		elif agents_with_grant[a]=="MEDIUM":
			agents_with_grant[a]=200	
		else:
			agents_with_grant[a]=100	

	# assign the DU0 to the agent0 
	#------------------------------
	print (" always DU0 is assigned to agent0 ")
	for du in dus:
		if du=="du_0":
			du0=du
			#print "du_0 found"
			break

	for a in agents_with_grant:
		if a=="AGENT0":
			#print "agent0 found"
			try:
				result[du0].append(a)
			except:
				result[du0]=[]	
				result[du0].append(a)
			agents_with_grant[a]=int(agents_with_grant[a])-int(dus[du0]["cost"]+dus[du0]["size"])
			dus[du0]["cost"]=0
			break
			#print "choosen DU:",dus[du0]
			#print "choosen agent:",agents_with_grant[a]

	for i in range(0,total_dus):
		#----------------------------------------------
		# search most costly DU, then search the most powerfull agent
		# assign the DU to the agent and reduce the power of the agent
		# delete the DU from du list
		# repeat the process till none DU is remaining 
		#-----------------------------------------------
		maxcost=0
		for du in dus:
			if (dus[du]["cost"]+dus[du]["size"]>=maxcost):
				max_du=du
				maxcost=dus[du]["cost"]+dus[du]["size"]

		if maxcost==0:
			break
		#print "the max costly DU is ", max_du

		#search the most powerfull agent
		max_power=-100000000
		max_agent="";
		for a in agents_with_grant:
			if (int(agents_with_grant[a])>max_power):
				#print a,agents_with_grant[a]
				max_agent=a
				max_power=agents_with_grant[a]

		#print "the most powerfull agent is ", max_agent, agents_with_grant[max_agent]
		

		if (max_agent==""):
			print ("  failure searching the most powefull agent")
			return False

		
		#if (int(agents_with_grant[max_agent])<int (dus[max_du]["cost"]+dus[max_du]["size"])):
		#	return False
		

		# we assign the most costly DU to the most powerfull agent
		# ----------------------------------------------------------
		print "choosen DU:",max_du,dus[max_du]
		print "choosen agent:",max_agent,agents_with_grant[max_agent]
		#print "power es ", agents_with_grant[max_agent]
		#print "le restamos ",dus[max_du]
		agents_with_grant[max_agent]=int(agents_with_grant[max_agent])-int(dus[max_du]["cost"]+dus[max_du]["size"])
		dus[max_du]["cost"]=0
		

		try:
			result[max_du].append(max_agent)
		except:
			result[max_du]=[]	
			result[max_du].append(max_agent)
		#print(chosen_agent, agents_sorted_by_grant[chosen_agent])




	#TODO: Make this properly, temporal assignation of du_0
	"""
	aux_value = ""
	print "===Correct du assignation==="
	for key, value in result.iteritems():
		if (key == "du_0") and (value != ["agent0"]):
			aux_value= value
			result[key] = ["agent0"]
			
		if (value == ["agent0"]) and (key != "du_0"):
			result[key] = aux_value
	"""
	print "result is", result

	return result

#Calls to Circle Management Service to obtain the circle info. From there, it takes the FS path.
def get_circle_info(circle_id, configuration = None):

	#Calls get_circle(circle_id) in Circle Management Service. It will return a json containing circle info.
	#From this JSON, we are getting the FS path (or URL)

	#url = "address to get the circle"+circle_id
    #	with urllib.request.urlopen(url) as res:
    #		data = json.loads(res.read().decode())
    #		FS = data["CIRCLE_INFO"]["DISTRIBUTED_FS"]
	#		return FS
	return		


#Performs full deployment and assignment of DUs to agents
def deploy(circle_id, configuration = None):

	#Calls get_circle_agents(circle_id) in Circle Management Service. It will return the list of agents
	#I suppose that the circle manager will return a JSON file
	#Also, we'll need the CIRCLE_INFO.json file to check the FS path
	
	#url = "address to get the circle"+circle_id
    #    with urllib.request.urlopen(url) as res:
    #        data = json.loads(res.read().decode())
    #        agents_list = list(data.keys())

	#Remember to load CIRCLE_INFO to get FS path

	#By now, we will work with the fake "cloudbook_agents" list
	agents_list = list(cloudbook_agents)
	
	res = assign_dus_to_machines(agents_list, agents_with_grant, dus)

	json_str = json.dumps(res)
	fo = open("../cloudbook_deployer/prueba.json", 'w')
	fo.write(json_str)
	fo.close()

	return True


#Performs full local deployment and assignment of DUs to agents
def deploy_local(agents_in_local_circle, path, configuration = None):

	#transform str (in json format) into dictionary with pairs agent, grant
	data = json.loads(agents_in_local_circle)

	#create a list of agents without grant
	agents_list = list(data.keys())
	print ("list of agents:")
	print (agents_list)

	#assign DUs to machines
	#-----------------------
	# NOTE: both variables "agents_with_grant and dus are global, not need to pass"
	res = assign_dus_to_machines(agents_list, agents_with_grant, dus)
	
	#write output file in json format
	#---------------------------------
	json_str = json.dumps(res)
	fo = open(output_dir+"/cloudbook.json", 'w')
	fo.write(json_str)
	fo.close()

	return True

def load_dictionary(filename):
	'''This function is used for getting the info coming from de config file'''
	with open(filename, 'r') as file:
		aux = json.load(file)
	return aux


#main program to execute by command line
#=======================================
print ("Welcome to cloudbook deployer  (V1.0)")
print ("=====================================")
print (" usage :")
print ("   python deploy.py [-mode local|service]")
print ("  ")	
print (" Prerequisites:")
print (" 1. default folder must exist:")
print ("    - windows: $HOMEDRIVE/$HOMEPATH/cloudbook/")
print ("    - linux: /etc/cloudbook/")
print (" 2. input files must exist at default folder:")
print ("    - config.json : common for all cloudbook components")
print ("    - du_list.json : created by cloudbook maker component")
print ("    - agents_grant.json : provided by agents")
print (" ")
print (" Output files:")
print ("  - cloudbook.json: this file contains the assignment of DUs to agents")
print ("=======================================")
print ( "")


# access to default directory or create it, if it does not exist
#------------------------------------------------------------
input_dict = load_dictionary("./config.json")
if input_dict["circle_info"]["DISTRIBUTED_FS"] == "":
	if(platform.system()=="Windows"):
	    path= os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']+"/cloudbook/"
	    if not os.path.exists(path):
	        os.makedirs(path)
	else:
	    path = "/etc/cloudbook/"
	    if not os.path.exists(path):
	        os.makedirs(path)
else:
	path = input_dict["circle_info"]["DISTRIBUTED_FS"] 

#the input and output path is the same
#-------------------------------------
input_dir = path + os.sep + "distributed"
output_dir = path + os.sep + "distributed"

#This file must exist in the cloudbook folder, created by the Maker
#-------------------------------------------------------------------
dus=loader.load_dictionary(input_dir+"/du_list.json")

#This file must exit in the cloudbook folder, created by the agents
#-------------------------------------------------------------------
agents_with_grant = loader.load_dictionary(input_dir+"/agents_grant.json")


# in "service" working mode, the agents must be requested to the circle manager service
# in "local" mode, we use angents_grant.json
#------------------------------------------------------------------------------------
# example of agents_grant.json
#  {
#  "AGENT0":"MEDIUM",
#  "AGENT1":"LOW",
#  "AGENT2":"LOW"
#  }

mode="local"
num_param=len(sys.argv)
if num_param==3 :
	if sys.argv[1]=="-mode":
		mode=sys.argv[2]
		

print ("working mode:"), mode

if mode=="local":
	#all content is loaded as single string into a variable.
	agents_in_local_circle=json.dumps(agents_with_grant)
else:
	print ("Service mode is not supported in this version")
	sys.exit()



print ("Agents in local circle:")
print agents_in_local_circle

#this is the most important function of deployer
#-----------------------------------------------
deploy_local(agents_in_local_circle, ".", configuration = None)



