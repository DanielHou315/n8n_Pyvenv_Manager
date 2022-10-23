FROM node:16.18-bullseye

ARG N8N_VERSION=0.199.0

RUN if [ -z "$N8N_VERSION" ] ; then echo "The N8N_VERSION argument is missing!" ; exit 1; fi

RUN \
        apt-get update && \
        apt-get -y install graphicsmagick gosu git

USER root

RUN npm_config_user=root npm install -g npm@latest full-icu n8n@${N8N_VERSION}

ENV NODE_ICU_DATA /usr/local/lib/node_modules/full-icu

WORKDIR /data

COPY docker-entrypoint.sh /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

# Installs git and python venv modules
RUN apt-get update && apt-get install -y git python3-pip python3-setuptools python3-venv

# Install Custom Component: pyvenv-manager
COPY pyvenv_manager/ /data/

EXPOSE 5678/tcp