import json
import loader

"""
	# example of what circle manager must return
	{
	"agent_id_0",
	"agent_id_1"
	}
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
"""
	#example of what deployer returns:
	{
	"du_0": {"agent_id_0", "agent_id_1", "agent_id_3"},
	"du_0": {"agent_id_0", "agent_id_2", "agent_id_5"}
	}
"""
#This function sorts dus in order of costs and size from smaller cost to higher cost.
def sort_dus(dus, configuration = None):
	dus_tmp={}
	#Count importance of every du to asign
	for du in dus:
		level = dus[du]["cost"] + dus[du]["size"]
		dus_tmp[du]=level
	dus_sorted = sorted(dus_tmp.items(), key=lambda kv: kv[1])
	#print(dus_sorted)	
	dus_final = dict(dus_sorted)
	#Format: {'du_6': 50, 'du_4': 92, 'du_5': 133, 'du_0': 200, 'du_1': 251, 'du_3': 315}
	
	return dus_final


#This function sorts agents in order of what they grant from smaller grant to higher grant.
#High grant means that the agent permits to cloudbook to use much of its computing capacity.
def sort_agents(agents_with_grant, configuration = None):
	agents_tmp={}
	#Order the agents by grant
	for agent in agents_with_grant:
		if agents_with_grant[agent] == "LOW":
			agents_tmp[agent]=100
		elif agents_with_grant[agent] == "MEDIUM":
			agents_tmp[agent]=200
		else:
			agents_tmp[agent]=300
	agents_sorted = sorted(agents_tmp.items(), key=lambda kv: kv[1])
	agents_final = dict(agents_sorted)
	
	return agents_final

#Assigns DUs to agents taking into account the cost each DU and the grant level of every agent.
def assign_dus_to_machines(circle_agents, agents_with_grant, dus, configuration = None):
	dus_sorted=sort_dus(dus)
	agents_sorted_by_grant=sort_agents(agents_with_grant)

	if(len(circle_agents) != len(agents_sorted_by_grant)):
		print("FATAL: circle agents number not coincident")
		return 0
	else:
		#Assign agents to dus.
		#In this case, we're assigning agents to DUs by looking to the most optimal performance.
		#We assume that LOW means 100 points, MEDIUM 200 points and HIGH 300 points.
		#Each DU has a number of performance points assigned. When we distribute DUs amongs agents, we substract the performance of 
		# every agent to the performance of every DU, assigning it when the value is closest to zero. We do this in every case.
		#With this method we are always assigning every DU to an agent, no matter if there are more DUs that agents.
		
		result = {}
		for du in reversed(list(dus_sorted.keys())):
			result[du]=[]
			print(du)

			smallest = float(999999999999)
			chosen_agent = ""
			for agent in reversed(list(agents_sorted_by_grant.keys())):

				if abs(dus_sorted[du]-agents_sorted_by_grant[agent]) < smallest:
					
					smallest = abs(agents_sorted_by_grant[agent]-dus_sorted[du])
					print(smallest)
					chosen_agent = agent
			
			result[du].append(chosen_agent)
			agents_sorted_by_grant[chosen_agent]=agents_sorted_by_grant[chosen_agent]-dus_sorted[du]
			print(chosen_agent, agents_sorted_by_grant[chosen_agent])


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