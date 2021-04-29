#!/usr/bin/env bash
set -eux pipefail
flake8 .
mypy .
PLUGIN_DIR=~/.local/share/QGIS/QGIS3/profiles/default/python/plugins
# Deploy plugin to standard plugins dir
cd namari \
  && pb_tool deploy --config_file ../pb_tool.cfg --plugin_path $PLUGIN_DIR --no-confirm \
  && cd ..
