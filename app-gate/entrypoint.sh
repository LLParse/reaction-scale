#!/bin/bash -x

#  Starts local mongdb installation.
#  Starts application main.js
#
#  MONGO_URL env variable will prevent local db start
#

# set default meteor values if they arent set
: ${PORT:="80"}
: ${ROOT_URL:="http://localhost"}
: ${MONGO_URL:="mongodb://127.0.0.1:27017/meteor"}

# set default node executable
: ${NODE:="node"}

#start mongodb (optional)
if [[ "${MONGO_URL}" == *"127.0.0.1"* ]]; then
  echo "Starting local MongoDB..."
  # startup mongodb
  /usr/bin/mongod --smallfiles --fork --logpath /var/log/mongodb.log

fi

# Wait for mongodb
ip=$(curl rancher-metadata/2015-12-19/self/stack/services/mongo1/containers/0/primary_ip)
echo Waiting for mongo-1
while true; do
    >/dev/tcp/$ip/27017
    if [ "$?" -eq "0" ]; then
        break
    fi
    sleep 1
done    

ip=$(curl rancher-metadata/2015-12-19/self/stack/services/mongo2/containers/0/primary_ip)
echo Waiting for mongo-2
while true; do
    >/dev/tcp/$ip/27017
    if [ "$?" -eq "0" ]; then
        break
    fi
    sleep 1
done

sleep 10

# Run meteor
exec $NODE ./main.js