#!/bin/bash
source $1.envs/$2/bin/activate
python3 $1manage/resources/get-pip.py
deactivate
