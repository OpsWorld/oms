# -*- coding: utf-8 -*-
# author: itimor

import sys
import subprocess

def run(cmd):
    try:
        stdout = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stderr = ''
    except:
        stdout = ''
        stderr = str(sys.exc_info()[1])
    if len(stderr):
        return stderr
    else:
        return stdout