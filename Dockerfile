FROM pulumi/pulumi-python:3.114.0@sha256:83a58affd6075dcbe1eb05b8ffcd9d40f00707243bff0bb971a84836c098cb37

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
