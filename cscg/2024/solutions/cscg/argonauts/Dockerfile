FROM debian@sha256:79becb70a6247d277b59c09ca340bbe0349af6aacb5afa90ec349528b53ce2c9

# https://github.com/reproducible-containers/repro-sources-list.sh
# Sorry for the mess.
ADD --chmod=0755 --checksum=sha256:4e7e6536b206488b2414d1fa2272e8bbf17fbe7d11e5648eb51284c8fa96b0a9 \
    https://raw.githubusercontent.com/reproducible-containers/repro-sources-list.sh/v0.1.1/repro-sources-list.sh \
    /usr/local/bin/repro-sources-list.sh

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    /usr/local/bin/repro-sources-list.sh && \
    apt-get update && \
    DOCKER_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        libfdt1 libglib2.0-0 libpcre2-8-0 libpixman-1-0 libseccomp2 zlib1g

RUN useradd --create-home --shell /bin/bash ctf

COPY docker-stuff/ynetd /sbin/
COPY qemu-system-arc vmlinux /home/ctf/
COPY flag.txt docker-stuff/readflag /

RUN chown -R root:root /sbin/ynetd /home/ctf && \
    chown -R root:1337 /readflag /flag.txt && \
    chmod -R 0000 /home/ctf/* && \
    chmod 0500 /sbin/ynetd && \
    chmod 0040 /flag.txt && \
    chmod 2555 /readflag && \
    chmod 0005 /home/ctf/qemu-system-arc && \
    chmod 0004 /home/ctf/vmlinux

RUN find / -xdev -ignore_readdir_race -type f \( -perm -4000 -o -perm -2000 \) -not -wholename /readflag -delete
USER ctf
RUN ! find / -writable -or -user "$(id -un)" -or -group $(id -Gn | sed -e 's/ / -or -group /g') 2>/dev/null | grep -Ev -m 1 '^(/dev/|/run/|/proc/|/sys/|/tmp|/var/tmp|/var/lock)'
USER root

WORKDIR /home/ctf
EXPOSE 1024
CMD [ "ynetd", "-u", "ctf", "-lt", "300", "-lm", "-1", "/home/ctf/qemu-system-arc -M virt -cpu archs -display none -monitor none -m 2G -kernel /home/ctf/vmlinux -nographic -snapshot -no-reboot" ]
