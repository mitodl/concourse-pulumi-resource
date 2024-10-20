FROM pulumi/pulumi-python:3.137.0@sha256:3a0bc04d50b3ef68572bbdabf592861d1458063ecb2e9c6e4bf596b72d7fb8e9

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/

RUN  /usr/bin/curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl \
     && chmod +x ./kubectl  \
     &&  mv ./kubectl /usr/local/bin/kubectl
