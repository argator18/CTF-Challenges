FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install -y socat gcc
RUN useradd -UM chall

COPY . /app

WORKDIR /app

CMD /app/socat.sh
