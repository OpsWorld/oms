#!/bin/bash
# author: kiven

cd /data/projects/oms/omsBackend
/root/.pyenv/shims/python manage.py runworker --threads 5 --only-channels=websocket.*
