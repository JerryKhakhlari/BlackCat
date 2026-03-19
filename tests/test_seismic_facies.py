"""Tests for the seismic facies characterisation package."""

import numpy as np
import pytest

from seismic_facies.data_generation import SeismicDataGenerator
from seismic_facies.feature_extraction import SeismicAttributeExtractor
from seismic_facies.facies_classification import FaciesClassifier
from seismic_facies.visualization import SeismicVisualizer


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

N_TRACES = 20
N_SAMPLES = 80
N_FACIES = 3


@pytest.fixture(scope="module")
def generated_data():
    gen = SeismicDataGenerator(
        n_traces=N_TRACES,
        n_samples=N_SAMPLES,
        n_facies=N_FACIES,
        random_state=0,
    )
    return gen.generate()


@pytest.fixture(scope="module")
def attributes(generated_data):
    extractor = SeismicAttributeExtractor(window=3)
    return extractor.extract(generated_data["seismic"])


# ---------------------------------------------------------------------------
# SeismicDataGenerator tests
# ---------------------------------------------------------------------------


class TestSeismicDataGenerator:
    def test_output_shapes(self, generated_data):
        assert generated_data["seismic"].shape == (N_TRACES, N_SAMPLES)
        assert generated_data["facies"].shape == (N_TRACES, N_SAMPLES)
        assert generated_data["impedance"].shape == (N_TRACES, N_SAMPLES)

    def test_facies_labels_in_range(self, generated_data):
        labels = generated_data["facies"]
        assert labels.min() >= 0
        assert labels.max() < N_FACIES

    def test_wavelet_is_1d(self, generated_data):
        assert generated_data["wavelet"].ndim == 1

    def test_seismic_has_non_zero_values(self, generated_data):
        assert np.any(generated_data["seismic"] != 0)

    def test_reproducibility(self):
        gen1 = SeismicDataGenerator(n_traces=5, n_samples=20, n_facies=2, random_state=7)
        gen2 = SeismicDataGenerator(n_traces=5, n_samples=20, n_facies=2, random_state=7)
        d1 = gen1.generate()
        d2 = gen2.generate()
        np.testing.assert_array_equal(d1["seismic"], d2["seismic"])
        np.testing.assert_array_equal(d1["facies"], d2["facies"])

    def test_different_seeds_give_different_data(self):
        gen1 = SeismicDataGenerator(n_traces=5, n_samples=20, n_facies=2, random_state=1)
        gen2 = SeismicDataGenerator(n_traces=5, n_samples=20, n_facies=2, random_state=2)
        d1 = gen1.generate()
        d2 = gen2.generate()
        assert not np.array_equal(d1["facies"], d2["facies"])


# ---------------------------------------------------------------------------
# SeismicAttributeExtractor tests
# ---------------------------------------------------------------------------


class TestSeismicAttributeExtractor:
    def test_output_shape(self, generated_data):
        extractor = SeismicAttributeExtractor(window=3)
        attrs = extractor.extract(generated_data["seismic"])
        # 5 attributes
        assert attrs.shape == (N_TRACES, N_SAMPLES, 5)

    def test_attribute_names_count(self):
        extractor = SeismicAttributeExtractor()
        assert len(extractor.attribute_names()) == 5

    def test_envelope_non_negative(self, attributes):
        envelope = attributes[:, :, 1]  # index 1 = envelope
        assert np.all(envelope >= 0)

    def test_phase_in_range(self, attributes):
        phase = attributes[:, :, 2]  # index 2 = instantaneous_phase
        assert phase.min() >= -np.pi - 1e-10
        assert phase.max() <= np.pi + 1e-10

    def test_invalid_window_raises(self):
        with pytest.raises(ValueError):
            SeismicAttributeExtractor(window=0)

    def test_instantaneous_amplitude_static(self):
        seismic = np.ones((3, 10))
        env = SeismicAttributeExtractor.instantaneous_amplitude(seismic)
        assert env.shape == (3, 10)
        assert np.all(env >= 0)


# ---------------------------------------------------------------------------
# FaciesClassifier tests
# ---------------------------------------------------------------------------


class TestFaciesClassifier:
    def test_fit_returns_accuracy(self, attributes, generated_data):
        clf = FaciesClassifier(n_estimators=10, random_state=0)
        stats = clf.fit(attributes, generated_data["facies"])
        assert "accuracy" in stats
        assert 0.0 <= stats["accuracy"] <= 1.0

    def test_predict_shape(self, attributes, generated_data):
        clf = FaciesClassifier(n_estimators=10, random_state=0)
        clf.fit(attributes, generated_data["facies"])
        pred = clf.predict(attributes)
        assert pred.shape == (N_TRACES, N_SAMPLES)

    def test_predict_labels_in_range(self, attributes, generated_data):
        clf = FaciesClassifier(n_estimators=10, random_state=0)
        clf.fit(attributes, generated_data["facies"])
        pred = clf.predict(attributes)
        assert pred.min() >= 0
        assert pred.max() < N_FACIES

    def test_predict_before_fit_raises(self, attributes):
        clf = FaciesClassifier()
        with pytest.raises(RuntimeError):
            clf.predict(attributes)

    def test_feature_importances_shape(self, attributes, generated_data):
        clf = FaciesClassifier(n_estimators=10, random_state=0)
        clf.fit(attributes, generated_data["facies"])
        imp = clf.feature_importances()
        assert imp.shape == (5,)
        assert np.isclose(imp.sum(), 1.0, atol=1e-6)

    def test_feature_importances_before_fit_raises(self):
        clf = FaciesClassifier()
        with pytest.raises(RuntimeError):
            clf.feature_importances()

    def test_confusion_matrix_shape(self, attributes, generated_data):
        clf = FaciesClassifier(n_estimators=10, random_state=0)
        stats = clf.fit(attributes, generated_data["facies"])
        cm = stats["confusion_matrix"]
        assert cm.shape == (N_FACIES, N_FACIES)


# ---------------------------------------------------------------------------
# SeismicVisualizer tests
# ---------------------------------------------------------------------------


class TestSeismicVisualizer:
    """Smoke tests – just verify that figures are created without errors."""

    @pytest.fixture(autouse=True)
    def close_figs(self):
        import matplotlib.pyplot as plt
        yield
        plt.close("all")

    def test_plot_seismic_section(self, generated_data):
        viz = SeismicVisualizer()
        fig = viz.plot_seismic_section(generated_data["seismic"])
        assert fig is not None

    def test_plot_facies_section(self, generated_data):
        viz = SeismicVisualizer()
        fig = viz.plot_facies_section(generated_data["facies"], n_facies=N_FACIES)
        assert fig is not None

    def test_plot_side_by_side(self, generated_data):
        viz = SeismicVisualizer()
        fig = viz.plot_side_by_side(
            generated_data["seismic"],
            generated_data["facies"],
            generated_data["facies"],
            n_facies=N_FACIES,
        )
        assert fig is not None

    def test_plot_confusion_matrix(self):
        cm = np.array([[10, 2, 0], [1, 12, 1], [0, 3, 9]])
        viz = SeismicVisualizer()
        fig = viz.plot_confusion_matrix(cm, n_facies=3)
        assert fig is not None

    def test_plot_feature_importances(self):
        importances = np.array([0.3, 0.25, 0.2, 0.15, 0.1])
        viz = SeismicVisualizer()
        fig = viz.plot_feature_importances(importances, ["a", "b", "c", "d", "e"])
        assert fig is not None
