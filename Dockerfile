FROM pulumi/pulumi-python:3.119.0@sha256:edf3e6912a514cc9202a7d5fdf0fd370fac199f1012d92685aca0d748d5405b0

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
