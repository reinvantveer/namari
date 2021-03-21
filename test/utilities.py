# coding=utf-8
"""Common functionality used by regression tests."""

import sys
import logging


LOGGER = logging.getLogger('QGIS')
QGIS_APP = None  # Static variable used to hold hand to running QGIS app
CANVAS = None
PARENT = None
IFACE = None


def get_qgis_app():
    """ Start one QGIS application to test against.

    :returns: Handle to QGIS app, canvas, iface and parent. If there are any
        errors the tuple members will be returned as None.
    :rtype: (QgsApplication, CANVAS, IFACE, PARENT)

    If QGIS is already running the handle to that app will be returned.
    """

    from qgis.PyQt import QtGui, QtCore
    from qgis.core import QgsApplication
    from qgis.gui import QgsMapCanvas

    global QGIS_APP  # pylint: disable=W0603

    if QGIS_APP is None:
        QGIS_APP = QgsApplication(argv=[], GUIenabled=True)
        # Make sure QGIS_PREFIX_PATH is set in your env if needed!
        QGIS_APP.initQgis()
        s = QGIS_APP.showSettings()
        LOGGER.debug(s)

    global CANVAS  # pylint: disable=W0603
    if CANVAS is None:
        # noinspection PyPep8Naming
        CANVAS = QgsMapCanvas(PARENT)
        CANVAS.resize(QtCore.QSize(400, 400))

    return QGIS_APP, CANVAS, IFACE, PARENT
