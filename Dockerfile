FROM pulumi/pulumi-python:3.133.0@sha256:35940164736514b6511fe6604a39fffa57d108c5e79b06d7949efceb34e3e262

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
