---
Author: 
- José Veiga
date: '2021-09-14'
description: | 
    Learn how to use this repo
tags: 'Python, Raspberry Pi, GPS, Shell'
title: Solar assisted electric rickshaw 
---
This project is under development and it is been made in the scope of my master thesis which consists in construction and evaluation performance of and electric tuk tuk (rickshaw) with the addition of solar panels. With this in mind, three set of solar panels were installed at the roof of our sola rickshaw and microcontroller version: raspberry pi 3b will be used for data acquision.

Folder: RPI-stuff
========================================================
In the folder `RPI-stuff` can be found some functions implemented in bash language to automatically
upload all the data from a Raspberry Pi into a remote server. 

```bash
function check_if_RPI_has_internet {
     for ip in $pingme; do
        echo "pinging to $ip"
        ping -c 1 $ip > /dev/null 2>&1
        # We know that $? variable contains the return code of the previous command.
        # In Batch return code 0 usually means that everything executed successully
        # Check if the 'ping' command returned 0
        if [[ $? == 0 ]]; then 
           date_log "Raspberry pi is online"
           return 0
        else
          echo "Raspberry pi is offline. See you soon!" 
                    
        fi
        
     done 
}
```

