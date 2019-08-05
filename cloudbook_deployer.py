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




'''
def assign_dus_to_machines(circle_agents, agents_with_grant, dus, agent0,configuration = None):
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
		if a=="agent_0": # or a == agent0:
			#print "agent0 found"
			try:
				result[du0].append(a)
			except:
				result[du0]=[]	
				result[du0].append(a)
			agents_with_grant[a]=int(agents_with_grant[a])-int(dus[du0]["cost"]+dus[du0]["size"])
			dus[du0]["cost"]=0
			dus[du0]["size"]=0
			break
			#print "choosen DU:",dus[du0]
			#print "choosen agent:",agents_with_grant[a]
	print ("el agente 0 es: ",agent0, " y carga la du: ", du)

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
		dus[max_du]["size"]=0
		

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
'''


'''
This function assigns the existing DUs to the agents defined in agents_grant.json. The assignment is done in the following manner:
If there is the same number of DUs and agents:
	- du_0 is assigned to agent_0
	- The rest of DUs are sorted from higher to lower cost and assigned to the agents sorted from higher to lower grant
If there are less DUS than agents:
	- du_0 is assigned to agent_0
	- The rest of DUs are sorted from higher to lower cost and assigned to the agents sorted from higher to lower grant, stopping when
	running out of DUs.
If there are more DUS than agents:
	- du_0 is assigned to agent_0
	- NEEDS TO BE DECIDED WHAT TO DO (NOT IMPLEMENTED YET)
'''
def assign_dus_to_machines(circle_agents, agents_with_grant, dus, agent0, configuration = None):
	print ("ENTER in assign_dus_to_machines()...")


 


	#translate grant cualitative values into numerical values
	for a in agents_with_grant:
		if agents_with_grant[a]=="HIGH":
			agents_with_grant[a]=3
		elif agents_with_grant[a]=="MEDIUM":
			agents_with_grant[a]=2
		else:
			agents_with_grant[a]=1

	print "dictionaries:"
	print("\ndus"); print(dus)
	print("\nagents_with_grant"); print(agents_with_grant)

	print("\nSorting agents...")
	sorted_agents_with_grant = sorted(agents_with_grant.items(), key=operator.itemgetter(1))
	sorted_agents_with_grant = sorted_agents_with_grant[::-1] #reverse the list to have the higher grants first
	print("\nsorted_agents_with_grant"); print(sorted_agents_with_grant)

	dus_with_cost = {}
	for du in dus:
		dus_with_cost[du] = dus[du]['cost']+dus[du]['size'] #the complexity and size of the du code is used as cost
	#print("\ndus_with_cost"); print(dus_with_cost)

	print("\nSorting DUs...")
	#this sort operation transform a dictionary into a list, because a dictionary has not order
	sorted_dus_with_cost = sorted(dus_with_cost.items(), key=operator.itemgetter(1))
	sorted_dus_with_cost = sorted_dus_with_cost[::-1] #reverse the list to have the higher costs first
	print("\nsorted_dus_with_cost"); print(sorted_dus_with_cost)

	result = {}
	# initialization assigning du_0 to agent_0
	result['du_0'] = ['agent_0']
	
	
	
	#set du0 cost to zero
	for i in range(0,len(sorted_dus_with_cost)):
		#convert each tuple in a list
		sorted_dus_with_cost[i]=list(sorted_dus_with_cost[i])
		if sorted_dus_with_cost[i][0]=='du_0':
			#print "el coste de la du0 es ",sorted_dus_with_cost[i][1]
			sorted_dus_with_cost[i][1]=0
			du_0_cost=dus['du_0']['cost']+dus['du_0']['size']
			dus['du_0']['cost']=0 # update dictionary cost
			dus['du_0']['size']=0 # update dictionary size
			
			#sorted_dus_with_cost.pop(i) # pop it because is yet inserted
			#print("popped du_0");
	
	#reduce numerical value of grant of agent_0 according with du0 cost
	for i in range(0,len(sorted_agents_with_grant)):
		#convert each tuple in a list
		sorted_agents_with_grant[i]=list(sorted_agents_with_grant[i])
		if sorted_agents_with_grant[i][0]=='agent_0':
			sorted_agents_with_grant[i][1]=sorted_agents_with_grant[i][1]-du_0_cost
			agents_with_grant['agent_0']=agents_with_grant['agent_0']-du_0_cost # update dictionary
			#sorted_agents_with_grant.pop(i) # pop it because is yet inserted
			#print("popped agent_0");

	# assign one du to each agent (agents>dus) or one agent to each du (dus>agents)	
	print 
	print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	print " 1st round --- assigning one du to each agent ---"
	print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	agent_index=0
	for i in range(0,min (len(sorted_dus_with_cost), len(sorted_agents_with_grant))):
		if sorted_dus_with_cost[i][1]==0 :
			print " DU" , sorted_dus_with_cost[i][0]," has cost zero"
			continue;
		print("du -> ", sorted_dus_with_cost[i])
		if sorted_agents_with_grant[agent_index][0]=="agent_0":
			agent_index+=1
		print("agent -> ",sorted_agents_with_grant[agent_index])
		result[sorted_dus_with_cost[i][0]] = [sorted_agents_with_grant[agent_index][0]]
		#reduction of agent grant and update cost of DU to zero 
		du_name= sorted_dus_with_cost[i][0]
		du_cost=dus[du_name]['cost']+dus[du_name]['size']
		sorted_agents_with_grant[i][1]=sorted_agents_with_grant[agent_index][1]-du_cost
		agent_name =sorted_agents_with_grant[i][0]
		agents_with_grant[agent_name]=agents_with_grant[agent_name]-du_cost #dict
		sorted_dus_with_cost[i][1]=0 # set cost to zero
		dus[sorted_dus_with_cost[i][0]]['cost']=0 # update dictionary
		dus[sorted_dus_with_cost[i][0]]['size']=0 # update dictionary
		
		agent_index+=1

	print "1st round result: "
	print("\n\nRESULT 1st round:"); print(result)
	print 
	print "--- dus ---"
	print sorted_dus_with_cost
	print "--- agents ---"
	print sorted_agents_with_grant
	print
	print "diccionarios:"
	print dus
	print agents_with_grant


	print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	print " 2nd round --- assigning rest of DUs to agents according their power ---"
	print "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
	# now we proceed to assign the rest of DUs to the available agents according with power
	total_dus=len(dus)
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
		print "the max costly DU is ", max_du

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
		du_name=max_du
		print "choosen agent:",max_agent,agents_with_grant[max_agent]
		agent_name= max_agent
		
		result [du_name]=agent_name
		agents_with_grant[agent_name]= agents_with_grant[agent_name]- maxcost #update dictionary
		dus[du_name]['cost']=0 # update dictionary
		dus[du_name]['size']=0 # update dictionary

	print "diccionarios:"
	print dus
	print agents_with_grant

	print("\n\nRESULT 2nd round:"); print(result)
	
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
	print ("ENTER in deploy_local()...")
	#transform str (in json format) into dictionary with pairs agent, grant
	data = json.loads(agents_in_local_circle)

	#create a list of agents without grant
	agents_list = list(data.keys())
	print ("list of agents:")
	print (agents_list)
	agent0 = "agent_0"
	if agent0 not in agents_list:
		agent0 = agents_list[0]
		print "ERROR!!. there is not agent_0 ", agent0 ,"will be used as agent_0"

	#assign DUs to machines
	#-----------------------
	# NOTE: both variables "agents_with_grant and dus are global, not need to be passed"
	res = assign_dus_to_machines(agents_list, agents_with_grant, dus, agent0)
	
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
print ("              (for example, c:/users/myuser/cloudbook")
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



