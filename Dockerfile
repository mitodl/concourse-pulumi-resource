FROM pulumi/pulumi-python:3.132.0@sha256:8d60cb83a7925d81a05b0dfb0310ceb98c06377873a391c89fa2ef65a77d6ef4

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
