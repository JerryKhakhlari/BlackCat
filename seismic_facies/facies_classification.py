"""Facies classification using machine-learning models.

This module wraps scikit-learn classifiers to provide a clean interface for
training on labelled seismic attribute data and predicting facies labels on
unseen data.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix


class FaciesClassifier:
    """Train and apply a Random-Forest facies classifier on seismic attributes.

    The classifier normalises feature vectors using :class:`StandardScaler`
    before passing them to a :class:`RandomForestClassifier`.

    Parameters
    ----------
    n_estimators : int
        Number of trees in the random forest.
    max_depth : int or None
        Maximum depth of each tree.  ``None`` means nodes are expanded until
        all leaves contain fewer than *min_samples_split* samples.
    random_state : int or None
        Seed passed to the underlying :class:`RandomForestClassifier`.
    test_size : float
        Fraction of samples to reserve for the hold-out evaluation set.
    """

    def __init__(
        self,
        n_estimators: int = 100,
        max_depth: int | None = None,
        random_state: int | None = 42,
        test_size: float = 0.2,
    ) -> None:
        self.n_estimators = n_estimators
        self.max_depth = max_depth
        self.random_state = random_state
        self.test_size = test_size

        self._scaler = StandardScaler()
        self._clf = RandomForestClassifier(
            n_estimators=self.n_estimators,
            max_depth=self.max_depth,
            random_state=self.random_state,
            n_jobs=-1,
        )
        self._is_fitted = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def fit(self, attributes: np.ndarray, labels: np.ndarray) -> dict:
        """Fit the classifier on seismic attribute data.

        Parameters
        ----------
        attributes : ndarray of shape ``(n_traces, n_samples, n_attrs)``
            Seismic attributes as returned by
            :meth:`SeismicAttributeExtractor.extract`.
        labels : ndarray of shape ``(n_traces, n_samples)``
            Integer facies labels for every sample.

        Returns
        -------
        dict
            Training statistics with keys ``accuracy``, ``report``, and
            ``confusion_matrix``.
        """
        X, y = self._flatten(attributes, labels)

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=y,
        )

        X_train_s = self._scaler.fit_transform(X_train)
        X_test_s = self._scaler.transform(X_test)

        self._clf.fit(X_train_s, y_train)
        self._is_fitted = True

        y_pred = self._clf.predict(X_test_s)
        accuracy = float(np.mean(y_pred == y_test))
        report = classification_report(y_test, y_pred, output_dict=False)
        cm = confusion_matrix(y_test, y_pred)

        return {
            "accuracy": accuracy,
            "report": report,
            "confusion_matrix": cm,
        }

    def predict(self, attributes: np.ndarray) -> np.ndarray:
        """Predict facies labels for a new seismic attribute array.

        Parameters
        ----------
        attributes : ndarray of shape ``(n_traces, n_samples, n_attrs)``

        Returns
        -------
        ndarray of shape ``(n_traces, n_samples)``
            Predicted integer facies labels.
        """
        if not self._is_fitted:
            raise RuntimeError("Classifier has not been fitted yet.  Call fit() first.")

        n_traces, n_samples, _ = attributes.shape
        X = attributes.reshape(-1, attributes.shape[-1])
        X_s = self._scaler.transform(X)
        y_pred = self._clf.predict(X_s)
        return y_pred.reshape(n_traces, n_samples)

    def feature_importances(self) -> np.ndarray:
        """Return the feature importance scores from the trained forest.

        Returns
        -------
        ndarray of shape ``(n_attrs,)``
        """
        if not self._is_fitted:
            raise RuntimeError("Classifier has not been fitted yet.  Call fit() first.")
        return self._clf.feature_importances_

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _flatten(
        attributes: np.ndarray, labels: np.ndarray
    ) -> tuple[np.ndarray, np.ndarray]:
        """Reshape (n_traces, n_samples, n_attrs) → (n_samples_total, n_attrs)."""
        n_traces, n_samples, n_attrs = attributes.shape
        X = attributes.reshape(-1, n_attrs)
        y = labels.reshape(-1)
        return X, y
