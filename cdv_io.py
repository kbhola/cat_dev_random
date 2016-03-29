# Kishavan Bhola, 2016-03-24
# This is for Symbiont.io's problem
# This library simply writes a seed to file as root
# I came up with this idea after reading the man page for /dev/random.  
# This will require adversary to have local root access in order
# for him or her to make this insecure

import os
import sys

# This boolean encapsulates whether we should check that the script was called
# as the root user.  In reality, for security, this should always be true, but
# for the purposes of testing (by Symbiont, for example), I don't want to enforce this

extra_security = False

seed_file_name = 'cdv_io_seed.log'

def sudo_id():
    return os.environ.get('SUDO_UID')

def is_root():
    return os.getuid() == 0

def kill_if_not_root():
    if not is_root():
        print('ERROR: Needs to be run as root for extra security!')
        sys.exit(0) # kill the python interpreter!


def write_seed_file(seed):
    # for simplicity in this prototype, just write to current working dir
    # and just keep all previously used seeds
    with open(seed_file_name, 'a') as sf:
        sf.write(str(seed) + '\n')

def last_seed(extra_security=False):
    if not os.path.isfile(seed_file_name): # there is no seed file
        if extra_security:
            print('ERROR: No seed file while running with extra security.')
            sys.exit(0)
        else: # okay, no seed file; first time script is run, perhaps
            return b'1'
    else: # there is a seed, so let's grab it
        with open(seed_file_name, 'r') as sf:
            seeds = sf.readlines()
            return (seeds[-1][:-1]).encode('utf-8') # last seed; ignore new lines

def cwd():
    # current working directory
    return (os.getcwd()).encode('utf-8')


if __name__ == '__main__':
    print(str(cwd()))

    print(str(sudo_id()))
    print(str(os.getuid()))

    kill_if_not_root()
