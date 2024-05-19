FROM ubuntu:jammy-20240125@sha256:bcc511d82482900604524a8e8d64bf4c53b2461868dac55f4d04d660e61983cb

# https://github.com/reproducible-containers/repro-sources-list.sh
# Sorry for the mess.
ADD --checksum=sha256:4e7e6536b206488b2414d1fa2272e8bbf17fbe7d11e5648eb51284c8fa96b0a9 \
    https://raw.githubusercontent.com/reproducible-containers/repro-sources-list.sh/v0.1.1/repro-sources-list.sh \
    /usr/local/bin/repro-sources-list.sh

RUN chmod +x /usr/local/bin/repro-sources-list.sh && \
    /usr/local/bin/repro-sources-list.sh && \
    apt-get update && \
    DOCKER_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        zsh socat bsdmainutils

COPY run.sh run.sh
RUN chmod +x run.sh
EXPOSE 1024
CMD socat TCP-LISTEN:1024,fork,reuseaddr EXEC:"./run.sh",stderr
