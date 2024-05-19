# syntax=docker/dockerfile:1
FROM ubuntu:jammy-20230804
ENV DEBIAN_FRONTEND=noninteractive

# sudo docker build -t win_server .
# sudo docker run win_server
# sudo docker ps 
# sudo docker exec -it <id> /bin/bash

ADD --chmod=0755 \
    https://raw.githubusercontent.com/reproducible-containers/repro-sources-list.sh/v0.1.0/repro-sources-list.sh \
    /usr/local/bin/repro-sources-list.sh

RUN \
  --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  --mount=type=bind,source=./repro-sources-list.sh,target=/usr/local/bin/repro-sources-list.sh \
  repro-sources-list.sh && \
  apt-get update && \
  apt-get install -y sshpass socat ansible vagrant libglib2.0-dev libgcrypt20-dev zlib1g-dev autoconf automake libtool bison flex libpixman-1-dev tar wget python3-dev python3-venv python3-pip ninja-build meson git

RUN wget https://download.qemu.org/qemu-8.2.1.tar.xz && \
  tar xvJf qemu-8.2.1.tar.xz && \
  cd qemu-8.2.1 && \
  ./configure --enable-slirp && \
  make -j$(nproc) && make install

RUN wget https://gitlab.freedesktop.org/slirp/libslirp/-/archive/v4.7.0/libslirp-v4.7.0.tar.gz && \
  tar xvf libslirp-v4.7.0.tar.gz && cd libslirp-v4.7.0 && meson build && ninja -C build install
RUN \
 vagrant plugin install vagrant-qemu winrm winrm-fs winrm-elevated

WORKDIR /opt/vagrant

RUN vagrant box add peru/windows-server-2019-standard-x64-eval --box-version 20240201.01

COPY Vagrantfile .
RUN vagrant up --provider qemu --provision
# Here we have a privisioned windows 2019 box ready and in the build cache. Custom code here :)

# Setup windows box

# Dirty hack to get rid of interactive prompt
COPY known_hosts /root/.ssh/known_hosts

# Getting the installer
RUN wget 'https://github.com/jasp-stats/jasp-desktop/releases/download/v0.18.3/JASP-0.18.3.0-Windows.msi'
RUN wget 'https://aka.ms/vs/17/release/vc_redist.x64.exe'

# Copy our ansible stuff to docker
COPY playbook.yml .
COPY inventory.yml .

# Run ansible
RUN vagrant up && sleep 30 && ansible-playbook -i inventory.yml playbook.yml
RUN rm JASP-0.18.3.0-Windows.msi

COPY entrypoint.sh .

EXPOSE 5022 53389
CMD ["bash", "entrypoint.sh"]
