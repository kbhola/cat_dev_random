# Try to grab hardware entropy in a cross-platform way (OS X / Linux)
# Kishavan Bhola

import sys
import subprocess
import cdv_system


def get_cpu_temp():
    val = b'0'
    if 'darwin' == cdv_system.get_platform():
        # Found tool osx-cpu-temp (should be in current-working directory)
        cpu_temp = subprocess.check_output(['./osx-cpu-temp'])
        print(type(cpu_temp))
        print(cpu_temp.decode('utf-8'))
        val += cpu_temp # concatenate bytes
        print(val)
    else: # we assume we're on a system that supports the following (UNTESTED!)
        # do nothing for now
        return val


if __name__ == '__main__':
    get_cpu_temp()
