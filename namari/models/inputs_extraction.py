from typing import List, Optional, Union, Dict, Tuple

from qgis.PyQt.QtCore import NULL, QDate, QDateTime
from qgis.core import QgsVectorLayer, QgsFeature
from scipy.sparse import csr_matrix
# First, try to load the machine learning dependency
from sklearn.feature_extraction import DictVectorizer


def inputs_from_layer(layer: QgsVectorLayer) -> Tuple[csr_matrix, List[int]]:
    """
    Converts all features from a vector layer to a SciPy sparse matrix.

    :param layer: a QGIS vector layer

    :return: a SciPy sparse matrix
    """

    vectorizer = DictVectorizer()
    feat_dicts, fids = features_to_dicts(layer)
    inputs = vectorizer.fit_transform(feat_dicts)

    return inputs, fids


def features_to_dicts(layer: QgsVectorLayer) -> Tuple[List[dict], List[int]]:
    """
    Converts features from a QGIS layer to data dictionaries that can be interpreted by the DictVectorizer of
    scikit-learn.

    :param layer: A QGIS vector layer

    :return: a list of dictionaries containing the data for the layer
    """

    features: List[QgsFeature] = layer.getFeatures()
    field_names = [f.name() for f in layer.fields()]
    field_types = [f.typeName() for f in layer.fields()]
    print(list(zip(field_names, field_types)))

    feat_dicts: List[dict] = []
    fids: List[int] = []

    for feature in features:
        result_tuple = feature_to_dict(feature, field_names)

        if result_tuple is not None:
            feat_dict, fid = result_tuple  # Unpack the tuple
            feat_dicts.append(feat_dict)
            fids.append(fid)

    return feat_dicts, fids


def feature_to_dict(feature: QgsFeature, field_names: List[str]) -> Optional[Tuple[dict, int]]:
    if not feature.isValid():
        print(f'Skipped invalid feature with fid {feature.id()}')
        return None

    feat_dict = {}

    for field_name in field_names:
        value = feature.attribute(field_name)
        data_type_name = feature.fields().field(field_name).typeName()

        # Skip feature ids, they are guaranteed not to be a distinguishing attribute
        # Skip binary data: there's no telling how to treat the data within
        if field_name == 'fid' or data_type_name == 'Binary':
            continue

        feat_dict[field_name] = value

        # Map absent values
        if value == NULL:
            null_value = map_null_value(data_type_name)

            if null_value is None:
                return None

            feat_dict[field_name] = null_value

        # Map date values to unixy seconds since 1970-01-01T00:00:00.000
        elif type(value) == QDate:
            feat_dict[field_name] = QDateTime(value).toSecsSinceEpoch()
        elif type(value) == QDateTime:
            feat_dict[field_name] = value.toSecsSinceEpoch()

    return feat_dict, feature.id()


def map_null_value(data_type_name) -> Optional[Union[str, int, float]]:
    mapping: Dict[str, Union[str, int, float]] = {
        'String': "",
        'Integer': 0,
        'Integer64': 0,
        'Float': 0.,
        'Real': 0.,
        'Date': 0.,
        'DateTime': 0.,
        'Boolean': -1  # Since boolean values are commonly mapped to either 1 or 0, we choose a distinguishing value
    }

    if data_type_name in mapping.keys():
        return mapping[data_type_name]

    return None
