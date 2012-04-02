#!/usr/bin/python

import os, sys, time, signal
from datetime import datetime
import subprocess, struct
from subprocess import Popen, PIPE, STDOUT

sys.path.append("../protos/python")
import hbase_status_pb2 as proto

"""Polls HBase for metrics using the HBase logs.
"""

FREQUENCY = 3
HBASE_HOME = os.getenv('HBASE_HOME','')
SHOULD_EXIT = False
HBASE_METRICS_LOG = "/tmp/metrics_hbase.log"
HBASE_REGIONSERVER_METRICS = 'hbase.regionserver:'

previous_timestamp = ''
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
 
def getLatencyStats():
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

def populateProto(host, hbase_status, read_latency, write_latency, sync_latency):
  hbase_status.host = host
  hbase_status.read_latency = read_latency
  hbase_status.write_latency = write_latency
  hbase_status.sync_latency = sync_latency

  return hbase_status

def writeProtoToOutfile(proto):
  serialized = proto.SerializeToString()
  length = getPaddedLength(serialized)
  if length == -1:
    return
  sys.stdout.write(length)
  sys.stdout.write(serialized)
  sys.stdout.flush()


def main():
  signal.signal(signal.SIGINT, signal_handler)
  
  if HBASE_HOME = '':
    print 'Please set $HBASE_HOME'
    exit(1)

  while not SHOULD_EXIT:
    hbase_status = proto.HBaseStatus()
    hbase_status.timestamp =  str(datetime.now())
  
    stats = getLatencyStats()
    if not stats == None:
      (host, read_latency, write_latency, sync_latency) = stats
      populateProto(host, hbase_status,read_latency, write_latency, sync_latency)

      writeProtoToOutfile(hbase_status)
    time.sleep(FREQUENCY)


if __name__ == '__main__':
  main()
