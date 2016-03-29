# Classes & Functionality to Encapsulate an Entropy Pool
# 2016-03-24
# For Symbiont.io test problem

import hashlib
import subprocess
import os
import sys
import cdv_gps
import cdv_system
import cdv_hardware
import cdv_io
import cdv_crypto_prices
import cdv_gps
import time

MAX_POOL_SIZE = 512*1000
SALT = b'10010010010111110'

def sha256(input):
    return hashlib.sha256(input + SALT).digest()

class Pool:
    def __init__(self, salt, size):
        self.salt = salt
        self.size = size
        self.pool = bytearray() # empty bytes
    def add_bytes(self,bs):        
        self.pool += sha256(bs) # add to the byte pool
        self.pool = self.pool[:self.size]    
    def pool_ready(self):
        return len(self.pool) > self.size
    def grab_stream(self):
        return self.pool

class PoolHandler:
    def __init__(self, size=MAX_POOL_SIZE):
        self.pool = Pool(SALT, size) 
        self.size = size
        self.gps = cdv_gps.GPSData()
        self.iters = 0
        self.mean_exec_time = 0
    
    def rand_val(self):
#        self.gather_entropy() # the heavy lifting
        pure_ent = self.pool.grab_stream() # grab the current pool
        pure_ent = pure_ent + bytearray(self.iters) # concatenate with iteration        
        encoded_ent = sha256(pure_ent)
        self.pool.add_bytes(pure_ent) # let's add this secret val back to the pool
        return encoded_ent # the secret pool is never exposed, only the hashed version
        
    def gather_entropy(self):
        start_time = time.time()
        # if we're in the first iteration, let's gather some seed data
        if self.iters == 0:
            self.pool.add_bytes(cdv_system.uptime())
            self.pool.add_bytes(cdv_system.bootsig())
            self.pool.add_bytes(cdv_system.boottime())
            self.pool.add_bytes(cdv_system.get_platform()) 
            self.pool.add_bytes(cdv_io.last_seed()) # seed file as determined by last iteration
        
        # first gather GPS noise, probably the best source of entropy (unproven)
        self.gps.update_gps()
        cur_noise = self.gps.gps_noise()
        self.pool.add_bytes(cur_noise[0] + cur_noise[1])
        
        # Now let's grap the CPU temperature 
        self.pool.add_bytes(cdv_hardware.get_cpu_temp())
        
        # Let's add some current cryptocurrency exchange rates, if available
        # as determined by ShapeShift.  This is something that an adversary may have
        # access to, but in order to leverage this information, he or she would have
        # to receive the data faster than this script (plausible, of course) or predict
        # future prices (also plausible), but hopefully this is OK given other sources
        self.pool.add_bytes(cdv_crypto_prices.shapeshift_rand_prices())
        
        # Let's calculate the execution time of *this* function
        # if the execution time substantially differs from the mean execution time
        # then maybe we had some slowdowns on the machine that can be used to generate
        # entropy.
        end_time = time.time()
        exec_time = end_time - start_time
        
        if (self.mean_exec_time != 0):
            exec_pct = (exec_time - self.mean_exec_time)/self.mean_exec_time
            if (abs(exec_pct) > 0.25):
                self.pool.add_bytes(bytes(str(exec_time).encode('utf-8')))

        # Let's also update the current mean execution time
        self.mean_exec_time = (self.mean_exec_time*self.iters + exec_time)/(self.iters + 1)
        
        # And finally, it's may be a bad source of entropy, but let's just add
        # the start time of this function to the pool
        self.pool.add_bytes(bytes(str(start_time).encode('utf-8')))
        self.iters += 1
        
if __name__ == '__main__':
    print(str(sha256(b'Kishavan Bhola')))
    ph = PoolHandler()
