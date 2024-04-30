#!/bin/bash
vagrant up

sshpass -p 'vagrant' ssh -p 50022 -o StrictHostKeyChecking=no vagrant@127.0.0.1 "net user vagrant $VAGRANT_PASS && net user Administrator $VAGRANT_PASS && del C:\ProgramData\ssh\administrators_authorized_keys && echo '$FLAG' > C:\Users\vagrant\flag.txt"

socat TCP-LISTEN:5022,fork TCP:127.0.0.1:50022 &
socat TCP-LISTEN:53389,fork TCP:127.0.0.1:3389 &

while true; 
do
    vagrant up
     echo 'Windows Server is up';   
     sleep 60;
done