from typing import Tuple

from scipy.sparse import csr_matrix
from sklearn.ensemble import IsolationForest


def train_predict(inputs: csr_matrix,
                  n_estimators: int = 100,  # Use scikit-learn default
                  ) -> Tuple[IsolationForest, csr_matrix]:
    """
    Builds the anomaly detector model based on the inputs passed from the invocation. Returns the outlier predictions
    as well.

    :param inputs:          A csr_matrix, preferably produced by the inputs_extraction.get_inputs_from_layer function.
                            That function will automatically produce a csr_matrix from a QGIS vector layer.
    :param n_estimators:    The number of base estimators in the ensemble

    :return: None
    """

    classifier = IsolationForest(
        n_estimators=n_estimators,
        max_samples="auto",
        contamination="auto",
        max_features=1.,
        bootstrap=False,
        n_jobs=-1,  # Use all available CPUs
        verbose=1,  # show completions in parallel job
    )

    outputs = classifier.fit_predict(inputs)
    print('Training succeeded')

    return classifier, outputs
