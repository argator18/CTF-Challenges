#!/bin/sh
# Write part 1 flag
echo $FLAG_PART1 > /flag.txt

# Write part 2 flag
chmod +x /opt/flagtool
chmod u+s /opt/flagtool
/opt/flagtool writeflag
unset FLAG
su guacd -s /bin/sh -c "/opt/guacamole/sbin/guacd -b 0.0.0.0 -L $GUACD_LOG_LEVEL -f"