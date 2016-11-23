FROM ubuntu:14.04
MAINTAINER Mike Kellum <kellumm@gmail.com>

RUN echo deb http://www.analizo.org/download/ ./ >> /etc/apt/sources.list.d/analizo.list
RUN echo deb-src http://www.analizo.org/download/ ./ >> /etc/apt/sources.list.d/analizo.list
RUN apt-get update

RUN apt-get -y install wget

RUN wget -O - http://www.analizo.org/download/signing-key.asc | apt-key add -
RUN apt-get update

RUN apt-get -y install python
RUN apt-get -y install analizo
