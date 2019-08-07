
import shutil
import loader

# this function creates the file agents_grant.json using the files agent_xxx_grant.json created
# by each agent
def create_file_agents_grant(input_dir):

	return


# this function creates a backup of file 
def backup_file(input_dir, source_filename, dest_filename):    
	shutil.copy2(input_dir+source_filename, input_dir+dest_filename) # complete target filename given
	return

"""
# this function creates the backup of file agents_grant.json 
def create_file_previous_agents_grant(input_dir):    
	shutil.copy2(input_dir+"/agents_grant.json", input_dir+"/previous_agents_grant.json") # complete target filename given
	return
"""
# this function creates the backup of file cloudbook.json 
"""
def create_file_previous_cloudbook(input_dir):    
	shutil.copy2(input_dir+"/cloudbook.json", input_dir+"/previous_cloudbook.json") # complete target filename given
	return
"""

def check_agents_change(input_dir):
	agents_with_grant = loader.load_dictionary(input_dir+"/agents_grant.json")

	previous_agents_with_grant = loader.load_dictionary(input_dir+"/previous_agents_grant.json")

	return compare_dictionaries(agents_with_grant,previous_agents_with_grant)




def compare_dictionaries(dict1, dict2): 
	new_agents=False
	stopped_agents=False
	agents_updated=False

	for i in dict1:
		if i not in dict2:
			new_agents=True
		else:
			if (dict1[i]!=dict2[i]):
				print ("agent ",i, "has changed")
				print (dict1[i], "-->",dict2[i])
				agents_updated=True

	for i in dict2:
		if i not in dict1:
			stopped_agents=True
		else:
			if (dict1[i]!=dict2[i]):
				print ("agent ",i, "has changed")
				print (dict1[i], "-->",dict2[i])
				agents_updated=True

	print ("")
	print (" identified changes:")
	print ("   new agents:", new_agents)
	print ("   stopped agents:", stopped_agents)
	print ("   updated agents:", agents_updated)


	if not new_agents and not stopped_agents and not agents_updated:
		#print ("no changes on agents")
		return 0

	print ("HOT redeployment")

	if (new_agents or agents_updated) and not stopped_agents:
		#print ("HOT REDEPLOYMENT: new agents or agents updated but not stopped_agents")
		return 1

	#print ("HOT REDEPLOYMENT: stopped agents")
	return 2


