FROM pulumi/pulumi-python:3.115.0@sha256:968ceee157fbbb0b248b818aa3a4eaa8e4013461539d24b623c60fb4a62ce9a5

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
