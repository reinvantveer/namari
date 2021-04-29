import unittest

from qgis.core import QgsVectorLayer

from namari.models.anomaly_model import train_predict
from namari.models.inputs_extraction import inputs_from_layer


class TestAnomalyModel(unittest.TestCase):
    def setUp(self) -> None:
        self.layer = QgsVectorLayer('test/data/field_test.gpkg', 'field_test', 'ogr')

    def test_train_predict(self) -> None:
        inputs, fids = inputs_from_layer(self.layer)
        model, outputs = train_predict(inputs)
        self.assertEqual(outputs.shape, (2,))
