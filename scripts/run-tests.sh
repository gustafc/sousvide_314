#!/bin/bash

set -e
cd $(dirname $0)/..

python -m unittest discover -s sv314/ -p '*_test.py'
