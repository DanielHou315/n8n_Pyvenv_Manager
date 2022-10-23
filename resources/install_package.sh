#!/bin/bash
source /data/scripts/.envs/$1/bin/activate
python3 -m pip install $2
deactivate
