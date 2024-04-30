FROM php:7.3-apache

ADD --chmod=0755 \
    https://raw.githubusercontent.com/reproducible-containers/repro-sources-list.sh/v0.1.0/repro-sources-list.sh \
    /usr/local/bin/repro-sources-list.sh

#RUN bash /usr/local/bin/repro-sources-list.sh && apt-get update && apt-get -y install python2 curl tar
RUN apt-get update && apt-get -y install python2 curl tar

# Expose apache.
EXPOSE 1024

ADD src/ /var/www/site/

RUN chmod -R 755 /var/www/
RUN chown -R www-data:www-data /var/www

COPY flag /flag
RUN chmod 777 /flag

RUN mkdir -p /var/www/site/uploads
RUN chmod -R 777 /var/www/site/uploads

# Update the default apache site with the config we created.
ADD apache-config.conf /etc/apache2/sites-enabled/000-default.conf

RUN sed -i 's/Listen 80/Listen 1024/' /etc/apache2/ports.conf


# Install ply and lolcode1337
WORKDIR /opt/
RUN curl https://www.dabeaz.com/ply/ply-2.2.tar.gz -k -o ply-2.2.tar.gz && curl http://dalkescientific.com/writings/diary/lolpython.py -k -o lolcode.py && \
    tar -xvf ply-2.2.tar.gz && cd ply-2.2 && python2 setup.py install