#!/usr/bin/python

import os, sys, time, signal
from datetime import datetime
import subprocess, struct

sys.path.append("./protos")
import hadoop_status_pb2 as proto


def main():
  OUTFILE = open('hadoop_status.out', 'rb')
  if len(sys.argv) > 1:
    OUTFILE = open(sys.argv[1], 'rb')
  
  length_string = OUTFILE.read(4)
  try:
    while length_string != "":
      try:
        length = struct.unpack('<l', length_string)[0]
        print length
        data = OUTFILE.read(length)
        status = proto.HadoopStatus()
        status.ParseFromString(data)    
        print status.timestamp, 
        for job in status.job_status:
          print job.job_id, job.map, job. reduce, job.start_time, job.finish_time
      except:
        print "Unexpected end of data"        
        exit(0)
      length_string = OUTFILE.read(4)
  finally:
    OUTFILE.close()

if __name__ == '__main__':
  main()


#bin/hadoop job -status `bin/hadoop job -list | tail -n1 | cut -f1` | grep -E "map\(\)|reduce\(\)" | cut -d' ' -f3

