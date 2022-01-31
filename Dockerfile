FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1
ENV PATH="${PATH}:/root/.pulumi/bin"
WORKDIR /opt/resource
CMD ["/bin/sh"]

ARG PULUMI_VERSION=3.23.2

RUN apk add --no-cache --update curl build-base linux-headers && \
    curl -fsSL https://get.pulumi.com | sh -s -- --version ${PULUMI_VERSION} && \
    rm -f /root/.pulumi/bin/pulumi-language-dotnet /root/.pulumi/bin/pulumi-language-go /root/.pulumi/bin/pulumi-language-nodejs /root/.pulumi/bin/pulumi-resource-pulumi-nodejs && \
    pip install --no-cache-dir pulumi~=${PULUMI_VERSION} && \
    apk del curl linux-headers

COPY bin/* /opt/resource/
COPY lib/* /opt/resource/lib/
