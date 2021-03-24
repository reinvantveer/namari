# coding=utf-8
"""Resources test.

.. note:: This program is free software; you can redistribute it and/or modify
     it under the terms of the GNU General Public License as published by
     the Free Software Foundation; either version 2 of the License, or
     (at your option) any later version.

"""

__author__ = 'rein@vantveer.me'
__date__ = '2021-02-19'
__copyright__ = 'Copyright 2021, Rein van \'t Veer'

import unittest

from qgis.PyQt.QtGui import QIcon


class NamariDialogTest(unittest.TestCase):
    """Test resources work."""

    def test_icon_png(self):
        """Test we can click OK."""
        path = ':/plugins/Namari/icon.png'
        icon = QIcon(path)
        self.assertFalse(icon.isNull())
