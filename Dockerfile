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

RUN mkdir -p /home/kellum
RUN echo 'kellum::21493:0::/home/kellum:/bin/bash' >> /etc/passwd

RUN mkdir /home/kellum/repo_metrics
COPY gitalizo.py /home/kellum/
COPY repo_list.csv /home/kellum/

RUN chmod -R 777 /home/kellum


# RUN apt-get -y install --no-install-recommends openssh-client

# RUN mkdir -p /root/.ssh
# COPY id_rsa /root/.ssh
# RUN chmod 700 /root/.ssh/id_rsa
# RUN echo "Host github.com\n\tStrictHostKeyChecking no\n" >> /root/.ssh/config
# COPY id_rsa.pub /root/.ssh

# RUN eval $(ssh-agent -s)
# RUN eval 'ssh-agent -s'
# RUN ssh-agent /bin/sh
# RUN env | grep ^SSH
# RUN exec ssh-agent bash
# RUN ssh-add /root/.ssh/id_rsa

# RUN mkdir -p /home/dummy24601
# RUN echo 'dummy24601::21493:0::/home/dummy24601:/bin/bash' >> /etc/passwd

# RUN mkdir -p /home/condor
# RUN echo 'condor::21493:0::/home/condor:/bin/bash' >> /etc/passwd


# RUN mkdir -p /home/dummy24601
# RUN echo 'condor::65534:0::/home/dummy24601:/bin/bash' >> /etc/passwd

# RUN git config --global user.name "dummy24601"
# RUN git config --global user.email "5a9wml+cafn9w0qrudls@sharklasers.com"
