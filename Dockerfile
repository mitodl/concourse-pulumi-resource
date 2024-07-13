FROM pulumi/pulumi-python:3.124.0@sha256:8e1450105019c93fa7d6c43fc033cd5f7f8af4986af2d74c8378c2635208cc23

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
