import json
import loader
import datetime
import os
import sys
import time
import platform

from pathlib import Path


def sum_all_items_matrix(matrix):
	suma=0
	len_row=len(matrix[0])
	for row in range(1,len_row):
		for col in range(1,len_row):
			suma+=matrix[row][col]
	return suma

def compare_matrix(old_matrix,matrix):
	
	#first sumation of all values
	suma_old=sum_all_items_matrix(old_matrix)
	suma=sum_all_items_matrix(matrix)



	len_row=len(old_matrix[0])
	print ("len_row",len_row)
	
	ratio=1
	num_updates_ratio=0
	for row in range(1,len_row):
		for col in range(1,len_row):
			print ("old:",+old_matrix[row][col], "   new:",+matrix[row][col])
			ratio_new =(suma)//(1+matrix[row][col])
			ratio_old =(suma_old)//(1+old_matrix[row][col])
			print ("ratios:", ratio_old,ratio_new)
			ratio=ratio_new//ratio_old
			if ratio>10:
				return True
	return False


##############################################################
# frow are invokers
# fcol are invoked

def matrix_set(frow,fcol, value):
	#print ("get ",frow,fcol)
	col_index=0
	for i in matrix[0]: # scans 1st row
		if i==frow:
			#print("col found", i,col_index)
			break
		col_index+=1

	row_index=0
	for i in matrix:
		#print ("row:",i)
		if i[0]==fcol:
			#print ("row found")
			break
			#return matrix[row_index][col_index]
		row_index+=1
	matrix[row_index][col_index]=value
	return
#############################################################
# frow are invokers
# fcol are invoked

def matrix_get(frow,fcol):
	#print ("get ",frow,fcol)
	col_index=0
	for i in matrix[0]: # scans 1st row
		if i==frow:
			print("col found", i,col_index)
			break
		col_index+=1

	row_index=0
	for i in matrix:
		#print ("row:",i)
		if i[0]==fcol:
			#print ("row found")
			return matrix[row_index][col_index]
		row_index+=1
################################################################################################
def timestamp():
	x=datetime.datetime.now()
	return x.strftime("%b %d %Y %H:%M:%S |")

################################################################################################
def timestamp_file():
	now=datetime.datetime.now()
	return now.strftime("%Y%m%d%H%M%S")

################################################################################################
def get_stats(input_dir):
	cumulated_stats={}
	print ("----")
	for i in matrix:
		print (i)

	print("reading agents stats...")
	agents_with_grant = {}
	agents_files=[]
	agents_files=os.listdir(input_dir+"/stats")
	print (agents_files)
	# enter in each file
	print ("--------------------------------")
	for file in agents_files:
		print ("loading file:"+file+" ...")
		agent_stats= loader.load_dictionary(input_dir+"/stats/"+file)
		print ("   agent_stats=",agent_stats)
		for invoked_dict in agent_stats: # cada d es un diccionario con las invocaciones a una funcion
			invoked_orig_name=function_inverse_map[invoked_dict]
			print ("     processing  invoked:", invoked_dict, " orig_name:",invoked_orig_name) # printa una funcion
			
			for invoker in agent_stats[invoked_dict]: #f1:4, f2:6 , veces que f ha invocado a la invoked
				print ("       processing invoker",invoker, "orig_name",function_inverse_map[invoker])
				invoker_orig_name=function_inverse_map[invoker]
				prev_value=matrix_get(invoker_orig_name,invoker_orig_name)
				#print ("       teniamos:",matrix_get(invoker_orig_name,invoker_orig_name)) #[invoker_orig_name])
				print (" adding:",agent_stats[invoked_dict][invoker])
				adding_value=agent_stats[invoked_dict][invoker]
				matrix_set(invoker_orig_name,invoker_orig_name,prev_value+adding_value)
			
		#removal of file . STILL NOT ACTIVATED 
		#os.remove (input_dir+"/stats/"+file)
	print ("all agents have been read")
	print (matrix)

	# PENDIENTE SALVAR EL FICHERO, aunque ya esta programado
	"""
	json_str = json.dumps(agents_with_grant)
	fo = open(output_dir+"/agents_grant.json", 'w')
	fo.write(json_str)
	fo.close()
	"""
	return 

