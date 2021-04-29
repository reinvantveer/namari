# coding=utf-8
"""Tests QGIS plugin init."""

import unittest
import logging
import configparser

LOGGER = logging.getLogger('QGIS')


class TestInit(unittest.TestCase):
    """Test that the plugin init is usable for QGIS.

    Based heavily on the validator class by Alessandro
    Passoti available here:

    http://github.com/qgis/qgis-django/blob/master/qgis-app/
             plugins/validator.py

    """

    def test_read_init(self):
        """Test that the plugin __init__ will validate on plugins.qgis.org."""

        # You should update this list according to the latest in
        # https://github.com/qgis/qgis-django/blob/master/qgis-app/
        #        plugins/validator.py

        required_metadata = [
            'name',
            'description',
            'version',
            'qgisMinimumVersion',
            'email',
            'author']

        file_path = 'namari/metadata.txt'
        config = configparser.ConfigParser()
        config.read(file_path)
        self.assertTrue(config.has_section('general'), f'Cannot find a section named "general" in {file_path}')

        for expectation in required_metadata:
            with self.subTest(f'It finds metadata "{expectation}" in metadata source ({file_path}).'):
                self.assertIn(expectation, config['general'])
