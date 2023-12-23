FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN=true

RUN apt-get update -qq && apt-get install -y \
        openscad \
        git \
        make \
        admesh \
        python3-pip \
        jq \
 && pip install sca2d \
 && rm -rf /var/lib/apt/lists/*