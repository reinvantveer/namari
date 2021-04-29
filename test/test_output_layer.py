import unittest

from qgis.core import QgsVectorLayer, QgsWkbTypes

from namari.models.anomaly_model import train_predict
from namari.models.inputs_extraction import inputs_from_layer
from namari.output_visualization.output_layer import create_output_layer


class TestOutputLayer(unittest.TestCase):
    def setUp(self) -> None:
        self.layer = QgsVectorLayer('test/data/field_test.gpkg', 'field_test', 'ogr')
        inputs = inputs_from_layer(self.layer)
        self.model, self.outputs = train_predict(inputs)

    def test_output_layer_creation(self):
        layer = create_output_layer(self.layer, self.outputs)
        geom_type_name = QgsWkbTypes.displayString(layer.wkbType())
        self.assertEqual(geom_type_name, "Polygon")
