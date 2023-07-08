ARG FUNCTION_DIR="/function"

FROM public.ecr.aws/docker/library/python:bookworm as build-image

ARG FUNCTION_DIR="/function"

RUN apt-get update && \
  apt-get install -y \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

# Copy function code
RUN mkdir -p ${FUNCTION_DIR}
COPY lambda_requirements.txt ${FUNCTION_DIR}
# Install the function's dependencies
RUN pip install \
    --target ${FUNCTION_DIR} \
        awslambdaric
RUN pip install \
    --target ${FUNCTION_DIR} \
        -r ${FUNCTION_DIR}/lambda_requirements.txt


FROM public.ecr.aws/docker/library/python:bookworm
ARG FUNCTION_DIR
RUN apt-get update && \
    apt-get install -y xfonts-75dpi xfonts-base libgl1 libxkbcommon-x11-0 libegl1 libdbus-1-3 libnss3 libxcomposite1 \
        libxdamage1 libxrandr2 libxtst6 libxi6 libasound2 libpulse0 libpcsclite1 libxkbfile1
RUN apt install -y python3-pip python3-cffi python3-brotli libpango-1.0-0 libpangoft2-1.0-0
RUN curl -Lo /usr/local/bin/aws-lambda-rie https://github.com/aws/aws-lambda-runtime-interface-emulator/releases/latest/download/aws-lambda-rie \
    && chmod +x /usr/local/bin/aws-lambda-rie



# Set working directory to function root directory
WORKDIR ${FUNCTION_DIR}

# Copy in the built dependencies
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}
COPY lambda_function.py ${FUNCTION_DIR}
COPY assets ${FUNCTION_DIR}/assets
COPY modules ${FUNCTION_DIR}/modules
COPY templates ${FUNCTION_DIR}/templates
COPY ./entry_script.sh /entry_script.sh
ENTRYPOINT [ "/entry_script.sh" ]
#ENTRYPOINT [ "/usr/local/bin/python", "-m", "awslambdaric" ]
CMD ["lambda_function.lambda_handler"]



