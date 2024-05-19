# docker build -t pwn1 . && docker run -p 1024:1024 --rm -it pwn1

FROM ubuntu:22.04
COPY pwn1 flag ynetd .

EXPOSE 1024
CMD ./ynetd ./pwn1
