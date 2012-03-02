#!/usr/bin/python

import os, sys, time
from datetime import datetime
import subprocess


FREQUENCY = 3

def main():
  OUTFILE = open('hadoop_status.out', 'a')
  if len(sys.argv) > 1:
    OUTFILE = open(sys.argv[1], 'a')

  while True:
    print 'Polling...'
    # Flawed security with shell=True
    lines = subprocess.check_output("./bin/hadoop job -list", shell=True)
    #jobs = call("ls")
    for line in lines.rstrip().split('\n')[2:]:
      jobid = line.split(None)[0]
      OUTFILE.write(str(datetime.now()) + ' ' + jobid + ' ')
      statuslines = subprocess.check_output('bin/hadoop job -status ' + jobid + ' | grep -E "map\(\)|reduce\(\)" | cut -d" " -f3', shell=True)
      for status in statuslines.rstrip().split('\n'):
        OUTFILE.write(status.rstrip() + ' ')
      OUTFILE.write('\n')
      OUTFILE.flush()
      time.sleep(FREQUENCY)


if __name__ == '__main__':
  main()


#bin/hadoop job -status `bin/hadoop job -list | tail -n1 | cut -f1` | grep -E "map\(\)|reduce\(\)" | cut -d' ' -f3

