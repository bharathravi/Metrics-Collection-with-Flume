#!/usr/bin/python

import os, sys, time, signal
from datetime import datetime
import subprocess

import hadoop_status_pb2 as proto

FREQUENCY = 3
HADOOP_HOME = "../hadoop-1.0.0"
SHOULD_EXIT = False

def signal_handler(signal, frame):
  print 'You pressed Ctrl+C!'
  SHOULD_EXIT = True
        
 
def main():
  OUTFILE = open('hadoop_status.out', 'a')
  if len(sys.argv) > 1:
    OUTFILE = open(sys.argv[1], 'a')

  signal.signal(signal.SIGINT, signal_handler)

  while not SHOULD_EXIT:
    print SHOULD_EXIT
    status = proto.HadoopStatus()
    status.timestamp =  str(datetime.now())
    print 'Polling...'
    # Flawed security with shell=True
    lines = subprocess.check_output(HADOOP_HOME + '/bin/hadoop job -list', shell=True)
    #jobs = call("ls")
    for line in lines.rstrip().split('\n')[2:]:
      jobstatus = status.job_status.add()
      jobstatus.job_id = line.split(None)[0]
      statuslines = subprocess.check_output(HADOOP_HOME + '/bin/hadoop job -status ' + jobstatus.job_id + ' | grep -E "map\(\)|reduce\(\)" | cut -d" " -f3', shell=True)
      jobstatus.map = float(statuslines.rstrip().split('\n')[0])
      jobstatus.reduce = float(statuslines.rstrip().split('\n')[1])
      print jobstatus.map
      print jobstatus.reduce
    OUTFILE.write(status.SerializeToString())
    OUTFILE.flush()
    time.sleep(FREQUENCY)


if __name__ == '__main__':
  main()


#bin/hadoop job -status `bin/hadoop job -list | tail -n1 | cut -f1` | grep -E "map\(\)|reduce\(\)" | cut -d' ' -f3

