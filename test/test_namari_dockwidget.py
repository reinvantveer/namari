# coding=utf-8
"""DockWidget test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'rein@vantveer.me'
__date__ = '2021-02-19'
__copyright__ = 'Copyright 2021, Rein van \'t Veer'

import sys
import unittest

from PyQt5.QtWidgets import QApplication

from namari_dockwidget import NamariDockWidget
from test.utilities import get_qgis_app

QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()
app = QApplication(sys.argv)


class NamariDockWidgetTest(unittest.TestCase):
    """Test dockwidget works."""

    def setUp(self):
        """Runs before each test."""
        self.dockwidget = NamariDockWidget()

    def tearDown(self):
        """Runs after each test."""
        self.dockwidget = None

    def test_present_QGIS_app(self):
        self.assertIsNotNone(QGIS_APP)
        self.assertIsNotNone(CANVAS)
        # self.assertIsNotNone(IFACE)
        # self.assertIsNotNone(PARENT)

    def test_dockwidget_layer_selector(self):
        with self.subTest('When we start the widget, there is no layer set'):
            layer = self.dockwidget.mMapLayerComboBox.currentLayer()
            self.assertEqual(layer, None)

        with self.subTest('So the "Build model" button is disabled'):
            enabled = self.dockwidget.pushButtonBuildModel.isEnabled()
            self.assertFalse(enabled)
