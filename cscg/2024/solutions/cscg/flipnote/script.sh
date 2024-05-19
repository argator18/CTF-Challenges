# connect to server
ssh -p 2222 <usr>@<url>

# start this on server
/ynetd -p 1218 "prlimit --as=2977736:-1  /vuln"


# get the ip address or hostname
hostname -I

# execute this local
ssh -p 2222 -L 1234:<ip or hostname>:1024 <user>@<url>
# Now port 1234 on localhost is forwarded to the ssh port of the forwarded server

ssh -p 1234 -N -L 12345:localhost:1218 ctf@localhost

# python3 exploit.py
nc localhost 12345

# execute this when shell is dropped:
prlimit --pid=$$ --as=-1
cat /flag
