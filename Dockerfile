FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

ARG PULUMI_VERSION=3.21.0

RUN set -x && \
    apk add --no-cache --update curl && \
    curl -fsSL https://get.pulumi.com | sh -s -- --version ${PULUMI_VERSION} && \
    pip install --no-cache-dir pulumi~=${PULUMI_VERSION}

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
