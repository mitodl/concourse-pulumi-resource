FROM pulumi/pulumi-python:3.117.0@sha256:c060ff31f1e6fc40b7bd08c4cb40adbd9f01b751962fb6b53f52d5ca00597e7d

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
