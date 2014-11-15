#!/bin/sh

cd $(dirname "$0")/..

test -d env || virtualenv env
source scripts/load-env.sh
pip install -r requirements.txt
