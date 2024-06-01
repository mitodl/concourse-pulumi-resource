FROM pulumi/pulumi-python:3.118.0@sha256:4611b948bd46cd39775f8a59d9112a6df960155c90cf8fe9ee7c6bdeba69abb5

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
