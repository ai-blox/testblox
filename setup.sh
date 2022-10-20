#!/bin/bash

if [[ $(/usr/bin/id -u) -ne 0 ]]; then
  echo "This script need to be run as root"
  exit
fi

apt-get update
apt-get install parted
apt-get -y install python3-pip

pip3 install -r requirments.txt