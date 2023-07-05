FROM public.ecr.aws/lambda/python:3.10

RUN yum -y install unzip wget
RUN wget https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6-1/wkhtmltox-0.12.6-1.amazonlinux2.x86_64.rpm
RUN yum -y install wkhtmltox-0.12.6-1.amazonlinux2.x86_64.rpm
RUN yum -y install libxslt-devel libxml2-devel
COPY lambda_requirements.txt .

RUN pip3 install -r lambda_requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY assets ${LAMBDA_TASK_ROOT}/assets
COPY modules ${LAMBDA_TASK_ROOT}/modules
COPY templates ${LAMBDA_TASK_ROOT}/templates

CMD ["lambda_function.lambda_handler"]

