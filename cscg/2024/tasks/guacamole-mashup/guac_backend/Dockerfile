# syntax=docker/dockerfile:1
FROM node:21.6.1-bookworm

RUN mkdir -p /home/node/app/node_modules && chown -R node:node /home/node/app

WORKDIR /home/node/app
COPY --chown=node:node package*.json ./
COPY --chown=node:node main.js .

USER node
RUN npm install

EXPOSE 3000

CMD [ "nodejs", "main.js" ]