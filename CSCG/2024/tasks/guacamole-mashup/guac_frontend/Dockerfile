# syntax=docker/dockerfile:1
FROM node:21.6.1-bookworm

RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app

WORKDIR /home/node/app
COPY --chown=node:node package*.json ./
COPY --chown=node:node src/ src/
COPY --chown=node:node public public/
COPY --chown=node:node entrypoint.sh entrypoint.sh

RUN npm install -g serve

USER node
RUN npm install

EXPOSE 3000

ENTRYPOINT ["sh", "entrypoint.sh"]