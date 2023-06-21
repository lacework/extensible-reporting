#!/bin/bash
#
docker build -t csa_lambda .
aws ecr get-login-password --region us-east-2 | docker login --username AWS --password-stdin 988001579975.dkr.ecr.us-east-2.amazonaws.com
docker tag csa_lambda:latest 988001579975.dkr.ecr.us-east-2.amazonaws.com/csa_lambda:latest
docker push 988001579975.dkr.ecr.us-east-2.amazonaws.com/csa_lambda:latest