#!/bin/bash

#********************************************************************************************************
# Bash script used to upload files to remote server (helianto -group).                                  *
# Commands used: sshpass for raspberrypi to be able to connect to remote server without user interation *
# Author: José Carlos // ago 10 10.33                                                                   *
#******************************************************************************************************** 

#                        SFTP commands
USER_REMOTE=ist188120
HOST_REMOTE=sigma.ist.utl.pt
REMOTE_DIR=/afs/ist.utl.pt/groups/helianto/SolarTuk/remote
FOLDER=data
export SSHPASS=Fisica20 # Is For temporary purpose onlyand will be removed during reboot
LOCAL_DIR='/home/pi/Documents/server_page/main/full_data_logger/data/log_*'
#---------------------------------------------------------------------------------------------------------
#                        RPI commands
pingme='google.com'

#---------------------------------------------------------------------------------------------------------


# This function is a simple logger, just adding datetime to messages.
function date_log {
    echo "$(date +'%Y-%m-%d %T') $1"
}

ver="0.0"  # This is first version 
printf "\n"
date_log "$0 version $ver written by José Carlos." 

# The first thing that we want to do is to check if the raspberry pi has internet access. To do this just ping to google.com for exem.
echo "--------------------------------------------------------------------"


function check_if_RPI_has_internet {
     for ip in $pingme; do
        echo "pinging to $ip"
        ping -c 1 $ip > /dev/null 2>&1
        # We know that $? variable contains the return code of the previous command.
        # In Batch return code 0 usually means that everything executed successully
        # Check if the 'ping' command returned 0
        if [[ $? == 0 ]]; then 
           date_log "Raspberry pi is UP"
           return 0
        fi
     done
     echo "Seems that my connection went down- I will notify you went I'm up"
     echo "See you soon"
     return 1       
}

function install_requirments_if_need {
   check_if_RPI_has_internet
   date_log "Cool Network is working correctly"
   if [ -f /usr/bin/sshpass ]; then
       echo "sshpass is already installed at /usr/bin/sshpass"
       echo "----------------------------------------------------------------------"
   else 
     echo "You need to install it"
     sudo apt-get install sshpass
     echo "sshpass is now installed"
     which sshpass
     echo "$?" 
   fi   
}

function perform_directory {
   install_requirments_if_need
   date_log "Now that I have the necessary package I will search for the directory."
   for local_file in ${LOCAL_DIR}; do
       printf "\n"
       printf "$file[%s]\n" "$local_file"
       cd /home/pi/Documents/server_page/main/full_data_logger/data 
       fn=$(ls -t log_*| head -1)  # concept of pipe
       fnsize=$(wc -l $fn | awk '{print $1}')
   done
   echo "-------------------------------------------------------------------------"   
   printf "\t\t New file %s- contains %d lines" $fn $fnsize
   printf "\n"
}

function watch_file {
   perform_directory
   
   pn=$(ls -Art log_* | tail -n 2 | head -n 1) #second last file in the directory
   echo "connecting again to helainto"
   sshpass -e sftp -p $USER_REMOTE@$HOST_REMOTE:$REMOTE_DIR << EOF
   put $pn
   put $fn
   bye    
EOF
  # probably I will return here to remove the older files in local server.
  #rm -f $pn
  #echo $?
   
}

watch_file
