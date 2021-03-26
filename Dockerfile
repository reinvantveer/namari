FROM qgis/qgis:release-3_18

WORKDIR app
COPY Pipfile* ./
RUN pip3 install pipenv==2020.11.15 \
    && pipenv install --dev --deploy --system

ENV XDG_RUNTIME_DIR=/tmp

COPY . ./
RUN xvfb-run python3 -m unittest discover .
RUN mypy --namespace-packages --explicit-package-bases .
RUN flake8 .
