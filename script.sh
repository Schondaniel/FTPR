#!/bin/bash
set -x

#Name of file to replace and upload
FILENAME=$1
#Destination path for uploaded file
DESTINATION=$2
#Current Local Directory
LOCAL=$3

# Server and login details
HOST=$4
USER=$5
PASSWORD=$6

# FTP login and upload is explained in paragraph below

ftp -inv $HOST <<EOF
user $USER $PASSWORD
cd $DESTINATION
lcd $LOCAL
binary
delete $FILENAME
put $FILENAME
bye
EOF
