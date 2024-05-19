FROM ubuntu:jammy-20240227@sha256:77906da86b60585ce12215807090eb327e7386c8fafb5402369e421f44eff17e as builder

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
    xz-utils \
    gcc

WORKDIR /work

ADD --chmod=0666 --checksum=sha256:4300f2fbc3996bc389d3c03a74662bfff3106ac1930942c5bd27580c7ba5053d \
    https://yx7.cc/code/ynetd/ynetd-0.1.2.tar.xz \
    /work/ynetd-0.1.2.tar.xz

RUN tar -xJf ynetd-0.1.2.tar.xz && cd ynetd-0.1.2 && CC="musl-gcc" CFLAGS="-static" make

COPY vuln.c .
RUN gcc -g -pie -fcf-protection -frandom-seed=0 -fno-plt -fstack-protector-all -fstack-clash-protection -O3 -g -Wl,-O1,--sort-common,--as-needed,-z,relro,-z,now -Wall -Wextra vuln.c -o vuln

RUN echo "7cdf302e663641c132daaae59f82ceaebd8780f37eccc7844e17ddea3c82b664  /work/vuln" | sha256sum --check

FROM ubuntu:jammy-20240227@sha256:77906da86b60585ce12215807090eb327e7386c8fafb5402369e421f44eff17e
COPY --from=builder /work/ynetd-0.1.2/ynetd /ynetd
COPY --from=builder /work/vuln /vuln

ADD --chmod=0755 --checksum=sha256:4c97fd03a3b181996b1473f3a99b69a1efc6ecaf2b4ede061b6bd60a96b9325a \
    https://raw.githubusercontent.com/reproducible-containers/repro-sources-list.sh/v0.1.0/repro-sources-list.sh \
    /usr/local/bin/repro-sources-list.sh

RUN \
    --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    /usr/local/bin/repro-sources-list.sh && \
    apt-get update && \
    apt-get install -y dropbear rsync openssh-client && \
    rm /var/cache/ldconfig/aux-cache /var/log/apt/term.log /var/log/apt/history.log /var/log/dpkg.log /var/log/alternatives.log && \
    rm -rf /etc/dropbear/dropbear_*_host_key

COPY --chmod=600 --chown=root:root dropbear_ecdsa_host_key dropbear_ed25519_host_key dropbear_rsa_host_key /etc/dropbear/

RUN chown root /vuln && chmod 4555 /vuln
COPY ./flag /flag
RUN chmod 600 /flag
RUN useradd -d /home/ctf/ -m -s /bin/bash ctf && passwd -d ctf

WORKDIR /home/ctf

CMD ["dropbear", "-FBREkwp", "1024"]