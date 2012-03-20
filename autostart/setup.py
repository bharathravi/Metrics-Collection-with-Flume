#!/usr/bin/python
import sys
def start_configs(master):
	print "connect "+master
#	for line in q.readlines():
#		line=line.strip()
#		print "exec config decommission "+line	
	f=open("agents.conf");
	for line in f.readlines():
		line=line.strip()
		config=line.split(";")
		node=config[1]
		source=config[2]
		sink=config[3]
		comp=source+" "+ sink
		print "exec unconfig " + node
#		print "exec decommission "+node
#		print "exec purge "+node
		print "exec config "+node+" "+comp
	print "exec refreshAll"	

def stop_configs(master):
	print "connect "+master	
	f=open("agents");
	for line in f.readlines():
		line=line.strip()
		#config=line.split(" ")
		node=line
		print "exec unconfig "+node
		print "exec decommission "+node
		print "exec purge "+node

if __name__ == "__main__":
	if(len(sys.argv)!=3):
		sys.exit("Usage master_hostname start|stop")
		
	master=sys.argv[1]
	option=sys.argv[2]
	if option == "start":
		start_configs(master)
	else:
		stop_configs(master)
		

