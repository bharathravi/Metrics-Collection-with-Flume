#!/bin/sh

MASTER=`cat master`
CURRENT_DIR=`pwd`

. ./env.sh

if [ "$FLUME_HOME" = "" ]; then
  echo "FLUME_HOME is not set"
  exit
fi

# Start  master
ssh -o ConnectTimeout=10 $MASTER "cd $FLUME_HOME; $FLUME_HOME/bin/flume-daemon.sh start master" 2>&1 | sed "s/^/$MASTER: /" 

cd $CURRENT_DIR

for agent in `cat agents.conf | cut -d';' -f1 | sort | uniq`
do
  HOST=`echo $agent | cut -d';' -f1`
  ssh -o ConnectTimeout=10 $HOST "cd $FLUME_HOME; $FLUME_HOME/bin/flume-daemon.sh start node -n $HOST" 2>&1 | sed "s/^/$HOST: /" & 
done
 
wait
