#!/usr/bin/env python3

import sys
import cdv_pool
# import termios
# import fcntl
# import request

"""
  This is an attempt at a OS-X clone of `$ cat /dev/random` for Symbiont.io's
  coding challenge.
  
  Note that the OS-X version of /dev/random is essentially /dev/urandom and this
  is what has been attempted to be cloned.
  
  The main and hopefully best source of entropy is the GPS deviation from the mean
  GPS location using the tool whereami (which uses Apple's Location Servies) and
  leveraging the code I wrote in cdv_pool and cdv_gps. 
  
  The main issue right now is that the script is extremely slow.  I think I need to switch
  to faster hash functions, but I haven't taken the time to profile yet.

  There are other lower quality sources of entropy used as well:
     (1) Unusual function execution times (the mean execution time is tracked)
     (2) Cryptocurrency exchange rates (obviously public); an attack would
         require getting the information faster or predicting prices, both
         of which are plausible.  Given the combination of sources, however,
         I do not believe this is a concern.
     (3) CPU Temperature, as determined by the tool osx-cpu-temp.
     (4) The current time.
     (5) At first use of the entropy pool, system data is seeded into it: uptime,
         platform name, the boot signature.
     (6) Lastly, the previous *final* random number from the last iteration of this
         script is written to a file in the current working direct: cdv_io_seed.log.
         An attempt was made to ensure this file is only readable as root (via a test
         switch).  This contents of this file is seeded at the first iteration of this
         script.         

     Finally, this has broken my terminal, so execute with caution.

     2016-03-24
     Kishavan Bhola
""" 


if __name__ == '__main__':    
    # cdv_pool encapsulates the data structures for this program
    # and delegates the entropy gathering to the other modules
    rand_pool_handle = cdv_pool.PoolHandler()
    iters = 0
    while True:
        if iters % 100 == 0: 
            # gathering is very slow, mainly because of GPS datab
            # if entropy is never gathered, then the call to rand_val()
            # below will cause the pool to act as a pseudorandom number generator
            rand_pool_handle.gather_entropy() 
            iters = 1
        byt_string = rand_pool_handle.rand_val()

        # Convert to ASCII to properly clone `$ cat /dev/random `
        ascii_list = list(map(lambda x: chr(x%128), byt_string))
        ascii_string = ''.join(ascii_list)
        sys.stdout.write(ascii_string)

        iters += 1



    
"""  Ended up not using these sources of entropy, because microphone seemed buggy
     And I didn't have time to figure out the keylogger termios (library)
def key_logger(): 
    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
    fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

    try:
        while 1:
            try:
                c = sys.stdin.read(1)
                print("Got character " + str(repr(c)))
            except IOError: pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
        
def microphone():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

    print("* recording")

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK, exception_on_overflow=False)
        frames.append(data)
        print(str(data))

    print("* done recording")

    stream.stop_stream()
    stream.close()
    p.terminate()
"""
