import configparser
import os
import sys

from qgis.PyQt.QtWidgets import QMessageBox


def report_missing_dependency(dependency_name: str) -> None:
    """
    Reports that one of the dependencies for the project could not be loaded.

    :return: None
    """
    python_location = sys.executable
    dir_path = os.path.dirname(os.path.realpath(__file__))
    config = configparser.ConfigParser()
    config.read(os.path.join(dir_path, '..', 'metadata.txt'))
    dependencies = config['general']['plugin_dependencies']

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(f'Unable to load {dependency_name}')
    message = 'You can install with:\n\n' + \
              '{}'.format(python_location) + \
              ' -m pip install {}\n\n'.format(dependencies) + \
              'You can copy-paste this command into a console, and then restart QGIS.'

    msg.setInformativeText(message)
    msg.setWindowTitle("Error")
    msg.exec_()
