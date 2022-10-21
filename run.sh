#!/usr/bash


source ~/.venv-aiblox/bin/activate
sudo su -c "~/.venv-aiblox/bin/python3 main.py --tb $1 --config config.yml --debug"
