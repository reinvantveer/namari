from qgis import utils
from namari import classFactory


def run_all() -> None:
    print('Hello QGIS!')

    plugins = utils.plugins
    plugins['namari'] = classFactory(utils.iface)
    print(plugins)

    print('OK')
    print('Ran')
