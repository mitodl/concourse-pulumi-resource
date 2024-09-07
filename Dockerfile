FROM pulumi/pulumi-python:3.131.0@sha256:03cb3d50b252479de799833aeb31e5bd3e40e7bdebeb0b02b805101fac7d2a36

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
