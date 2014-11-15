#!/bin/bash
set -e

cd $(dirname "$0")/..

mkdir -p build
git ls-files | xargs tar cJf build/sv314.tar.xz
