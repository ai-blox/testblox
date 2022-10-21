#!/bin/bash

source ~/.venv-aiblox/bin/activate

pushd ~/.venv-aiblox/bin
PYTHON_DIR=$(pwd)
popd

sudo su -c "${PYTHON_DIR}/python3 main.py --tb ${1} --config config.yml --debug"
