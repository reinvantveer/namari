FROM qgis/qgis:release-3_18

WORKDIR app
COPY Pipfile* ./
RUN pip3 install pipenv==2020.11.15 \
    && pipenv install --dev --deploy --system

COPY . ./
RUN xvfb-run python3 -m unittest discover .
