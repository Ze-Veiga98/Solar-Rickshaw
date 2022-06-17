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
LOCAL_DIR=''
#-----------------------------------------------------------------------------------------

# Customize rclone sync variables
# ----------------------------------------------------------------------------------------------------------------------------------

RCLONENAME=""                                                  # Name of Remote Storage Service
SYNCROOT=""                                                    # Root Folder to start
REMOTEDIR=""                                                   # Destination Folderon Remote
RCLONEPARAM=""                                                 # rclone option to perform Eg sync, copy, move
                                                               # IMPORTANT: sync will make remoteDir identical to localDir
                                                               # so remoteDir Files that do not exist on localDir will be DeletE
# -----------------------------------------------------------------------------------------------------------------------------------

# This function is a simple logger, just adding datetime to messages.
function date_log {
    echo "$(date +'%Y-%m-%d %T') $1"
}

ver="v0.3"  # This is first version 
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

function watch_files {
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

#---------------------------------------------------------------------------------------------------
# 
# PROCESS B: 
#             After all the tasks from the previous script have been performed, the alternative B 
#             , that we used is to push data to a remote storage service (google drive) via rclone.
#             rclone allows to synchronize all the files between remote server and local server. 
#----------------------------------------------------------------------------------------------------

function upload_data_to_google_drive {
   watch_files
   
   # Display Users Settings
   echo "----------- SETTINGS -------
   rcloneName    : $RCLONENAME
   syncRoot      : $SYNCROOT
   remoteDir     : $REMOTEDIR
   rcloneParam   : $RCLONEPARAM   (Options are sync, copy or move)
   ---------------------------------"
   
   echo "upload data to google drive too"
   
   rclone copy /home/pi/Documents/server_page/main/full_data_logger/data datatese:path/to/folder
   if [[ $? == 0 ]]; then
      data_log "data was been uploaded successfully"
      return 0
   fi 
}

function delete_files {
  upload_data_to_google_drive
  echo "deleting files in a directory that were 10 days old "
  find /home/pi/Documents/server_page/main/full_data_logger/data/* -mtime +10 -delete
 
}

delete_files