################################################################################################
#main program to execute by command line
#=======================================
print (" ")
print (" ")
print ("Welcome to cloudbook stats monitor  (V1.0)")
print ("=============================================")
print ("This program analyzes statistics from agens and create consolidated filled matrix")
print ("additionally this program recomends remake if detects high variations of matrix ")
print ("  ")
print ("usage:")
print (" py stats_monitor.py -project_folder <folder> -matrix <filematrix.json> [-t <seconds>]")
print ("where: ")
print ("   -project_folder : the name of the folder of your project")
print ("   -matrix : the matrix to compare new stats")
print ("   -t : (optional) stats monitoring interval. If not present, default value is 3/2*AGENT_STATS_INTERVAL")
print ("")



function_inverse_map={}
function_map={}


stats_interval=0 #initial value
filematrix="matrix"

# read AGENT_STATS_INTERVAL parameter at config.json
# --------------------------------------------------



# gather invocation parameters
# -----------------------------
num_param=len(sys.argv)
for i in range(1,len(sys.argv)):
	
	if sys.argv[i]=="-t":
		stats_interval=int(sys.argv[i+1])
		i=i+1

	if sys.argv[i]=="-matrix":
		filematrix=sys.argv[i+1]
		i=i+1

	if sys.argv[i]=="-project_folder":
		project_folder=	sys.argv[i+1]
		i=i+1
	
if (project_folder==""):
	print ("option -project_folder missing")
	sys.exit(0)


#load dictionary config.json to extract AGENT_STATS_INTERVAL
# ----------------------------------------------------------
if(platform.system()=="Windows"):
	path= os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']+"/cloudbook/"+project_folder	
else:
	path = "/etc/cloudbook/"+project_folder
	

input_dir = path + os.sep + "distributed"
config_dir = path + os.sep + "distributed"
config_dict = loader.load_dictionary(config_dir+ os.sep +"config.json")

agent_stats_interval=config_dict["AGENT_STATS_INTERVAL"]
print("  value of AGENT_STATS_INTERVAL at config.json is:",str(agent_stats_interval)," seconds")
# default value of stats interval is 3/2 * agent_stats_interval
if (stats_interval==0):
	stats_interval=(3*agent_stats_interval)/2

# check final value of stats_interval
if (stats_interval<agent_stats_interval):
	print ("very low interval value (lower than AGENT_STATS_INTERVAL parameter at config.json")
	sys.exit(0)

if (stats_interval<5):
	print ("very low interval value")
	sys.exit(0)

# read matrix input into a dictionary 
# this is the current cumulated stats file ( this is the filematrix) 
print (" Reading matrix: ", filematrix," ...")
matrix={}
matrix=loader.load_dictionary(input_dir+"/matrix/"+filematrix)
old_matrix=loader.load_dictionary(input_dir+"/matrix/"+filematrix)

print (matrix)

"""
print ("matrix test invoker:move_tower, invoked:main:")
print (matrix_get("hanoi.move_tower", "hanoi.main"))
matrix_set("hanoi.move_tower","hanoi.main",23)
print (matrix_get("hanoi.move_tower", "hanoi.main"))
print ("-----------")
print (matrix)
sys.exit(0)
"""

# ----------------- monitoring process --------------------------------	
while  True:
	print (timestamp(),"sleeping...", stats_interval, " seconds")
	print()
	time.sleep (float(stats_interval))
	print ("============== STATS MONITOR ===============================")
	print (timestamp(), "End of sleep. Now ready for processing stats")

	#read function mapping file
	function_map=loader.load_dictionary(input_dir+"/matrix/function_mapping.json")
	print ("functions mapping:")
	print (function_map)
	function_inverse_map={}
	for i in function_map:
		function_inverse_map[function_map[i]]=i

	
	print ("--- current matrix ---")
	print (matrix)


	#for each agent stats
	#   read stats from agents and add their numbers to the matrix
	#   delete stats_xx.json
	get_stats(input_dir)
	
	print ("--- new matrix ---")
	print (matrix)


	#write output file in json format
	#---------------------------------
	json_str = json.dumps(matrix)
	fo = open(input_dir+"/matrix/"+timestamp_file()+"_matrix.json", 'w')
	fo.write(json_str)
	fo.close()
	

	# compare old stats with new stats
	recomendation=compare_matrix(old_matrix,matrix)
	print ("RECOMENDATION REMAKE:", recomendation)

	# make a recomendation (REQUEST_REMAKE file) based on the comparison achieved




