#!/bin/sh

FLUME_HOME='/root/flume-distribution-0.9.4'
MASTER=`cat master`
export FLUME_CONF_DIR=$FLUME_HOME/conf

# Stop old  master
$FLUME_HOME/bin/flume-daemon.sh stop master

for agent in `cat agents.conf`
do
  HOST=`echo $agent | cut -d';' -f1`
  NODE_NAME=`echo $agent | cut -d';' -f2`
  echo "Stopping $NODE_NAME on $HOST"
  ssh $HOST "cd $FLUME_HOME; $FLUME_HOME/bin/flume-daemon.sh stop node -n $NODE_NAME"
done
