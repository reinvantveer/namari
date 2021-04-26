# Namari anomaly detector for QGIS

A data quality assessment plugin tool for QGIS. Fully automated anomaly or outlier detection over all properties of your
data.

# Data type support
Currently supports basically any QGIS data type, but some data is ignored:

| Type | Mapping |
|---|---|
| Feature Id | Ignored |
| Text | One-hot |
| Int32 | Float |
| Int64 | Float |
| Decimal | Float |
| Date | Seconds since 1970 |
| DateTime | Seconds since 1970 |
| Boolean | 0. or 1. |
| Binary | Ignored |

Note that each unique text value is assigned to its own attribute. This is because one-hot vectors are the conventional
method for dealing with class-like data. If the text in your data is unique for each record, you'd better keep it out of
the model builder, otherwise the expansion of the data will probably not result in a good data mapping. 

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
