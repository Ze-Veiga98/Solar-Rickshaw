#!/bin/bash

#********************************************************************************************************
# Bash script used to upload files to remote server (helianto -group).                                  *
# Commands used: sshpass for raspberrypi to be able to connect to remote server without user interation *
# Author: José Carlos // ago 10 10.33                                                                   *
#******************************************************************************************************** 

#--------------------------------------------------------------------------------------------------------
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


function if_RPI_has_internet {
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

function install_requirments {
   if_RPI_has_internet
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
   install_requirments
   date_log "Now that I have the necessary package I will search for the directory."
   for local_file in ${LOCAL_DIR}; do
       printf "\n"
       printf "$file[%s]\n" "$local_file"
       cd /home/pi/Documents/server_page/main/full_data_logger/data 
       fn=$(ls -t log_*| head -1)  
   done
   echo "-------------------------------------------------------------------------"   
   printf "\t\t New file %s-  $fn"
   printf "\n"
}

function check_change_in_file {
   perform_directory
   printf "New file" "\t\t New file %s-  $fn"
   # check size1 of this new file
   sleep 120  # sleep for 2 minutes
   # check again the size2
   # compare the the size if is different then upload the file to helianto  
   
}

check_change_in_file




