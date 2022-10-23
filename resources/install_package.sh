#!/bin/bash
source $1.envs/$2/bin/activate
python3 -m pip install $3
deactivate
