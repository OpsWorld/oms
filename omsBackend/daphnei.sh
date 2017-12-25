#!/bin/bash
# author: kiven

cd /data/projects/oms/omsBackend
/root/.pyenv/shims/daphne -b 0.0.0.0 -p 8001 -v2 omsBackend.asgi:channel_layer --access-log=/data/logs/oms/daphnei.log
