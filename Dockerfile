FROM qgis/qgis:release-3_18

WORKDIR app
COPY Pipfile* ./
RUN pip3 install pipenv==2020.11.15 \
    && pipenv install --dev --deploy --system

ENV XDG_RUNTIME_DIR=/tmp

COPY . ./
RUN sed -i 's|/home/rein/.local/share/QGIS/QGIS3/profiles/default|/QGIS/build/output|' pb_tool.cfg
RUN pb_tool deploy -y
RUN mypy --namespace-packages --explicit-package-bases .
RUN flake8 .

RUN xvfb-run python3 -m unittest discover .
