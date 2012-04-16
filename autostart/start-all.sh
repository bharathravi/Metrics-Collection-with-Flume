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

for agent in `cat agents.conf | cut -d';' -f1 | sort | uniq`
do
  HOST=`echo $agent | cut -d';' -f1`
  ssh -o ConnectTimeout=1 $HOST "cd $FLUME_HOME; $FLUME_HOME/bin/flume-daemon.sh start node -n $HOST" | sed "s/^/$HOST: /" 
done
 
wait
