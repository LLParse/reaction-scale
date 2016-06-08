#!/bin/bash

start=$1
stop=$2

for i in $(seq $start $stop); do
  curl -s localhost:$((79+$i)) &> /dev/null
  if [ $? -eq 0 ]; then
    echo -e "App $i\tUP"
  else
    echo -e "App $i\tDOWN"
  fi
done