FROM ubuntu

RUN sudo apt-get update
RUN sudo apt-get install -y \
    build-essential \
    libldap2-dev \
    libsasl2-dev \
    libssl-dev \
    python \
    python-dev \
    python-setuptools \
    supervisor

RUN useradd -m minion-web

COPY . /srv/minion
WORKDIR /srv/minion
RUN python setup.py develop

ENV MINION_FRONTEND_PRODUCTION=no
