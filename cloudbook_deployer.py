import json



cloudbook_agents={
	"agent_0" : {"127.0.0.1":["du_0"]},
	"agent_1" : {"127.0.0.1":["du_1"]}
}
json_str = json.dumps(cloudbook_agents)
fo = open("../cloudbook_agent/du_files/cloudbook_agents.json", 'w')
fo.write(json_str)
fo.close()

cloudbook_dus={
	"du_0" : ["agent_0"],
	"du_1" : ["agent_1"]
}
json_str = json.dumps(cloudbook_dus)
fo = open("../cloudbook_agent/du_files/cloudbook_dus.json", 'w')
fo.write(json_str)
fo.close()

