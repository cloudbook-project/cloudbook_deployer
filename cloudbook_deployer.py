import json
import loader


cloudbook_agents={
	"agent_0" : {"127.0.0.1":["du_0"]},
	"agent_1" : {"127.0.0.1":["du_1"]}
}

cloudbook_dus={
	"du_0" : ["agent_0"],
	"du_1" : ["agent_1"]
}

def assign_dus_to_machines(machines, dus):
	
	# example of circle.json
	"""
	{
	"127.0.0.1":{"RAM": 100, "CPU": 2},
	"127.0.0.1":{"RAM": 1000, "CPU": 1}
	}
	"""
	#example of du_list.json
	"""
	{
	"du_0":{"cost":0, "size":100},
	"du_1":{"cost":1, "size":130}
	}
	"""

	# one machine runs only one agent
	# if we want more agents in the same machine, the machine must be repeated in the circle
	du_list= dus.keys()
	machine_list= machines.keys()
	num_agents=len (machine_list)

	result={}
	for i in range(0,num_agents):
		agent_name="agent_"+str(i)
		result[agent_name]={}
		result[agent_name][machine_list[i]]=[]
		result[agent_name][machine_list[i]].append(du_list[i])
	return result



# asign 
machines=loader.load_dictionary("./circle.json")
dus=loader.load_dictionary("./du_list.json")

cloudbook_agents= assign_dus_to_machines(machines, dus)




json_str = json.dumps(cloudbook_agents)
fo = open("../cloudbook_agent/du_files/cloudbook_agents.json", 'w')
fo.write(json_str)
fo.close()

json_str = json.dumps(cloudbook_dus)
fo = open("../cloudbook_agent/du_files/cloudbook_dus.json", 'w')
fo.write(json_str)
fo.close()

