#!/usr/bin/env bash

set -e
set -x

black src tests --check
isort src tests --check-only
