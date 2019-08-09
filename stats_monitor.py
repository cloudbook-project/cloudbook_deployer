import json
import loader
import datetime
import os
import sys
import time
import platform

from pathlib import Path

################################################################################################
def timestamp():
	x=datetime.datetime.now()
	return x.strftime("%b %d %Y %H:%M:%S |")

################################################################################################
#main program to execute by command line
#=======================================
print (" ")
print (" ")
print ("Welcome to cloudbook stats monitor  (V1.0)")
print ("=============================================")
print ("this program analyzes statistics from agens and create consolidated filled matrix")
print ("additionally this program recomends remake if detects high variations of matrix ")
print ("  ")
print ("usage:")
print (" py stats_monitor.py -matrix <filematrix.json> -t <seconds>")
print (" ")

stats_interval=0
# gather invocation parameters
# -----------------------------
num_param=len(sys.argv)
for i in range(1,len(sys.argv)):
	
	if sys.argv[i]=="-t":
		stats_interval=int(sys.argv[i+1])
		i=i+1
	
if (stats_interval<5):
	print ("very low interval value")
	sys.exit(0)


input_dict = loader.load_dictionary("./config.json")
if input_dict["circle_info"]["DISTRIBUTED_FS"] == "":
	if(platform.system()=="Windows"):
	    path= os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']+"/cloudbook/"
	    if not os.path.exists(path):
	        os.makedirs(path)
	else:
	    path = "/etc/cloudbook/"
	    if not os.path.exists(path):
	        os.makedirs(path)
else:
	path = input_dict["circle_info"]["DISTRIBUTED_FS"] 

input_dir = path + os.sep + "distributed"
	
while  True:
	print (timestamp(),"sleeping...", stats_interval	)
	print()
	time.sleep (float(stats_interval))
	print ("============== STATS MONITOR ===============================")
	print (timestamp(), "End of sleep. Now ready for processing stats")

	#read function mapping file
	function_map=loader.load_dictionary(input_dir+"/matrix/function_mapping.json")
	print ("functions mapping:")
	print (function_map)

	#read current cumulated stats file ( this is the filematrix) into a dictionary
	

	#for each agent stats
	#   read stats from agents and add their numbers to the dictionary
	#   delete stats_xx.json
	

	# compare old stats with new stats
	

	# make a recomendation (REQUEST_REMAKE file) based on the comparison achieved




