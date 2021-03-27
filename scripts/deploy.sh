#!/usr/bin/env bash
set -eux pipefail
flake8 .
mypy --namespace-packages --explicit-package-bases .
pb_tool deploy -y
