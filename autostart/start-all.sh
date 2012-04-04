#!/bin/sh

MASTER=`cat master`
CURRENT_DIR=`pwd`

./setup-env.sh

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
  ssh $HOST "cd $FLUME_HOME; $FLUME_HOME/bin/flume-daemon.sh start node -n $HOST"
done


# Unfortu-bloody-nately, the master in flume 0.9.2 takes up to 5 minutes
# to start up with an external zookeeper. We sleep for a while to give it
# time to move its lazy behind.

#echo "Waiting for master..."
#sleep 120

./setup $MASTER start

if [ "$?" -ne 0 ]; then
  ./stop-all.sh
fi
