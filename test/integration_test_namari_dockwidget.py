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
from typing import Optional

from PyQt5.QtWidgets import QWidget
from qgis.core import QgsApplication, QgsVectorLayer

QgsApplication.setPrefixPath('/QGIS/build/output', True)


class NamariDockWidgetTest(unittest.TestCase):
    app: QgsApplication = QgsApplication(argv=[], GUIenabled=True)
    dock_widget: Optional[QWidget] = None

    @classmethod
    def setUpClass(cls) -> None:
        print('prefixpath:', QgsApplication.prefixPath())
        cls.app.initQgis()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.app.exitQgis()

    def test_dockwidget_layer_selector(self) -> None:
        assert self.dock_widget is not None
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
            self.app.addMapLayer(layer)

        with self.subTest('Then the build button is enabled'):
            assert self.dock_widget is not None
            enabled = self.dock_widget.pushButtonBuildModel.isEnabled()
            self.assertTrue(enabled)
