from typing import List

from PyQt5.QtCore import QVariant
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

        types = [type(d) for d in feature]
        if NULL in feature.attributes():
            # print('NULL')
            continue

        if QVariant in types:
            q_variant_idxs = [t_idx for t_idx, t in enumerate(types) if t == QVariant]
            null_field_name = field_names[q_variant_idxs[0]]
            print(f'Skipped feature with fid {feature.id()}: '
                  f'field {null_field_name} is {feature.attribute(null_field_name)}')
            assert feature.attribute(null_field_name) == NULL
            continue

        feat_dict = {field: feature.attribute(field) for field in field_names}
        feat_dicts.append(feat_dict)

    return feat_dicts
