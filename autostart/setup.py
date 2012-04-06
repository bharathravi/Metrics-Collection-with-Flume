#!/usr/bin/python
import sys
def start_configs(master):
  print "connect "+master
#  for line in q.readlines():
#    line=line.strip()
#    print "exec config decommission "+line  
  f=open("agents.conf");
  seen_hosts = []
  print "submit unmapAll"
  print "submit purgeAll"
  for line in f.readlines():
    line=line.strip()
    if len(line) == 0:
      # Ignore empty lines
      continue
   
    config=line.split(";")
    host=config[0]
    node=config[1]
    source=config[2]
    sink=config[3]
    flowname=config[4]
    comp= flowname + " " + source + " " + sink    
    if host not in seen_hosts:
      seen_hosts.append(host)
      print "submit decommission " + host
    print "submit decommission "+node
    print "submit map " + host + " " + node

    # Use some noops after map to give it some time 
    # to start up. 
    print "submit noop 5000"
    print "submit noop 5000"
    print "submit config " + node + " " + comp
  print "submit refreshAll"  

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
