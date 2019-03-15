import loader
import json, urllib.request
import urllib.request


#Checks if al machines are online by connecting to the ip publisher service
#If so, calls du_0 to run.

#Reads file created by deployer, compares to 
cloudbook_directory = loader.load_cloudbook("./prueba.json")

def run(circle_id, configuration = None):

    #Process cloudbook_directory by getting every agent that it includes
    agents_list = []
    for du in cloudbook_directory:
        for agent in cloudbook_directory[du]:
            if agent not in agents_list:
                agents_list.append(agent)

    ip_publisher_agents = get_online_agents(circle_id)

    if(set(agents_list) == set(ip_publisher_agents)):
        #Invoke du_0 somehow
        return True
    else:
        print ("Error. The following agents are not online:")
        print (set(agents_list).symmetric_difference(set(ip_publisher_agents)))
        return False


def get_online_agents(circle_id, configuration = None):
    agents = list()
    #By now its a fake URL, but it should be:
    #url = "http://cloudbook-ip-publisher.eu-west-1.elasticbeanstalk.com/getCircle?circle_id="+circle_id"
    url = "http://localhost:3100/getCircle?circle_id="+circle_id
    with urllib.request.urlopen(url) as res:
        data = json.loads(res.read().decode())
        for agent in data:
            if data[agent]["IP"]=="None":
                continue
            else:
                agents.append(agent)
        return agents


def run_local(configuration = None):
    
    #just invoke du_0 somehow
    return True

if __name__ == "__main__":
    contents = urllib.request.urlopen("http://localhost:3000/invoke?invoked_function=du_0.main").read()
    try:
        print(eval(contents))
    except:
        print(contents)
