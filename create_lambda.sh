#!/bin/bash
#

poetry export --without-hashes --format=requirements.txt > requirements.txt
mkdir -p csa_lambda
poetry run pip install -r requirements.txt --target csa_lambda

