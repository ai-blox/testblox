#!/bin/bash

sudo su -c "apt-get update"
sudo su -c "apt-get install parted"
sudo su -c "apt-get -y install python3-pip"

pip3 install virtualenv

python3 -m virtualenv ~/venv-aiblox
source ~/venv-aiblox/bin/activate

pip3 install -r requirments.txt

