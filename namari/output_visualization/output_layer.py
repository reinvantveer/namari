from typing import List

from numpy import ndarray
from qgis.core import QgsVectorLayer, QgsWkbTypes, QgsCoordinateReferenceSystem, edit


def get_anomalous_fids(fids: List[int], outputs: ndarray):
    output_list = outputs.tolist()
    output_with_ids = [{'fid': f, 'class': o} for (o, f) in zip(output_list, fids)]
    anomalies = [o['fid'] for o in output_with_ids if o['class'] == -1]

    return anomalies


def create_output_layer(input_layer: QgsVectorLayer, anomalies: List[int]) -> QgsVectorLayer:
    """
    Creates an output layer based on the input layer that the anomaly detector was trained on.

    :param input_layer: The QGIS vector layer used as input for the anomaly detection model
    :param anomalies:   The anomalous feature ids of the layer

    :return: A QGIS memory/temporary layer containing the anomaly classifications as a map layer to be added to QGIS
    """

    # The displayed layer name
    output_layer_name = input_layer.name() + '_anomalies'

    # The geometry type name for the layer definition
    geom_type_number = int(input_layer.wkbType())
    geom_type_name = QgsWkbTypes.displayString(geom_type_number)

    # Copy the EPSG code for output layer
    crs: QgsCoordinateReferenceSystem = input_layer.crs()
    crs_name = crs.authid()

    # The layer definition template
    layer_def = f'{geom_type_name}?crs={crs_name}'

    anomalies_layer = QgsVectorLayer(layer_def, output_layer_name, 'memory')

    with edit(anomalies_layer):
        for field in input_layer.fields():
            anomalies_layer.addAttribute(field)

        anomalous_features = input_layer.getFeatures(anomalies)

        for feature in anomalous_features:
            succeeded = anomalies_layer.addFeature(feature)
            assert succeeded, f'Unable to add feature with fid {feature.id()} to layer'

    return anomalies_layer
