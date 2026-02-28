FROM pulumi/pulumi-python:3.224.0@sha256:df92e19b5436b7634ac6d2c68a3a4c6ec0f2926b8bbc267a75b86f90743d0f2d

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/

RUN  /usr/bin/curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl \
     && chmod +x ./kubectl  \
     &&  mv ./kubectl /usr/local/bin/kubectl
