FROM qgis/qgis:release-3_18

WORKDIR app
COPY Pipfile* ./
RUN pip3 install pipenv==2020.11.15 \
    && pipenv install --dev --deploy --system

COPY . ./
ENV PATH=/QGIS/build/output/lib/qgis:/QGIS/build/output/lib/qgis/plugins:$PATH
RUN echo $PATH
ENV PYTHONPATH=/QGIS/build/output/python:$PYTHONPATH
RUN echo $PYTHONPATH
RUN xvfb-run python3 -m unittest discover .
