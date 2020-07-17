#!/bin/sh
cd "`dirname "$0"`"

docker build clang-build
docker build retail-runtime
