FROM pulumi/pulumi-python:3.160.0@sha256:e4eab1b6221dd484b3830482fdb3477ec0344bf0f5dda937a9dd7b7d3d23266d

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/

RUN  /usr/bin/curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl \
     && chmod +x ./kubectl  \
     &&  mv ./kubectl /usr/local/bin/kubectl
