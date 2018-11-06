import json
import loader

"""
	# example of what circle manager must return

	{
	"agent_id_0" : {some stuff about the agent, for future use},
	"agent_id_1" : {some stuff about the agent, for future use}
	}


	#example of du_list.json

	{
	"du_0":{"cost":0, "size":100},
	"du_1":{"cost":1, "size":130}
	}
	"""

#This file must exist in the cloudbook folder, created by the Maker
dus=loader.load_dictionary("./du_list.json")

#Just an example of what circle manager must return
cloudbook_agents={
	"agent_id_0" : {},
	"agent_id_1" : {}
}


def assign_dus_to_machines(machines, dus):

	# one machine runs only one agent
	# if we want more agents in the same machine, the machine must be repeated in the circle
	print(dus)
	ff= list(dus.keys())
	num_agents = len(machines)

	result={}
	for i in range(0,num_agents):
		result[machines[i]]={}
		result[machines[i]]= ff[i]
	return result


#Performs full deployment and assignment of DUs to agents
def deploy(circle_id):

	#Calls get_circle_agents(circle_id) in Circle Management Service. It will return the list of agents
	#I suppose that the circle manager will return a JSON file
	
	#url = "address to get the circle"+circle_id
    #    with urllib.request.urlopen(url) as res:
    #        data = json.loads(res.read().decode())
    #        agents_list = list(data.keys())

	#By now, we will work with the fake "cloudbook_agents" list
	agents_list = list(cloudbook_agents.keys())
	
	res = assign_dus_to_machines(agents_list, dus)

	json_str = json.dumps(res)
	fo = open("../cloudbook_deployer/prueba.json", 'w')
	fo.write(json_str)
	fo.close()

	return True


#Performs full deployment and assignment of DUs to agents
def deploy_local(agents_in_local_circle):

	data = json.load(agents_in_local_circle)

	agents_list = list(data.keys())
	
	res = assign_dus_to_machines(agents_list, dus)

	json_str = json.dumps(res)
	fo = open("../cloudbook_deployer/prueba.json", 'w')
	fo.write(json_str)
	fo.close()

	return True

deploy(000)
