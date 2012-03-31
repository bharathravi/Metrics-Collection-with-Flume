#!/usr/bin/python

import os, sys, time, signal
from datetime import datetime
import subprocess, struct
from subprocess import Popen, PIPE, STDOUT
from socket import gethostname

sys.path.append("/root/Metrics-Collection-with-Flume/protos")
import system_status_pb2 as proto

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

def getHostname():
  return gethostname()

def getMemoryStats():
  p = subprocess.Popen('free -m -t | grep Mem', shell=True, stdout=PIPE)
  line = p.stdout.read()
  words = line.split(None)

  return (int(words[1]), int(words[3]))

def getNumCpus():
  p = subprocess.Popen('cat /proc/stat | grep cpu | wc -l', shell=True, stdout=PIPE)
  line = p.stdout.read()
  return int(line) - 1

def getCpuLoad():
  p = subprocess.Popen('top -b -n1 | grep Cpu', shell=True, stdout=PIPE)
  line = p.stdout.read()
  words = line.split(None)
  return 100 - float(words[4][0:-4])
 
def getSysStats():
  host = getHostname()
  total_mem, free_mem = getMemoryStats()
  num_cpus = getNumCpus()
  cpu_usage = getCpuLoad()
  return(host, total_mem, free_mem, num_cpus, cpu_usage)
 

def populateProto(sys_status, host, total_memory, free_memory, num_cpus, cpu_usage):
  sys_status.host = host
  sys_status.total_memory = total_memory
  sys_status.free_memory = free_memory
  sys_status.num_cpus = num_cpus
  sys_status.cpu_usage = cpu_usage

  return sys_status

def writeProtoToOutfile(proto, outfile):
  serialized = proto.SerializeToString()
  length = getPaddedLength(serialized)
  if length == -1:
    return
  sys.stdout.write(length)
  sys.stdout.write(serialized)
  sys.stdout.flush()


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
      (host, total_memory, free_memory, num_cpus, cpu_usage) = stats
      populateProto(sys_status, host, total_memory, free_memory, num_cpus, cpu_usage)

      writeProtoToOutfile(sys_status, OUTFILE)
    time.sleep(FREQUENCY)


if __name__ == '__main__':
  main()
