FROM buildpack-deps:stretch-curl

ENV TZ Europe/Paris
RUN cp /usr/share/zoneinfo/Europe/Paris /etc/localtime

COPY docker/etc/apt /etc/apt

RUN curl -sL https://repos.influxdata.com/influxdb.key | apt-key add -
RUN source /etc/lsb-release
RUN echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | tee /etc/apt/sources.list.d/influxdb.list
RUN apt-get update
RUN apt-get dist-upgrade -y
RUN apt-get update
RUN apt-get install -y influxdb chronograf telegraf kapacitor mosquitto

COPY docker/etc /etc
RUN chmod 0644 /etc/crontab
COPY docker/scripts /scripts

ENV GOPATH /go
COPY src /go/src/github.com/emembrives/dispotrains/dispotrains.webapp/src
WORKDIR /go/src/github.com/emembrives/dispotrains/dispotrains.webapp/src/
RUN make
RUN ln -s /go/src/github.com/emembrives/dispotrains/dispotrains.webapp/ /dispotrains

EXPOSE 9000
WORKDIR /dispotrains/build/
CMD ["/usr/bin/supervisord"]