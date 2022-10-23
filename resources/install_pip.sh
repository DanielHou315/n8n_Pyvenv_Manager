#!/bin/bash
source /data/scripts/.envs/$1/bin/activate
python3 /data/scripts/manage/resources/get-pip.py
deactivate
