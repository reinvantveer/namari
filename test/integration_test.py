import unittest

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


def run_all() -> None:
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(NamariDockWidgetTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
