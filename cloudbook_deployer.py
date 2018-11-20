import json
import loader

"""
	# example of what circle manager must return
	{
	"agent_id_0",
	"agent_id_1"
	}

	#example of du_list.json
	{
	"du_0":{"cost":0, "size":100},
	"du_1":{"cost":1, "size":130}
	}

	#example of agent_with_grant
	{
	"agent_id_0": "LOW",
	"agent_id_1": "HIGH"
	}

	#example of what deployer returns:
	{
	"du_0": {"agent_id_0", "agent_id_1", "agent_id_3"},
	"du_0": {"agent_id_0", "agent_id_2", "agent_id_5"}
	}
"""

def sort_dus(dus):
	dus_tmp={}
	#Count importance of every du to asign
	for du in dus:
		level = dus[du]["cost"] + dus[du]["size"]
		dus_tmp[du]=level
	dus_sorted = sorted(dus_tmp.items(), key=lambda kv: kv[1])
	return dus_sorted

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
	return agents_sorted

def assign_dus_to_machines(circle_agents, agents_with_grant, dus):

	dus_sorted=sort_dus(dus)
	agents_sorted_by_grant=sort_agents(agents_with_grant)

	if(len(circle_agents) != len(agents_sorted_by_grant)):
		print("FATAL: circle agents number not coincident")
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


#Performs full deployment and assignment of DUs to agents
def deploy(circle_id):

	#Calls get_circle_agents(circle_id) in Circle Management Service. It will return the list of agents
	#I suppose that the circle manager will return a JSON file
	
	#url = "address to get the circle"+circle_id
    #    with urllib.request.urlopen(url) as res:
    #        data = json.loads(res.read().decode())
    #        agents_list = list(data.keys())

	#By now, we will work with the fake "cloudbook_agents" list
	agents_list = list(cloudbook_agents)
	
	res = assign_dus_to_machines(agents_list, agents_with_grant, dus)

	json_str = json.dumps(res)
	fo = open("../cloudbook_deployer/prueba.json", 'w')
	fo.write(json_str)
	fo.close()

	return True


#Performs full deployment and assignment of DUs to agents
def deploy_local(agents_in_local_circle):

	data = json.load(agents_in_local_circle)

	agents_list = list(data.keys())
	
	res = assign_dus_to_machines(agents_list, agents_with_grant, dus)

	json_str = json.dumps(res)
	fo = open("../cloudbook_deployer/prueba.json", 'w')
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