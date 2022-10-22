FROM amazon/aws-lambda-provided:al2

RUN yum -y update
RUN yum -y install jq

RUN mkdir /opa
WORKDIR /opa
RUN curl -L -o opa https://openpolicyagent.org/downloads/v0.37.2/opa_linux_amd64_static
RUN chmod +x opa
COPY bundle.tar.gz .

WORKDIR /var/runtime
COPY start.sh .
COPY opa-lambda.sh .

RUN chmod +x start.sh
RUN chmod +x opa-lambda.sh

ENTRYPOINT ["/var/runtime/start.sh"]

