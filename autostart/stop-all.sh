#!/bin/sh

. ./env.sh

if [ "$FLUME_HOME" = "" ]; then
  echo "FLUME_HOME is not set"
  exit
fi


MASTER=`cat master`
export FLUME_CONF_DIR=$FLUME_HOME/conf

./configure.sh stop

# Stop master
ssh -o ConnectTimeout=5 $MASTER "cd $FLUME_HOME; $FLUME_HOME/bin/flume-daemon.sh stop master" 2>&1 | sed "s/^/$MASTER: /" &


for agent in `cat agents.conf | cut -d';' -f1 | sort | uniq`
do
  HOST=`echo $agent | cut -d';' -f1`
  echo "Stopping $HOST on $HOST"
  ssh -o ConnectTimeout=10 $HOST "cd $FLUME_HOME; $FLUME_HOME/bin/flume-daemon.sh stop node -n $HOST" 2>&1 | sed "s/^/$HOST: /" &
done

wait
