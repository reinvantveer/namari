# namari
An experiment in QGIS plugin creation

# Local dev-setup
This repo uses a combination of pipenv (unit testing) and Docker (integration testing) setups in order to develop and test. Use the following to set up an isolated virtual environment for development:
```shell
pipenv install --dev --deploy --site-packages --python=<path/to/your/QGIS/python/version> 
```

In order to obtain the path to your QGIS python interpreter, start QGIS, pres Ctrl-alt-P to start a python interpreter window and enter `import sys; sys.executable`

# Troubleshooting
If you get something like
```
ImportError: /lib/x86_64-linux-gnu/libQt5DBus.so.5: undefined symbol: _ZN14QMetaCallEventC2EttPFvP7QObjectN11QMetaObject4CallEiPPvEPKS0_iiPiS5_P10QSemaphore, version Qt_5_PRIVATE_API
```
your pipenv environment wasn't initialized properly with qgis components. Follow the instructions from the local install setup using pipenv.
