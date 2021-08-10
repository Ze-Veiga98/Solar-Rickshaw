#!/bin/bash

#********************************************************************************************************
# Bash script used to upload files to remote server (helianto -group).                                  *
# Commands used: sshpass for raspberrypi to be able to connect to remote server without user interation *
# Author: José Carlos // ago 10 10.33                                                                   *
#******************************************************************************************************** 

#--------------------------------------------------------------------------------------------------------
USER_REMOTE=istxxxxx
HOST_REMOTE=sigma.ist.utl.pt
REMOTE_DIR=/afs/ist.utl.pt/groups/helianto/SolarTuk/remote
FOLDER=data
export SSHPASS=your_password # Is For temporary purpose onlyand will be removed during reboot
#---------------------------------------------------------------------------------------------------------
LOCAL_DIR='/home/pi/Documents/server_page/main/full_data_logger/data/log_*'

ver="0.0"  # This is first version 
echo "$0 ver $ver written by José Carlos"

# This function is a simple logger, just adding datetime to messages.
function date_log {
    echo "$(date +'%Y-%m-%d %T') $1"
}

# The first thing that we want to do is to check if the raspberry pi has internet access. To do this just ping to google.com for exem.
pinger='google.com'
function check_internet_access {
   for ip in $pinger; do
      ping -c 1 $ip > /dev/null 2>&1
      # One knows that $? variable contains the return code of the previous command.
      # In Batch return code 0 usually means that everything executed successully
      # Check if the 'ping' command returned 0
      if [[ $? == 0 ]]; then
         echo "My raspberrypi is up in"  
         date_log 
         echo "Install sshpass if you have not installed in your system"
         sudo apt-get install sshpass
         echo "ssh pass installed in "
         which sshpass
         echo "$?" 
         echo "(sleeping for 5)"
         #sleep 5
         # see all that files that exist in my directory
         for local_file in ${LOCAL_DIR}; do
           echo "All files - $local_file" 
           cd /home/pi/Documents/server_page/main/full_data_logger/data 
           fn=$(ls -t log_*| head -1)
           printf "\t\t New file %s-  $fn"
           printf "\n"

         done
         #echo "estou fora de loop"
         #echo $fn
         echo "connecting to helianto"
         sshpass -e sftp -p $USER_REMOTE@$HOST_REMOTE:$REMOTE_DIR << EOF
         put $fn
         bye
EOF
          
                
      else
         echo "My network is went down"
           
      fi
   done
   echo "End of the program"
   return 1
}

check_internet_access
