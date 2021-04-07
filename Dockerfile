FROM qgis/qgis:release-3_18

WORKDIR namari
COPY Pipfile* ./
RUN pip3 install pipenv==2020.11.15 \
    && pipenv install --dev --deploy --system

ENV XDG_RUNTIME_DIR=/tmp

COPY . ./
RUN sed -i 's|/home/rein/.local/share/QGIS/QGIS3/profiles/default|/QGIS/build/output|' pb_tool.cfg
RUN pb_tool deploy -y
RUN mypy --namespace-packages --explicit-package-bases .
RUN flake8 .

# Run the more simple unit tests
RUN python3 -m unittest discover .

# Run the integration tests by using the test script
WORKDIR test
ENV PYTHONPATH=$PYTHONPATH:/namari
RUN xvfb-run qgis_testrunner.sh integration_test
