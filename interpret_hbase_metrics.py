#!/usr/bin/python

import os, sys, time, signal
from datetime import datetime
import subprocess, struct

sys.path.append("./protos")
import hbase_status_pb2 as proto


def main():
  OUTFILE = open('hbase_status.out', 'rb')
  if len(sys.argv) > 1:
    OUTFILE = open(sys.argv[1], 'rb')
  
  length_string = OUTFILE.read(8)
  try:
    while length_string != "":
      try:
        length = struct.unpack('L', length_string)[0]
        data = OUTFILE.read(length)
        status = proto.HBaseStatus()
        status.ParseFromString(data)    
        print status.timestamp, status.read_latency, status.write_latency, status.sync_latency 
      except:
        print "Unexpected end of data"        
        exit(0)
      length_string = OUTFILE.read(8)
  finally:
    OUTFILE.close()

if __name__ == '__main__':
  main()


#bin/hadoop job -status `bin/hadoop job -list | tail -n1 | cut -f1` | grep -E "map\(\)|reduce\(\)" | cut -d' ' -f3

