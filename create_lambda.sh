#!/bin/bash
#

docker build -t csa_lambda .
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin $1
docker tag csa_lambda:latest $1/lwpartner:csa_lambda
docker push $1/lwpartner:csa_lambda