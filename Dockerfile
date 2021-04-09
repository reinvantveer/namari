FROM qgis/qgis:release-3_18

WORKDIR namari
COPY Pipfile* ./
RUN pip3 install pipenv==2020.11.15 \
    && pipenv install --dev --deploy --system

ENV XDG_RUNTIME_DIR=/tmp

# Copy all assets
COPY . ./

# Reconfigure plugin builder tool to deploy to new plugin location
RUN grep -v plugin_path pb_tool.cfg > pb_tool_docker.cfg
RUN cat pb_tool_docker.cfg

# Run type and code style checks
RUN mypy --namespace-packages --explicit-package-bases .
RUN flake8 .

# Run the more simple unit tests
RUN python3 -m unittest discover .

# Deploy plugin to standard plugins dir
RUN pb_tool deploy --config_file pb_tool_docker.cfg --plugin_path /QGIS/build/output/python/plugins --no-confirm
RUN ls /QGIS/build/output/python/plugins
RUN pb_tool deploy --config_file pb_tool_docker.cfg --plugin_path /QGIS/build/output/python/plugins --no-confirm
RUN ls /QGIS/build/output/python/plugins

# Run the integration tests by using the test script
WORKDIR test
ENV PYTHONPATH=$PYTHONPATH:/namari:/QGIS/build/output/python/plugins
RUN xvfb-run qgis_testrunner.sh integration_test
