# syntax=docker/dockerfile:1
FROM guacamole/guacd:1.5.4

USER root
ADD entrypoint.sh /opt/entrypoint.sh
ADD flagtool /opt/flagtool

CMD ["/bin/sh", "/opt/entrypoint.sh"]