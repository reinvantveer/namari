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

import unittest

from PyQt5.QtCore import Qt
from PyQt5.QtTest import QTest
from qgis import utils

from namari import classFactory
from qgis.core import QgsProject, QgsVectorLayer
from qgis.gui import QgisInterface


class NamariDockWidgetTest(unittest.TestCase):
    def setUp(self) -> None:
        self.plugins = utils.plugins
        assert utils.iface is not None, 'This test needs an actual iface interface to QGIS'
        self.iface: QgisInterface = utils.iface

        self.plugins['namari'] = classFactory(utils.iface)
        self.namari = self.plugins['namari']
        self.namari.initGui()
        self.namari.run()

        self.dock_widget = self.namari.dockwidget

    def test_dockwidget_layer_selector(self) -> None:
        self.assertIsNotNone(self.namari)

        with self.subTest('When we start the widget, there is no layer set'):
            self.assertTrue(self.namari.dockwidget.isEnabled())

            layer = self.namari.dockwidget.mMapLayerComboBox.currentLayer()
            self.assertEqual(layer, None)

        with self.subTest('So the "Build model" button is disabled'):
            enabled = self.namari.dockwidget.pushButtonBuildModel.isEnabled()
            self.assertFalse(enabled)

        with self.subTest('But when we load a vector data source'):
            layer = QgsVectorLayer(
                'test/data/amersfoort-centre.gpkg',
                'amersfoort-centre',
                'ogr')
            QgsProject.instance().addMapLayer(layer)

            self.assertEqual(len(layer.fields()), 10)

        with self.subTest('Then the build button is enabled'):
            enabled = self.namari.dockwidget.pushButtonBuildModel.isEnabled()
            self.assertTrue(enabled)

        with self.subTest('We can execute the model building'):
            QTest.mouseClick(
                self.namari.dockwidget.pushButtonBuildModel,
                Qt.LeftButton)


def run_all() -> None:
    suite = unittest.TestLoader().loadTestsFromTestCase(NamariDockWidgetTest)
    assert unittest.TextTestRunner(verbosity=2).run(suite).wasSuccessful()
