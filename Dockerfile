### BASE IMAGE ###
FROM        python:3.7-alpine as base
FROM        base              as builder

RUN         mkdir /install
WORKDIR     /install

COPY        requirements_base.txt /requirements.txt
RUN         set -ex ;\
            apk add gcc musl-dev ;\
            pip install --no-cache-dir --install-option="--prefix=/install" -r /requirements.txt

### IMAGE ###
FROM        base

ARG         APP_DIR=/app/
ARG         SRC_DIR=src
WORKDIR     ${APP_DIR}

COPY        docker-entrypoint.sh  ${APP_DIR}docker-entrypoint.sh
RUN         apk add bash ;\
            chmod +x docker-entrypoint.sh

COPY        ${SRC_DIR}  ${APP_DIR}
COPY        --from=builder /install /usr/local

ENV         PATH=.:$PATH

ENTRYPOINT  ["docker-entrypoint.sh"]
CMD         ["run"]
