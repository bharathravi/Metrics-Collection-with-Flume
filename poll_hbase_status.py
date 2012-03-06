#!/usr/bin/python

import os, sys, time, signal
from datetime import datetime
import subprocess, struct

sys.path.append("./protos")
import hbase_status_pb2 as proto

"""Polls HBase for metrics using the HBase logs.
"""

FREQUENCY = 3
HBASE_HOME = "../hbase-0.92.0/"
SHOULD_EXIT = False
HBASE_METRICS_LOG = "/tmp/metrics_hbase.log"
HBASE_REGIONSERVER_METRICS = 'hbase.regionserver:'

previous_timestamp = ''

def signal_handler(signal, frame):
  print 'You pressed Ctrl+C!'
  SHOULD_EXIT = True
        
def getPaddedLength(string):
  """Returns the length of the string padded to 8 bytes.
  Obviously, the maximum string length allowed is 2^32.
  """ 
  if len(string) > 2<<64:
    print "String too long"
    return -1
  return struct.pack('L', len(string))
 
def getLatencyStats():
  line = subprocess.check_output('tail -n1 ' + HBASE_METRICS_LOG, shell=True)
  words = line.split(None)
  timestamp = words[0]
  if timestamp == previous_timestamp:
    # We have already seen this line. Don't record it again.
    return None

  global previous_timestamp
  previous_timestamp = timestamp
 
  read = 0
  write = 0
  sync = 0 
  if (words[1] == HBASE_REGIONSERVER_METRICS):
    # This line is a regionserver metrics line. Go ahead.
    read = float(words[23][:-1].split('=')[1])
    write = float(words[25][:-1].split('=')[1])
    sync = float(words[27][:-1].split('=')[1])
    return(read, write, sync)
 
  return None

def populateProto(hbase_status, read_latency, write_latency, sync_latency):
  hbase_status.read_latency = read_latency
  hbase_status.write_latency = write_latency
  hbase_status.sync_latency = sync_latency

  return hbase_status

def writeProtoToOutfile(proto, outfile):
  serialized = proto.SerializeToString()
  length = getPaddedLength(serialized)
  if length == -1:
    return
  outfile.write(length)
  outfile.write(serialized)
  outfile.flush()


def main():
  OUTFILE = open('hbase_status.out', 'ab')
  if len(sys.argv) > 1:
    OUTFILE = open(sys.argv[1], 'ab')

  signal.signal(signal.SIGINT, signal_handler)

  while not SHOULD_EXIT:
   # print SHOULD_EXIT
    hbase_status = proto.HBaseStatus()
    hbase_status.timestamp =  str(datetime.now())
   # print 'Polling...'
  
    stats = getLatencyStats()
    if not stats == None:
      (read_latency, write_latency, sync_latency) = stats
      print (read_latency, write_latency, sync_latency)
      populateProto(hbase_status,read_latency, write_latency, sync_latency)

      writeProtoToOutfile(hbase_status, OUTFILE)
    time.sleep(FREQUENCY)


if __name__ == '__main__':
  main()
