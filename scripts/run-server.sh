#!/bin/sh
set -ex

REPOROOT=$(dirname $0)/..
cd $REPOROOT

source scripts/load-env.sh
python -m sv314.server
