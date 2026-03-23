FROM ghcr.io/astral-sh/uv:latest AS uv

FROM pulumi/pulumi-python:3.227.0@sha256:01891988810014bdda50c5007946b0160e2d6241782d8da0a6122dffde66e610

COPY --from=uv /uv /usr/local/bin/uv

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/

RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*

RUN  /usr/bin/curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl \
     && chmod +x ./kubectl  \
     &&  mv ./kubectl /usr/local/bin/kubectl
