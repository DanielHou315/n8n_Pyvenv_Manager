#!/bin/bash
source /data/scripts/.envs/$1/bin/activate
cd /data/scripts/$1/
python3 $1.py
deactivate
