#!/usr/bin/python

import os, sys, time, signal
from datetime import datetime
import subprocess, struct
from subprocess import Popen, PIPE, STDOUT

sys.path.append("/root/flume_metrics/protos")
import hadoop_status_pb2 as proto

"""This file polls Hadoop for per job completion metrics.
It uses the hadoop command line API and wget, which is clumsy, evil and slow.
"""

#TODO(bharath): Use a more sane API
#TODO(bharath): Do not get metrics for jobs that have finished more than once.

FREQUENCY = 3
HADOOP_HOME = "/root/hadoop-1.0.1"
SHOULD_EXIT = False
finished_jobs = []


def signal_handler(signal, frame):
<<<<<<< HEAD
  global SHOULD_EXIT
=======
>>>>>>> 918581a3ef8fcffca801fa7e08c3c8c09858a9ae
  SHOULD_EXIT = True
        
def getPaddedLength(string):
  """Returns the length of the string padded to 8 bytes.
  Obviously, the maximum string length allowed is 2^64.
  """ 
  if len(string) > 2<<64:
    return -1
  return struct.pack('<l', len(string))
 
def getJobsList():
  # Flawed security with shell=True
  p = subprocess.Popen(HADOOP_HOME + '/bin/hadoop job -list all', shell=True, stdout=PIPE)
  lines = p.stdout.read()
  return lines.split('\n')[4:-1]

def getJobStats(job_id, job_state):
  # TODO(bharath): This method is evil and absolutely dirty. Find a better way of achieving this.
  p = subprocess.Popen(HADOOP_HOME + '/bin/hadoop job -status ' + job_id + ' | grep  "tracking URL" | cut -d" " -f3', shell=True, stdout=PIPE)
  trackingURL = p.stdout.read().rstrip()
<<<<<<< HEAD
=======
  print 'tracking ' + trackingURL
>>>>>>> 918581a3ef8fcffca801fa7e08c3c8c09858a9ae
  p = subprocess.Popen('wget -qO- ' + trackingURL + ' | grep "Started at" | cut -d" " -f3-10', shell=True, stdout=PIPE)
  start_time = p.stdout.read()[0:-5]

  p = subprocess.Popen(HADOOP_HOME + '/bin/hadoop job -status ' + job_id + ' | grep -E "map\(\)|reduce\(\)" | cut -d" " -f3', shell=True, stdout=PIPE)
  statuslines = p.stdout.read()

  map_percent = float(statuslines.rstrip().split('\n')[0])
  reduce_percent = float(statuslines.rstrip().split('\n')[1])
  finish_time = ''
  if job_state == '2':
    # The job has completed. Get finish time.
    # Add it to the finished list so that we don't query for it again in future    
    finished_jobs.append(job_id)
    p = subprocess.Popen('wget -qO- ' + trackingURL + ' | grep "Finished at" | cut -d" " -f3-10', shell=True, stdout=PIPE)
    statuslines = p.stdout.read()[0:-5]
 
  return (start_time, finish_time, map_percent, reduce_percent)

def populateProto(hadoop_status, job_id, job_state, start_time, finish_time, map_percent, reduce_percent):
  jobstatus = hadoop_status.job_status.add()
  jobstatus.map = map_percent
  jobstatus.reduce = reduce_percent
  jobstatus.start_time = start_time
  jobstatus.finish_time = finish_time
  jobstatus.job_id =job_id
  jobstatus.job_status = job_state

  return hadoop_status

def writeProtoToOutfile(proto, outfile):
  serialized = proto.SerializeToString()
  length = getPaddedLength(serialized)
  if length == -1:
    return
  sys.stdout.write(length)
  sys.stdout.write(serialized)
  sys.stdout.flush()
  outfile.write(length)
  outfile.write(serialized)
  outfile.flush()


def main():
  OUTFILE = open('hadoop_status.out', 'ab')
  if len(sys.argv) > 1:
    OUTFILE = open(sys.argv[1], 'ab')

  signal.signal(signal.SIGINT, signal_handler)

  while not SHOULD_EXIT:
    hadoop_status = proto.HadoopStatus()
    hadoop_status.timestamp =  str(datetime.now())
   
    for line in getJobsList():
      job_id = line.split(None)[0]
      job_state = line.split(None)[1]
      finish_time = ''
      start_time = ''
      map_percent = 0
      reduce_percent = 0

      if job_id not in finished_jobs:
        (start_time, finish_time, map_percent, reduce_percent) = getJobStats(job_id, job_state)
        populateProto(hadoop_status,job_id, job_state, start_time, finish_time, map_percent, reduce_percent)

    writeProtoToOutfile(hadoop_status, OUTFILE)
  time.sleep(FREQUENCY)


if __name__ == '__main__':
  main()


#bin/hadoop job -status `bin/hadoop job -list | tail -n1 | cut -f1` | grep -E "map\(\)|reduce\(\)" | cut -d' ' -f3

