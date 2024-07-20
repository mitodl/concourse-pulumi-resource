FROM pulumi/pulumi-python:3.125.0@sha256:5aa26d4fcac38971daf12edabfbfa94fd18e6204c3182acab9f83b441103bb42

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
