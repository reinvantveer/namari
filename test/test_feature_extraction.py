import unittest

from qgis.core import QgsVectorLayer

from models.feature_extraction import features_to_dicts


class TestFeatureExtraction(unittest.TestCase):
    def setUp(self) -> None:
        self.layer = QgsVectorLayer(
            'test/data/field_test.gpkg',
            'field_test',
            'ogr'
        )

    def test_remap_null_values(self) -> None:
        with self.subTest('When we convert the features to dictionaries of cleaned values'):
            inputs = features_to_dicts(self.layer)
            nulls = inputs[0]

            with self.subTest('then we get some inputs returned'):
                self.assertGreater(len(inputs), 0)

            expected_values = {
                'text_field': '',
                'integer32_field': 0,
                'integer64_field': 0,
                'decimal_field': 0.,
                'date_field': 0,
                'datetime_field': 0,
                'boolean_field': 1
            }

            for key, value in expected_values.items():
                with self.subTest(f'And the empty values in {key }from the test data are converted to zeros'):
                    self.assertEqual(nulls[key], value)

            with self.subTest('And the binary blob is omitted from the dictionary'):
                fields = field_names = [f.name() for f in self.layer.fields()]
                self.assertIn('binary_field', fields)
                self.assertNotIn('binary_field', nulls.keys())

            with self.subTest('And the fid is omitted from the dictionary'):
                fields = field_names = [f.name() for f in self.layer.fields()]
                self.assertIn('fid', fields)
                self.assertNotIn('fid', nulls.keys())

