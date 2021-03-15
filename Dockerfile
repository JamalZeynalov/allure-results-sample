FROM python:3.8.8-slim

MAINTAINER jamal.zeynalov@gmail.com

RUN mkdir -p /usr/share/man/man1

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y git

ENV JAVA_HOME="/usr/lib/jvm/java-1.11.0-openjdk-arm64"
ENV PATH=$PATH:$JAVA_HOME/bin