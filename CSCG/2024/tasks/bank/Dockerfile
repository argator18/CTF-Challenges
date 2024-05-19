# docker build -t bank . && docker run -p 1024:1024 --rm -it bank
FROM ubuntu@sha256:50ec5c3a1814f5ef82a564fae94f6b4c5d550bb71614ba6cfe8fadbd8ada9f12

RUN useradd --create-home --shell /bin/bash ctf

COPY docker-stuff/ynetd /sbin/
COPY flag /
COPY vuln /home/ctf/

RUN chmod 0555 /sbin/ynetd /home/ctf/vuln && \
    chmod 0444 /flag

EXPOSE 1024
CMD [ "ynetd", "-u", "ctf", "/home/ctf/vuln" ]
