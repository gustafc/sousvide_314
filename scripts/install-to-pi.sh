#!/bin/bash

set -e

PI_IP=$1
test -z "$1" && echo "Usage: $0 pi_hostname_or_ip" && exit -1
cd $(dirname "$0")/..
./scripts/build-tarball.sh
cat build/sv314.tar.xz | ssh pi@"$PI_IP" 'sh -c "mkdir -p sv314  && cd sv314  && tar xJv"'
