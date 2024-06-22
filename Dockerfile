FROM pulumi/pulumi-python:3.121.0@sha256:caac9ce89636297be4f7f6e94e64265ac37f3bdcac0b2ce8a8e2cfa52365fbc1

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
