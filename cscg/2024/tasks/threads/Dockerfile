# build qemu with
# docker build --output=build .
# you don't need to build qemu yourself, a binary is provided, but this might be helpful for debugging
FROM debian:bullseye as builder

RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    DOCKER_FRONTEND=noninteractive apt-get install -y \
    build-essential \
    curl \
    git \
    libglib2.0-dev \
    libpixman-1-dev \
    libz-dev \
    ncurses-dev \
    pkg-config \
    python \
    wget \
    zip

RUN mkdir -p /build/build
WORKDIR /build

ADD --chmod=0755 --checksum=sha256:65fbbc2d4b00ea3b985e0fb1e59ecb82f1d6d99564edd2e63fdcb75c71ae21e2 \
    https://github.com/img-meta/qemu/archive/0a2402860228198ae2729048f1de05aeedb7d642.zip \
    /build/qemu.zip

RUN unzip qemu.zip && \
    mv qemu-* qemu

ADD qemu_configure.sh /build/build

RUN cd build && \
    ./qemu_configure.sh ../qemu

RUN --mount=type=cache,target=/build/cache \
    cp -r build/* cache/ && \
    cd cache && \
    make -j && \
    cp meta-softmmu/qemu-system-meta ../

FROM scratch as binary
COPY --from=builder /build/qemu-system-meta /
