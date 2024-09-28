FROM pulumi/pulumi-python:3.134.1@sha256:d511ca9487de9aa47f34f862b0d660c82a5b8e5d0b60d205a2755b6b48b3f63f

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
