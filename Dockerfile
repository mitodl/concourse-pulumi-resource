ARG PULUMI_VERSION=3.23.2
FROM pulumi/pulumi-python:${PULUMI_VERSION}

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
