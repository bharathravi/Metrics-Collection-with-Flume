#!/usr/bin/python

import os, sys, time, signal
from datetime import datetime
import subprocess, struct
from subprocess import Popen, PIPE, STDOUT

sys.path.append("/root/flume_metrics/protos")
import sys_status_pb2 as proto

"""Polls HBase for metrics using the HBase logs.
"""

FREQUENCY = 3
SHOULD_EXIT = False

def signal_handler(signal, frame):
  global SHOULD_EXIT
  SHOULD_EXIT = True
        
def getPaddedLength(string):
  """Returns the length of the string padded to 8 bytes.
  Obviously, the maximum string length allowed is 2^32.
  """ 
  if len(string) > 2<<64:
    return -1
  return struct.pack('<l', len(string))
 
def getSysStats():
  p = subprocess.Popen('tail -n1 ' + HBASE_METRICS_LOG, shell=True, stdout=PIPE)
  line = p.stdout.read()
  words = line.split(None)
  timestamp = words[0]
  global previous_timestamp
  if timestamp == previous_timestamp:
    # We have already seen this line. Don't record it again.
    return None

  previous_timestamp = timestamp
 
  read = 0
  write = 0
  sync = 0 
  if (words[1] == HBASE_REGIONSERVER_METRICS):
    # This line is a regionserver metrics line. Go ahead.
    host = words[3].split('=')[1]
    read = float(words[23][:-1].split('=')[1])
    write = float(words[25][:-1].split('=')[1])
    sync = float(words[27][:-1].split('=')[1])
    return(host, read, write, sync)
 
  return None

def populateProto(host, total_memory, free_memory, num_cpus, cpu_load):
  sys_status.host = host
  sys_status.total_memory = total_memory
  sys_status.free_memory = free_memory
  sys_status.num_cpus = num_cpus
  sys_status.cpu_load = cpu_load

  return sys_status

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
  OUTFILE = open('sys_status.out', 'ab')
  if len(sys.argv) > 1:
    OUTFILE = open(sys.argv[1], 'ab')

  signal.signal(signal.SIGINT, signal_handler)

  while not SHOULD_EXIT:
    sys_status = proto.SystemStatus()
    sys_status.timestamp =  str(datetime.now())
  
    stats = getSysStats()
    if not stats == None:
      (host, total_memory, free_memory, num_cpus, cpu_load) = stats
      populateProto(host, total_memory, free_memoru, num_cpus, cpu_load)

      writeProtoToOutfile(sys_status, OUTFILE)
    time.sleep(FREQUENCY)


if __name__ == '__main__':
  main()
