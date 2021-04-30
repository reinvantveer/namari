import unittest

import numpy
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsVectorLayerFeatureCounter

from namari.models.inputs_extraction import inputs_from_layer
from namari.output_visualization.output_layer import create_output_layer, get_anomalous_fids


class TestOutputLayer(unittest.TestCase):
    def setUp(self) -> None:
        self.layer = QgsVectorLayer('test/data/field_test.gpkg', 'field_test', 'ogr')
        inputs, self.fids = inputs_from_layer(self.layer)
        self.anomalies = [1]

    def test_get_anomalous_fids(self) -> None:
        with self.subTest('It produces the feature ids of the anomalies'):
            predictions = numpy.array([-1, 1])
            anomalies = get_anomalous_fids(self.fids, predictions)
            self.assertListEqual(anomalies, [self.fids[0]])

    def test_output_layer_creation(self) -> None:
        with self.subTest('It creates the anomalies layer'):
            layer = create_output_layer(self.layer, self.anomalies)
            geom_type_name = QgsWkbTypes.displayString(layer.wkbType())
            self.assertEqual(geom_type_name, "Polygon")

            with self.subTest(f'With {len(self.anomalies)} features in it'):
                counter: QgsVectorLayerFeatureCounter = layer.countSymbolFeatures()
                if counter is not None:
                    counter.waitForFinished()
                self.assertEqual(layer.featureCount(), len(self.anomalies))
