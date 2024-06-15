FROM pulumi/pulumi-python:3.120.0@sha256:6f8603c82a426a3bd4c2b32b5a2cd21ec5ce9c48016ee49a27a9136fdc1c38d2

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
