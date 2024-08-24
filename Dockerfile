FROM pulumi/pulumi-python:3.130.0@sha256:5d7c44efe8804a888e1eaf57de71483789f9e12ee5873d4fd8cd501600c9a793

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
