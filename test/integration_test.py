import pyplugin_installer


def run_all() -> None:
    print('Hello QGIS!')
    plugins = pyplugin_installer.installer_data.plugins.all().keys()
    print(plugins)
    print('OK')
    print('Ran')
