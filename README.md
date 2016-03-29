# cat_dev_random
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
