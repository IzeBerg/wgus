#!/usr/bin/env bash

set -e
set -x

pytest --cov=wgus --cov=tests --cov-report=term-missing:skip-covered --cov-report=xml tests ${@}
