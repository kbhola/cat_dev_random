# System sources of entropy
# Kishavan Bhola

import subprocess
import sys
import os

def get_platform():
    return str(sys.platform).encode('utf-8') # note that OS X returns Darwin

def uptime(): 
    # system uptime; can be used as a seed
    # on Mac, also returns some 'load averages'
    return subprocess.check_output(['uptime'])

def boottime():
    # I think this works on linux too
    return subprocess.check_output(['sysctl', 'kern.boottime'])

def bootsig():
    return subprocess.check_output(['sysctl', 'kern.bootsignature'])

if __name__ == '__main__':
    print(uptime().decode('utf-8'))
    print(boottime().decode('utf-8'))
    print(bootsig().decode('utf-8'))
