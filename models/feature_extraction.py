from typing import List

from qgis.PyQt.QtCore import NULL
from qgis.core import QgsFeature, QgsVectorLayer
from sklearn.feature_extraction import DictVectorizer


def get_inputs_from_layer(layer: QgsVectorLayer):
    vectorizer = DictVectorizer()
    feat_dicts = features_to_dicts(layer)

    print(len(feat_dicts), 'features')

    inputs = vectorizer.fit_transform(feat_dicts)
    return inputs


def features_to_dicts(layer: QgsVectorLayer):
    features: List[QgsFeature] = layer.getFeatures()
    field_names = [f.name() for f in layer.fields()]
    field_types = [f.typeName() for f in layer.fields()]
    print(list(zip(field_names, field_types)))

    feat_dicts: List[dict] = []

    for f_idx, feature in enumerate(features):
        if not feature.isValid():
            continue

        add_feature = True
        feat_dict = {field: feature.attribute(field) for field in field_names}

        for key, val in feat_dict.items():
            if val == NULL:
                if layer.fields().field(key).typeName() == 'String':
                    feat_dict[key] = ""
                else:
                    print(f'Skipped feature with fid {feature.id()}: '
                          f'field {field_names[key]} is {feature.attribute(key)}')
                    add_feature = False

        if add_feature:
            feat_dicts.append(feat_dict)

    return feat_dicts
