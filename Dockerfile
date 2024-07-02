FROM pulumi/pulumi-python:3.122.0@sha256:8bb1561d9f755e0467aea55a2e6ed8d37a422c9805cb1f7b9cf8671d0dd2f3ce

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
