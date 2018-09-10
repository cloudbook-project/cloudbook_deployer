import json

cloudbook={}

cloudbook={
	"agent_0" : {"127.0.0.1":["du_0"]},
	"agent_1" : {"127.0.0.1":["du_1"]}
}
json_str = json.dumps(cloudbook)
fo = open("../cloudbook_agent/du_files/cloudbook.json", 'w')
fo.write(json_str)
fo.close()

cloudbook_du={
	"du_0" : ["agent_0"],
	"du_1" : ["agent_1"]
}
json_str = json.dumps(cloudbook_du)
fo = open("../cloudbook_agent/du_files/cloudbook_du.json", 'w')
fo.write(json_str)
fo.close()

