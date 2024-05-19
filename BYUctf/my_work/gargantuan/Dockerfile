FROM ubuntu@sha256:7a57c69fe1e9d5b97c5fe649849e79f2cfc3bf11d10bbd5218b4eb61716aebe6 as builder

ADD --chmod=0755 --checksum=sha256:4c97fd03a3b181996b1473f3a99b69a1efc6ecaf2b4ede061b6bd60a96b9325a \
    https://raw.githubusercontent.com/reproducible-containers/repro-sources-list.sh/v0.1.0/repro-sources-list.sh \
    /usr/local/bin/repro-sources-list.sh

RUN \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    /usr/local/bin/repro-sources-list.sh && \
    apt-get update && apt-get install -y \
    musl-dev \
    musl-tools \
    make \
    xz-utils

WORKDIR /work

ADD --chmod=0666 --checksum=sha256:4300f2fbc3996bc389d3c03a74662bfff3106ac1930942c5bd27580c7ba5053d \
    https://yx7.cc/code/ynetd/ynetd-0.1.2.tar.xz \
    /work/ynetd-0.1.2.tar.xz

RUN tar -xJf ynetd-0.1.2.tar.xz && cd ynetd-0.1.2 && CC="musl-gcc" CFLAGS="-static" make
    

FROM ubuntu@sha256:7a57c69fe1e9d5b97c5fe649849e79f2cfc3bf11d10bbd5218b4eb61716aebe6 as runner

RUN echo "8f7d59c6f95b0cf57a8db165033296dda91d1239  /lib/x86_64-linux-gnu/libc.so.6" | sha1sum -c

COPY --from=builder /work/ynetd-0.1.2/ynetd /ynetd

RUN apt update && apt install -y gdb && apt install -y curl
RUN apt install -y python3 
RUN apt install -y file && apt install -y binutils
RUN apt install -y neovim
RUN echo "export LC_CTYPE=C.UTF-8" >> /root/.bashrc
RUN bash -c "$(curl -fsSL https://gef.blah.cat/sh)"

COPY ./gargantuan /gargantuan
COPY libc.so.6 /lib/x86_64-linux-gnu/libc.so.6

CMD /ynetd -p 1024 /gargantuan
