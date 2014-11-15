#!/bin/sh

cd $(dirname "$0")/..

test -d env || virtualenv env
pip install -r requirements.txt
