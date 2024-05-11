FROM pulumi/pulumi-python:3.115.2@sha256:e2003aac862ad0bf23c31b26692ba6a1535ac62b0d94d28794e803b8e261118b

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
