FROM nginx:1.24.0

RUN mkdir /etc/nginx/http

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./join.js /etc/nginx/http
COPY ./index.html /usr/share/nginx/html/index.html

EXPOSE 1024

CMD ["nginx", "-g", "daemon off;"]