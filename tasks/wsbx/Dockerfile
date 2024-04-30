# syntax=docker/dockerfile:1
FROM alpine:3.18.2@sha256:25fad2a32ad1f6f510e528448ae1ec69a28ef81916a004d3629874104f8a7f70

# Install OS dependencies and add a challenge user
RUN apk add nodejs npm chromium \
    && addgroup -S wsbx \
    && adduser -S -G wsbx wsbx \
    && mkdir -p /home/wsbx/Downloads \
    && chown -R wsbx:wsbx /home/wsbx

# Set config for running in a container
ENV FLAG=CSCG{fake_flag} \
    HOST=0.0.0.0 \
    PORT=1337 \
    PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# Install NPM dependencies
WORKDIR /app
COPY package.json package-lock.json /app/
RUN npm ci

# Add the actual app
COPY . /app

# Don't run as root
USER wsbx

CMD ["node", "server.js"]
