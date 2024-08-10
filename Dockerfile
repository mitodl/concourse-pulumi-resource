FROM pulumi/pulumi-python:3.128.0@sha256:6efa79e4fd8d2ef325f8816b6fdfc4b0c0296933c6fc8bc4273c2bd4288a8a4d

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
