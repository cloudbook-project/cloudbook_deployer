import json
import loader

"""
	# example of what circle manager must return
	{
	"agent_id_0",
	"agent_id_1"
	}

	#example of du_list.json
	dus = {"du_0":{"cost":0, "size":100},
	"du_1":{"cost":1, "size":130},
	"du_2":{"cost":2, "size":50},
	"du_3":{"cost":5, "size":220},
	"du_4":{"cost":2, "size":110},
	"du_5":{"cost":3, "size":130},
	"du_6":{"cost":0, "size":110},
	}

	#example of agent_with_grant
	agents = { "agent_id_0": "LOW",
	"agent_id_1": "HIGH",
	"agent_id_2": "MEDIUM",
	"agent_id_3": "HIGH",
	"agent_id_4": "LOW",
	"agent_id_5": "HIGH",
	}

	#example of what deployer returns:
	{
	"du_0": {"agent_id_0", "agent_id_1", "agent_id_3"},
	"du_0": {"agent_id_0", "agent_id_2", "agent_id_5"}
	}
"""
#This function sorts dus in order of costs and size from smaller cost to higher cost.
def sort_dus(dus):
	dus_tmp={}
	#Count importance of every du to asign
	for du in dus:
		level = dus[du]["cost"] + dus[du]["size"]
		dus_tmp[du]=level
	dus_sorted = sorted(dus_tmp.items(), key=lambda kv: kv[1])
	#Format: [('du_2', 52), ('du_0', 100), ('du_6', 110)]
	# -> para obtener solo las dus:
	# dus = [x[0] for x in dus_sorted]
	return dus_sorted


#This function sorts agents in order of what they grant from smaller grant to higher grant.
#High grant means that the agent permits to cloudbook to use much of its computing capacity.
def sort_agents(agents_with_grant):
	agents_tmp={}
	#Order the agents by grant
	for agent in agents_with_grant:
		if agents_with_grant[agent] == "LOW":
			agents_tmp[agent]=1
		elif agents_with_grant[agent] == "MEDIUM":
			agents_tmp[agent]=2
		else:
			agents_tmp[agent]=3
	agents_sorted = sorted(agents_tmp.items(), key=lambda kv: kv[1])
	#format: [('agent_id_0', 1), ('agent_id_4', 1)] 
	# -> para obtener solo los agentes:
	# agentes = [x[0] for x in agents_sorted]
	return agents_sorted

#Assigns DUs to agents taking into account the cost each DU and the grant level of every agent.
def assign_dus_to_machines(circle_agents, agents_with_grant, dus):
	dus_sorted=sort_dus(dus)
	agents_sorted_by_grant=sort_agents(agents_with_grant)

	if(len(circle_agents) != len(agents_sorted_by_grant)):
		print("FATAL: circle agents number not coincident")
		return 0
	else:
		#Assign agents to dus: how to check assignment to do it correctly?

		result={}

		return result

	#ASSIGN MACHINES TO DUs

	# one machine runs only one agent
	# if we want more agents in the same machine, the machine must be repeated in the circle
	#print(dus)
	#ff= list(dus.keys())
	#num_agents = len(agents)

	#result={}
	#for i in range(0,num_agents):
	#	result[agents[i]]={}
	#	result[agents[i]]= ff[i]
	#return result

#Calls to Circle Management Service to obtain the circle info. From there, it takes the FS path.
def get_circle_info(circle_id):

	#Calls get_circle(circle_id) in Circle Management Service. It will return a json containing circle info.
	#From this JSON, we are getting the FS path (or URL)

	#url = "address to get the circle"+circle_id
    #	with urllib.request.urlopen(url) as res:
    #		data = json.loads(res.read().decode())
    #		FS = data["CIRCLE_INFO"]["DISTRIBUTED_FS"]
	#		return FS
	return		


#Performs full deployment and assignment of DUs to agents
def deploy(circle_id):

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
def deploy_local(agents_in_local_circle, path):

	data = json.load(agents_in_local_circle)

	agents_list = list(data.keys())
	
	res = assign_dus_to_machines(agents_list, agents_with_grant, dus)

	json_str = json.dumps(res)
	fo = open(path+"/cloudbook.json", 'w')
	fo.write(json_str)
	fo.close()

	return True



#This file must exist in the cloudbook folder, created by the Maker
dus=loader.load_dictionary("./du_list.json")

#This file must exit in the cloudbook folder, created by the agents.
agents_with_grant = loader.load_dictionary("./agents_grant.json")

#Get agents from Circle, for now, we're using a fake:
#Just an example of what circle manager must return
cloudbook_agents={
	"agent_id_0",
	"agent_id_1"
	}