#!/usr/bin/env bash

set -e
set -x

mypy wgus
flake8 wgus tests
black wgus tests --check
isort wgus tests scripts --check-only
