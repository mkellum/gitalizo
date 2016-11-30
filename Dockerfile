FROM debian:8.6
MAINTAINER Mike Kellum <kellumm@gmail.com>

ARG DEBIAN_FRONTEND=noninteractive

RUN echo deb http://www.analizo.org/download/ ./ >> /etc/apt/sources.list.d/analizo.list
RUN echo deb-src http://www.analizo.org/download/ ./ >> /etc/apt/sources.list.d/analizo.list
RUN apt-get update

RUN apt-get -y install --no-install-recommends apt-utils
RUN apt-get -y install --no-install-recommends wget
RUN apt-get -y install --no-install-recommends git
RUN apt-get -y install --no-install-recommends python
RUN apt-get -y install --no-install-recommends ca-certificates

RUN wget -O - http://www.analizo.org/download/signing-key.asc | apt-key add -
RUN apt-get update

RUN apt-get -y install analizo

COPY gitalizo.py /
COPY repo_list.csv /

RUN mkdir /repo_metrics

RUN git config --global user.name "dummy24601"
RUN git config --global user.email "5a9wml+cafn9w0qrudls@sharklasers.com"