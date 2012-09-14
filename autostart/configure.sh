#!/bin/bash
if [ $# -ne 2 ];
then
        echo "Usage : setup master_node start|stop"
        exit 1
fi
MASTER=$1
OPTION=$2
TEMP_FILENAME=`pwd`/temp_file

if [ "$FLUME_HOME" = "" ]; then
  echo "FLUME_HOME is not set"
  exit 1
fi

echo "Configuring nodes"
./setup.py $MASTER $OPTION > $TEMP_FILENAME

COUNT=0
cd $FLUME_HOME; $FLUME_HOME/bin/flume shell -q -c $MASTER -s $TEMP_FILENAME

while [ "$?" -ne 0 ];
do
  # If the flume shell command failed, sleep for 5 seconds and try again, 
  # up to 12 counts
  echo "Couldn't connect to master. Retrying..."
  sleep 5;
  COUNT=$(( $COUNT + 1 ))
  if [ "$COUNT" -eq 12 ]; then
    echo "Failed to connect to master";
    exit 1;
  fi

  cd $FLUME_HOME; $FLUME_HOME/bin/flume shell -q -c $MASTER -s $TEMP_FILENAME;
done
