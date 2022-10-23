#!/bin/bash
source $1.envs/$2/bin/activate
cd $1$2/
python3 $2.py
deactivate
