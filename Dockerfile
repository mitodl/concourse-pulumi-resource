FROM pulumi/pulumi-python:3.127.0@sha256:fddec762897141854ef91f8a412f35aad8910daa99d0538abc5962ceb909b769

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
