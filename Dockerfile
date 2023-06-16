FROM wkhtmltopdf-layer AS wkhtmltopdf-layer
FROM public.ecr.aws/lambda/python:3.10

RUN yum -y install unzip
COPY --from=wkhtmltopdf-layer . /tmp
RUN unzip /tmp/layer.zip -d /opt
RUN rm /tmp/layer.zip

COPY lambda_requirements.txt .
RUN pip3 install -r lambda_requirements.txt --target "${LAMBDA_TASK_ROOT}"
COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY assets ${LAMBDA_TASK_ROOT}/assets
COPY modules ${LAMBDA_TASK_ROOT}/modules
COPY templates ${LAMBDA_TASK_ROOT}/templates

CMD ["lambda_function.lambda_handler"]

