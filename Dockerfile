FROM qgis/qgis:release-3_18

RUN apt-get update \
    && apt-get install -y python3-pyqt5.qtsvg

WORKDIR app
COPY Pipfile* ./
RUN pip3 install pipenv==2020.11.15 \
    && pipenv install --dev --deploy --site-packages

COPY . ./
ENV PATH=/QGIS/build/output/lib/qgis:/QGIS/build/output/lib/qgis/plugins:$PATH
RUN echo $PATH
ENV PYTHONPATH=/QGIS/build/output/python:$PYTHONPATH
RUN echo $PYTHONPATH
RUN pipenv run python3 -m unittest discover .
