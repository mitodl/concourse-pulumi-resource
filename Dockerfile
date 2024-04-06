FROM pulumi/pulumi-python:3.112.0@sha256:2c50b84fcd4f49b646aeafcc1a62aa61c83063963aa436b6e877706b1c442f43

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
