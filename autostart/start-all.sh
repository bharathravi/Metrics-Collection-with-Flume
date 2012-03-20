#!/bin/sh

MASTER=`cat master`
CURRENT_DIR=`pwd`

if [ "$FLUME_HOME" = "" ]; then
  export FLUME_HOME='/root/flume-distribution-0.9.4'
fi

# Stop old  master
$FLUME_HOME/bin/flume-daemon.sh stop master

# Start master
cd $FLUME_HOME; $FLUME_HOME/bin/flume-daemon.sh start master
cd $CURRENT_DIR

for agent in `cat agents.conf`
do
  HOST=`echo $agent | cut -d';' -f1`
  NODE_NAME=`echo $agent | cut -d';' -f2`
  ssh $HOST "cd $FLUME_HOME; $FLUME_HOME/bin/flume-daemon.sh start node -n $NODE_NAME"
done

./setup $MASTER start
