FROM pulumi/pulumi-python:3.129.0@sha256:26c5503ad4e3bc580ea97526400dde17239b4fe74c5b582894e6fcb8931d815d

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
