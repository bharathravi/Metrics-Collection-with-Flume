#!/bin/sh

FLUME_HOME='/root/flume-distribution-0.9.4'
MASTER=`cat master`
export FLUME_CONF_DIR=$FLUME_HOME/conf

# Stop old  master
$FLUME_HOME/bin/flume-daemon.sh stop master


./setup $MASTER stop

for agent in `cat agents.conf | cut -d';' -f1 | sort | uniq`
do
  HOST=`echo $agent | cut -d';' -f1`
  echo "Stopping $HOST on $HOST"
  ssh -o ConnectTimeout=5 $HOST "cd $FLUME_HOME; $FLUME_HOME/bin/flume-daemon.sh stop node -n $HOST" | sed "s/^/$HOST: /" &
done

wait
