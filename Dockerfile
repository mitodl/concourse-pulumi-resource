FROM pulumi/pulumi-python:3.157.0@sha256:bedf7ffc3f5245b82d387db816e9d9777586f1b48bcbdc6a33c7356458f91b48

ENV PYTHONUNBUFFERED=1
WORKDIR /opt/resource
CMD ["/bin/sh"]

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/

RUN  /usr/bin/curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl \
     && chmod +x ./kubectl  \
     &&  mv ./kubectl /usr/local/bin/kubectl
