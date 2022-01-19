FROM python:3.9-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

ARG PULUMI_VERSION=3.21.1

RUN apt-get update && apt-get install -y -q curl && \
    curl -fsSL https://get.pulumi.com | sh -s -- --version ${PULUMI_VERSION} && \
    mv /root/.pulumi/bin/pulumi /usr/bin/pulumi && \
    pip install --no-cache-dir pulumi~=${PULUMI_VERSION} && \
    apt-get clean

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
