import json
import loader
import datetime
import os
import sys
import time

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


while  True:
	print (timestamp(),"sleeping...", stats_interval	)
	print()
	time.sleep (float(stats_interval))
	print ("============== STATS MONITOR ===============================")
	print (timestamp(), "End of sleep. Now ready for processing stats")


