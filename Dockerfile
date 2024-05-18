FROM pulumi/pulumi-python:3.116.1@sha256:10471f3c384fa2981a08aba66c5afb6fe5ee042f762e220993475207e5ac6fa5

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
