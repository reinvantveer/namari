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

from qgis.core import QgsApplication, QgsVectorLayer

from namari_dockwidget import NamariDockWidget

app = QgsApplication(argv=[], GUIenabled=True)
app.initQgis()


class NamariDockWidgetTest(unittest.TestCase):
    def setUp(self) -> None:
        """Runs before each test."""
        self.dock_widget = NamariDockWidget()

    def test_dockwidget_layer_selector(self) -> None:
        with self.subTest('When we start the widget, there is no layer set'):
            self.assertTrue(self.dock_widget.isEnabled())

            layer = self.dock_widget.mMapLayerComboBox.currentLayer()
            self.assertEqual(layer, None)

        with self.subTest('So the "Build model" button is disabled'):
            enabled = self.dock_widget.pushButtonBuildModel.isEnabled()
            self.assertFalse(enabled)

        with self.subTest('But when we load a vector data source'):
            layer = QgsVectorLayer(
                path='test/data/amersfoort-centre.gpkg',
                baseName='amersfoort-centre',
                providerLib='ogr')

            self.assertEqual(len(layer.fields()), 10)

            # Load the vector layer
            self.dock_widget.iface.addMapLayer(layer)

        with self.subTest('Then the build button is enabled'):
            enabled = self.dock_widget.pushButtonBuildModel.isEnabled()
            self.assertTrue(enabled)
