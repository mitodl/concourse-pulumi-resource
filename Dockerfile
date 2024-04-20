FROM pulumi/pulumi-python:3.113.3@sha256:30b08be39ad80088bd4bf2568935d2013c7d81f4c5c210eb28954058ef33f81d

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
