
import shutil
import loader
import os
import sys

#######################################################################################################
def clean_touch_files(input_dir):
	#delete posible alarms before sleep
	critical_file= os.path.isfile(input_dir+"/CRITICAL")
	if critical_file:
		os.remove(input_dir+"/CRITICAL")

	warning_file= os.path.isfile(input_dir+"/WARNING")
	if warning_file:
		os.remove(input_dir+"/WARNING")

	#delete REDEPLOY file if exists
	redeploy_file= os.path.isfile(input_dir+"/COLD_REDEPLOY")
	if redeploy_file:
		os.remove(input_dir+"/COLD_REDEPLOY")
	redeploy_file= os.path.isfile(input_dir+"/HOT_REDEPLOY")
	if redeploy_file:
		os.remove(input_dir+"/HOT_REDEPLOY")


#######################################################################################################
# this function identifies the idle (= non busy agents) that may be existing agents or new ones
# these agents have not any DU assotiated and are ready to get DUs
def get_idle_agents(input_dir):
	
	nba=[]
	cloudbook=loader.load_dictionary(input_dir+"/cloudbook.json")
	#print (cloudbook)

	aal=[]
	agents_with_grant = loader.load_dictionary(input_dir+"/agents_grant.json")
	available_agents=sorted (agents_with_grant.items())
	for i in range (0,len(available_agents)):
		aal.append(available_agents[i][0])

	#print ("available agents:")
	#print (aal)
	
	#print ("checking cloudbook")
	for a in aal:
		found=False
		for du in cloudbook:
			#print (cloudbook[du])
			for adu in cloudbook[du]:
				if adu == a :
					found=True
					continue
		if not found:
			nba.append(a)
	
	#print ("NBA:", nba)
	#sys.exit()
	return nba

#######################################################################################################
# this function creates the file agents_grant.json using the files agent_xxx_grant.json created
# by each agent
def create_file_agents_grant(input_dir):
	print("creating file agents_grant...")
	agents_with_grant = {}
	agents_files=[]
	agents_files=os.listdir(input_dir+"/agents_grant")
	print (agents_files)
	# enter in each file
	for file in agents_files:
		agent= loader.load_dictionary(input_dir+"/agents_grant/"+file)
		print ("agent=",agent)
		for a in agent:
			agents_with_grant[a]=agent[a]
		os.remove (input_dir+"/agents_grant/"+file)
	print ("all agents have been read")
	print (agents_with_grant)

	# PENDIENTE SALVAR EL FICHERO
	"""
	json_str = json.dumps(agents_with_grant)
	fo = open(output_dir+"/agents_grant.json", 'w')
	fo.write(json_str)
	fo.close()
	"""
	return

#######################################################################################################
# this function creates a backup of file 
def backup_file(input_dir, source_filename, dest_filename):    
	shutil.copy2(input_dir+source_filename, input_dir+dest_filename) # complete target filename given
	return

#######################################################################################################
def check_agents_changes(input_dir,na,ma,sa):
	agents_with_grant = loader.load_dictionary(input_dir+"/agents_grant.json")

	previous_agents_with_grant = loader.load_dictionary(input_dir+"/previous_agents_grant.json")

	return compare_dictionaries(agents_with_grant,previous_agents_with_grant,na,ma,sa)

#######################################################################################################
# this fuction compares the previous (dict2) and new dictionary (dict1). 
# return values:
#   0 : if no changes
#   1 : if new or modified but not stopped agents
#   2 : if stopped agents
#   lists: 
#   
def compare_dictionaries(dict1, dict2,new_agents_dict={}, modified_agents_dict={}, stopped_agents_dict={}): 
	new_agents=False
	new_agents_counter=0
	
	stopped_agents=False
	stopped_agents_counter=0
	
	modified_agents=False
	modified_agents_counter=0
	

	for i in dict1:
		if i not in dict2:
			new_agents=True
			new_agents_dict[i]=dict1[i]
			new_agents_counter+=1
		else:
			if (dict1[i]!=dict2[i]):
				print ("agent ",i, "has changed")
				print (dict1[i], "-->",dict2[i])
				modified_agents=True
				modified_agents_dict[i]=dict2[i]
				modified_agents_counter+=1

	for i in dict2:
		if i not in dict1:
			stopped_agents=True
			stopped_agents_dict[i]=dict2[i]
			stopped_agents_counter+=1
		else:
			if (dict1[i]!=dict2[i]):
				print ("agent ",i, "has changed")
				print (dict1[i], "-->",dict2[i])
				modified_agents=True
				modified_agents_dict[i]=dict1[i] # this line is not needed

	print ("")
	print (" Identified changes:")
	print ("   - new agents:", new_agents_counter)
	print ("   - stopped agents:", stopped_agents_counter)
	print ("   - modified agents:", modified_agents_counter)
	print ("")

	if not new_agents and not stopped_agents and not modified_agents:
		#print ("no changes on agents")
		return 0

	print ("HOT redeployment")

	if (new_agents or modified_agents) and not stopped_agents:
		#print ("HOT REDEPLOYMENT: new agents or agents updated but not stopped_agents")
		return 1

	#print ("HOT REDEPLOYMENT: stopped agents")
	return 2


