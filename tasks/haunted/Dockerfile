# docker build -t haunted . && docker run -p 1024:1024 --rm -it haunted
FROM ubuntu@sha256:f9d633ff6640178c2d0525017174a688e2c1aef28f0a0130b26bd5554491f0da

ADD --chmod=0755 --checksum=sha256:4e7e6536b206488b2414d1fa2272e8bbf17fbe7d11e5648eb51284c8fa96b0a9 \
    https://raw.githubusercontent.com/reproducible-containers/repro-sources-list.sh/v0.1.1/repro-sources-list.sh \
    /usr/local/bin/repro-sources-list.sh

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
    --mount=type=cache,target=/var/lib/apt,sharing=locked \
    /usr/local/bin/repro-sources-list.sh && \
    apt-get update && \
    DOCKER_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3 qemu-system-x86

RUN useradd --create-home --shell /bin/bash ctf

COPY server.py OVMF_CODE.fd OVMF_VARS.fd /home/ctf/

RUN chown -R root:ctf /home/ctf && \
    chmod -R 0000 /home/ctf/* && \
    chmod 770 /home/ctf && \
    chmod 040 /home/ctf/OVMF_CODE.fd /home/ctf/OVMF_VARS.fd /home/ctf/server.py

WORKDIR /home/ctf/
USER ctf
EXPOSE 1024
ENTRYPOINT ["python3", "/home/ctf/server.py"]
