from typing import List

from PyQt5.QtCore import QByteArray, QDate, QDateTime
from qgis.PyQt.QtCore import NULL
from qgis.core import QgsFeature, QgsVectorLayer
from scipy.sparse import csr_matrix
from sklearn.feature_extraction import DictVectorizer


def get_inputs_from_layer(layer: QgsVectorLayer) -> csr_matrix:
    vectorizer = DictVectorizer()
    feat_dicts = features_to_dicts(layer)

    print(len(feat_dicts), 'features')

    inputs = vectorizer.fit_transform(feat_dicts)
    return inputs


def features_to_dicts(layer: QgsVectorLayer) -> List[dict]:
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

    for f_idx, feature in enumerate(features):
        if not feature.isValid():
            print(f'Skipped invalid feature with fid {feature.id()}')
            continue

        add_feature = True
        feat_dict = {}

        for field_name in field_names:
            # Skip feature ids, they are guaranteed not to be a distinguishing attribute
            value = feature.attribute(field_name)
            if field_name == 'fid':
                continue
            # Skip binary data: there's no telling how to treat the data within
            elif type(value) == QByteArray:
                continue

            feat_dict[field_name] = value

            # Map absent values
            if value == NULL:
                data_type_name = layer.fields().field(field_name).typeName()

                if data_type_name == 'String':
                    feat_dict[field_name] = ""
                elif data_type_name.startswith('Integer'):
                    feat_dict[field_name] = 0
                elif data_type_name.startswith('Float'):
                    feat_dict[field_name] = 0.
                elif data_type_name.startswith('Real'):
                    feat_dict[field_name] = 0.
                elif data_type_name.startswith('Date'):
                    feat_dict[field_name] = 0
                elif data_type_name.startswith('Boolean'):
                    # Since boolean values are commonly mapped to either 0 or -1, we choose a distinguishing value
                    feat_dict[field_name] = 1
                else:
                    print(f'Skipped feature with fid {feature.id()}: '
                          f'field {field_name} is {feature.attribute(field_name)}')
                    add_feature = False
                    break

            # Map date values to unixy seconds since 1970-01-01T00:00:00.000
            if type(value) == QDate:
                feat_dict[field_name] = QDateTime(value).toSecsSinceEpoch()
            elif type(value) == QDateTime:
                feat_dict[field_name] = value.toSecsSinceEpoch()

        if add_feature:
            feat_dicts.append(feat_dict)

    return feat_dicts
