#!/usr/bin/env bash
set -eux pipefail
flake8 .
pb_tool deploy -y
