# Class to try to use GPS Noise a source of entropy
# Kishavan Bhola
# This uses the binary whereami which has to be in the current working directory
# This seems like the most promising source of entropy
# Of course, for a real cryptographically secure application,
# much more testing needs to be done, but the deviation from the long-running
# mean of each coordinate appears to look like white noise

import subprocess
import time

lat = 'Latitude: '
lon = 'Longitude: '

def raw_gps():
    return subprocess.check_output(['./whereami'])

def parsed_gps():
    raw = (raw_gps().decode('utf-8')).split('\n')
    gps = dict() # (latitude, longitude)
    for line in raw:
        if lat in line:
            gps[lat] = float(line[len(lat):])
        elif lon in line:
            gps[lon] = float(line[len(lon):])    
    return gps


class GPSData:
    def __init__(self):
        self.mean = [0, 0]
        self.cur_val = (None, None)
        self.num = 0
        self.MAX_NUM = 1000000000000 # to ensure this doesn't make us run out of memory

    def update_gps(self):
        # update GPS, sample size, and lon/lat means
        gps = parsed_gps()
        self.cur_val = (gps[lon], gps[lat])
        self.mean[0] = (self.num*self.mean[0] + self.cur_val[0])/(1+self.num)
        self.mean[1] = (self.num*self.mean[1] + self.cur_val[1])/(1+self.num)
        self.num += 1
        if self.num > self.MAX_NUM:
            # reset
            self.num = 1
            
    def gps_noise(self):
        lon_noise = str(self.cur_val[0] - self.mean[0]).encode('utf-8')
        lat_noise = str(self.cur_val[1] - self.mean[1]).encode('utf-8')
        return (bytearray(lon_noise), bytearray(lat_noise))

if __name__ == '__main__':
    print(str(raw_gps().decode('utf-8')))
    gps_tup = parsed_gps()
    print(str(gps_tup))
    print('\n')
    
    gps_guy = GPSData()
    while True:
        gps_guy.update_gps()
        print(str(gps_guy.gps_noise()))
        time.sleep(1)
