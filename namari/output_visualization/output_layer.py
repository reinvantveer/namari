from PyQt5.QtCore import QVariant
from numpy import ndarray
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsCoordinateReferenceSystem, QgsField


def create_output_layer(input_layer: QgsVectorLayer, outputs: ndarray) -> QgsVectorLayer:
    """
    Creates an output layer based on the input layer that the anomaly detector was trained on.

    :param input_layer: The QGIS vector layer used as input for the anomaly detection model
    :param outputs:     The anomaly detector classification outputs for the layer

    :return: A QGIS memory/temporary layer containing the anomaly classifications as a map layer to be added to QGIS
    """

    # The displayed layer name
    output_layer_name = input_layer.name() + '_anomalies'

    # The geometry type name for the layer definition
    geom_type_number = int(input_layer.wkbType())
    geom_type_name = QgsWkbTypes.displayString(geom_type_number)

    # EPSG code for output layer
    crs: QgsCoordinateReferenceSystem = input_layer.crs()
    crs_name = crs.authid()

    # The layer definition
    layer_def = f'{geom_type_name}?crs={crs_name}'

    anomaly_output_layer = QgsVectorLayer(layer_def, output_layer_name, 'memory')

    is_anomaly_field = QgsField('is_anomaly', QVariant.Bool)
    anomaly_output_layer.addAttribute(is_anomaly_field)

    return anomaly_output_layer
