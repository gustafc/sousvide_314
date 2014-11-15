#!/bin/bash
set -ex

cd $(dirname $0)/..

source scripts/load-env.sh
python -m sv314.server
