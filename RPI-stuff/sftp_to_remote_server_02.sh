#!/bin/bash


### BEGIN INIT INFO
# Provides:           SFTP-put
# Requires:           authentication
# Short-Description:  SFTP files synchronization
### END INIT INFO

###########################################################################################
#                                                                                         #
# SFTP Sync v0.3                                                                          #
#                                                                                         #
# A shell script to upload files to remote SFTP server and your local server/raspberrypi  #
# The raspberry pi will save a file every time it is booted. So the main idea is to       #
# upload that files to a remote server via sftp (secure files transfer protocol.          #
#                                                                                         #
# Master project: Solar tuk tuk @ IST                                                     #  
# Author: José Veiga                                                                      #
# Supervisors: Horácio Fernandes and Paulo Branco.                                        #
# ago 12 16:21 'Laboratório da area de energia'                                           #
###########################################################################################

# Global variables
pingme='8.8.8.8'


USER_REMOTE=istxxxxxx
HOST_REMOTE=sigma.ist.utl.pt
REMOTE_DIR=/afs/ist.utl.pt/groups/helianto/SolarTuk/remote
FOLDER=data
export SSHPASS=your_ist_password # Is For temporary purpose onlyand will be removed during reboot
LOCAL_DIR='/home/pi/Documents/server_page/main/full_data_logger/data/log_*'


# This function is a simple logger, just adding datetime to messages.
function date_log {
    echo "$(date +'%Y-%m-%d %T') $1"
}

ver="v0.3"  
printf "\n"
echo "estou"
date_log "$0 version $ver written by José Carlos." 


echo "--------------------------------------------------------------------"


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
 
 # PURPOSE: Upload all the files added in a specific directory in a given day at which the script is ran.
 
## This function is responsable to search for all the news data comming in a specific folder (in this case - data)  and then
#  iterate over that folder and move all its content to a another folder called 'data-to-sftp' and upload to remote server. 
# After all the files have been uploaded to a remote server, the script remove all the files in the local folder.
 

function watch_file {
   perform_directory
   cd /home/pi/Documents/server_page/main/full_data_logger/data 
   FILES=$(ls log_* -l --time-style=+%D | grep $(date +%D) | grep -v '^d' | awk '{print $NF}')
   DESTINATION=/home/pi/Documents/server_page/main/full_data_logger/data-to-sftp
   if [ -n "${FILES}" ]
   then
      for f in ${FILES}
      do
          cp -prf ${f} ${DESTINATION}
      done
      sshpass -e sftp -p $USER_REMOTE@$HOST_REMOTE:$REMOTE_DIR << EOF
      put /home/pi/Documents/server_page/main/full_data_logger/data-to-sftp/*
      bye
EOF
   rm -v /home/pi/Documents/server_page/main/full_data_logger/data-to-sftp/*
    
   else
     echo "NO FILES TO MOVE"
   fi
   
}

watch_file








