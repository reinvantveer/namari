from PyQt5.QtCore import QVariant
from sklearn.feature_extraction import DictVectorizer


def get_inputs_from_layer(layer):
    field_names = [f.name() for f in layer.fields()]
    print(field_names)
    features = layer.getFeatures()
    vectorizer = DictVectorizer()
    feat_dicts = features_to_dicts(features, field_names)
    print(len(feat_dicts), 'features')
    inputs = vectorizer.fit_transform(feat_dicts)
    return inputs


def features_to_dicts(features, field_names):
    feat_dicts = []

    for f_idx, feature in enumerate(features):
        if feature.isValid():
            if QVariant in [type(d) for d in feature]:
                print(f'Skipped feature {f_idx + 1}')
                continue

            feat_dict = {field: feature.attribute(field) for field in field_names}
            feat_dicts.append(feat_dict)

    return feat_dicts
