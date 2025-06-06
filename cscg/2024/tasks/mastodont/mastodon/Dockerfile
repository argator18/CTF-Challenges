# syntax=docker/dockerfile:1
ARG NODE_VERSION="16.20-bookworm-slim@sha256:b7455f5272e7397f3879a8b3bc7263d18dfb95e75d74ed56cf5506b5d8bc493f"

FROM ghcr.io/moritzheiber/ruby-jemalloc:3.2.2-slim@sha256:1ed65c8415632583ce552268cad1190097a2368800e26e3ed8381c4a32e31184 as ruby
FROM node:${NODE_VERSION} as build

# https://github.com/reproducible-containers/repro-sources-list.sh
# Sorry for the mess.
ADD --checksum=sha256:4e7e6536b206488b2414d1fa2272e8bbf17fbe7d11e5648eb51284c8fa96b0a9 \
    https://raw.githubusercontent.com/reproducible-containers/repro-sources-list.sh/v0.1.1/repro-sources-list.sh \
    /usr/local/bin/repro-sources-list.sh

COPY --link --from=ruby /opt/ruby /opt/ruby

ENV DEBIAN_FRONTEND="noninteractive" \
    PATH="${PATH}:/opt/ruby/bin"

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

WORKDIR /opt/mastodon
COPY Gemfile* package.json yarn.lock /opt/mastodon/

# hadolint ignore=DL3008
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
        ca-certificates \
        git \
        libicu-dev \
        libidn-dev \
        libpq-dev \
        libjemalloc-dev \
        zlib1g-dev \
        libgdbm-dev \
        libgmp-dev \
        libssl-dev \
        libyaml-0-2 \
        ca-certificates \
        libreadline8 \
        python3 \
        shared-mime-info && \
    bundle config set --local deployment 'true' && \
    bundle config set --local without 'development test' && \
    bundle config set silence_root_warning true && \
    bundle install -j"$(nproc)" && \
    yarn install --pure-lockfile --production --network-timeout 600000 && \
    yarn cache clean

FROM node:${NODE_VERSION}

ARG UID="991"
ARG GID="991"

# https://github.com/reproducible-containers/repro-sources-list.sh
# Sorry for the mess.
ADD --checksum=sha256:4e7e6536b206488b2414d1fa2272e8bbf17fbe7d11e5648eb51284c8fa96b0a9 \
    https://raw.githubusercontent.com/reproducible-containers/repro-sources-list.sh/v0.1.1/repro-sources-list.sh \
    /usr/local/bin/repro-sources-list.sh

COPY --link --from=ruby /opt/ruby /opt/ruby

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

ENV DEBIAN_FRONTEND="noninteractive" \
    PATH="${PATH}:/opt/ruby/bin:/opt/mastodon/bin"

## CSCG Specific stuff:
## Compiling our own ImageMagick (is needed for running mastodon in Docker)

ARG IM_VERSION=7.1.1-17
ARG LIB_WEBP_VERSION=1.3.2

RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install -y git make gcc pkg-config autoconf curl g++ cmake clang \
    # IM
    libpng16-16 libpng-dev libgomp1 ghostscript libxml2-dev libxml2-utils libtiff-dev libfontconfig1-dev libfreetype6-dev fonts-dejavu liblcms2-dev libtcmalloc-minimal4 \
    # Install manually to prevent deleting with -dev packages
    libxext6 libbrotli1
    
# you got a libwebp exploit? well, we'd gladly take that, too. :) 
# RUN git clone -b v${LIB_WEBP_VERSION} --depth 1 https://chromium.googlesource.com/webm/libwebp && \
#    cd libwebp && \
#    mkdir build && cd build && cmake ../ && make && make install && \
#    make && make install && \
#    ldconfig /usr/local/lib && \
#    cd ../../ && rm -rf libwebp
   
    # Building ImageMagick
RUN git clone -b ${IM_VERSION} --depth 1 https://github.com/ImageMagick/ImageMagick.git && \
    cd ImageMagick && \
    ./configure --without-rsvg && \
    make clean && make -j 4 && make install && \
    ldconfig /usr/local/lib
    
## Adding flag + setuid binary
COPY readflag.c /
RUN gcc -o readflag readflag.c
COPY flag /flag

RUN chown 0:0 /readflag \
    && chmod u+s /readflag \
    && chown 0:0 /flag \
    && chmod 400 /flag


## And delete all the stuff again     
RUN apt-get remove --autoremove --purge -y gcc make cmake clang curl g++ yasm git autoconf pkg-config libpng-dev libjpeg-turbo8-dev libde265-dev libx265-dev libxml2-dev libtiff-dev libfontconfig1-dev libfreetype6-dev liblcms2-dev libsdl1.2-dev libgif-dev libbrotli-dev && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /ImageMagick


# Ignoreing these here since we don't want to pin any versions and the Debian image removes apt-get content after use
# hadolint ignore=DL3008,DL3009
RUN apt-get update && \
    echo "Etc/UTC" > /etc/localtime && \
    groupadd -g "${GID}" mastodon && \
    useradd -l -u "$UID" -g "${GID}" -m -d /opt/mastodon mastodon && \
    apt-get -y --no-install-recommends install whois \
        wget \
        procps \
        libssl3 \
        libpq5 \
        imagemagick \
        ffmpeg \
        libjemalloc2 \
        libicu72 \
        libidn12 \
        libyaml-0-2 \
        file \
        ca-certificates \
        tzdata \
        libreadline8 \
        tini && \
    ln -s /opt/mastodon /mastodon

# Note: No cleaning here since Debian does this automatically
# See the file /etc/apt/apt.conf.d/docker-clean within the Docker image's filesystem

COPY --chown=mastodon:mastodon . /opt/mastodon
COPY --chown=mastodon:mastodon --from=build /opt/mastodon /opt/mastodon

## all of this is for you to have mastodon setup and an user automagically added and provisioned for you. 
## (and no, this is not a sneay way of adding a backdoor :P) 

RUN apt install -y xz-utils
ARG S6_OVERLAY_VERSION=3.1.5.0 
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-symlinks-noarch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-symlinks-noarch.tar.xz

ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-x86_64.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-x86_64.tar.xz
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_OVERLAY_VERSION}/s6-overlay-symlinks-arch.tar.xz /tmp
RUN tar -C / -Jxpf /tmp/s6-overlay-symlinks-arch.tar.xz

RUN touch /etc/s6-overlay/s6-rc.d/user/contents.d/setup-challenge
RUN touch /etc/s6-overlay/s6-rc.d/user/contents.d/run-mastodon

COPY cscg-init/ /

ENV RAILS_ENV="production" \
    NODE_ENV="production" \
    RAILS_SERVE_STATIC_FILES="true" \
    BIND="0.0.0.0"

# Set the run user
USER mastodon
WORKDIR /opt/mastodon

# Precompile assets && Note: This might take a while. Go sip some coffee and solve other challs :P
RUN OTP_SECRET=precompile_placeholder SECRET_KEY_BASE=precompile_placeholder rails assets:precompile

USER mastodon

ENTRYPOINT ["/init"]
