"""Synthetic seismic data generation for facies characterisation experiments."""

import numpy as np


class SeismicDataGenerator:
    """Generate synthetic post-stack seismic data with labelled facies.

    The generator convolves a Ricker wavelet with a reflectivity series that is
    constructed from a simple layered-earth model.  Each layer is assigned a
    geological *facies* label so that the resulting amplitude volume can be used
    to train and evaluate facies classifiers.

    Parameters
    ----------
    n_traces : int
        Number of seismic traces (inline × crossline positions) to generate.
    n_samples : int
        Number of time/depth samples per trace.
    n_facies : int
        Number of distinct geological facies to simulate.
    dominant_frequency : float
        Dominant frequency (Hz) of the Ricker wavelet used for convolution.
    sampling_interval : float
        Sampling interval in seconds (e.g. 0.002 for 2 ms).
    random_state : int or None
        Seed for the NumPy random number generator.  Use a fixed value for
        reproducible results.
    """

    def __init__(
        self,
        n_traces: int = 100,
        n_samples: int = 200,
        n_facies: int = 4,
        dominant_frequency: float = 30.0,
        sampling_interval: float = 0.002,
        random_state: int | None = 42,
    ) -> None:
        self.n_traces = n_traces
        self.n_samples = n_samples
        self.n_facies = n_facies
        self.dominant_frequency = dominant_frequency
        self.sampling_interval = sampling_interval
        self.rng = np.random.default_rng(random_state)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self) -> dict:
        """Generate synthetic seismic traces together with facies labels.

        Returns
        -------
        dict with keys:
            ``seismic``   – ndarray of shape ``(n_traces, n_samples)``
            ``facies``    – ndarray of shape ``(n_traces, n_samples)`` (int labels)
            ``impedance`` – ndarray of shape ``(n_traces, n_samples)``
            ``wavelet``   – 1-D ndarray containing the Ricker wavelet
        """
        wavelet = self._make_wavelet()
        impedance, facies = self._make_impedance_model()
        seismic = self._convolve(impedance, wavelet)

        return {
            "seismic": seismic,
            "facies": facies,
            "impedance": impedance,
            "wavelet": wavelet,
        }

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _make_wavelet(self) -> np.ndarray:
        """Return a zero-phase Ricker wavelet with *dominant_frequency*."""
        a = 1.0 / (np.sqrt(2.0 * np.pi) * self.dominant_frequency * self.sampling_interval)
        n_points = int(2 * np.ceil(2.2 * a) + 1)  # symmetric, odd length
        n_points = max(n_points, 3)
        # Analytic Ricker wavelet: (1 - 2*(π*f*t)²) * exp(-(π*f*t)²)
        t = np.arange(n_points) - (n_points - 1) / 2.0
        pft = np.pi * self.dominant_frequency * t * self.sampling_interval
        return (1.0 - 2.0 * pft ** 2) * np.exp(-(pft ** 2))

    def _make_impedance_model(self) -> tuple[np.ndarray, np.ndarray]:
        """Build a layered impedance model and associated facies labels.

        Layers have randomised thickness.  The acoustic impedance of each layer
        is drawn from a facies-specific Gaussian distribution so that different
        facies have distinguishable amplitude signatures.
        """
        # Base impedance value (kg/m² s × 10⁶) for each facies
        base_impedances = np.linspace(4.0, 8.0, self.n_facies)
        impedance_noise_std = 0.2

        impedance = np.zeros((self.n_traces, self.n_samples))
        facies = np.zeros((self.n_traces, self.n_samples), dtype=int)

        for trace_idx in range(self.n_traces):
            sample = 0
            while sample < self.n_samples:
                # Random facies label for this layer
                f = int(self.rng.integers(0, self.n_facies))
                # Random layer thickness (in samples): 5–40 samples
                thickness = int(self.rng.integers(5, 41))
                end = min(sample + thickness, self.n_samples)

                # Impedance value with small random perturbation per trace
                imp_val = base_impedances[f] + self.rng.normal(0, impedance_noise_std)
                impedance[trace_idx, sample:end] = imp_val
                facies[trace_idx, sample:end] = f
                sample = end

        return impedance, facies

    def _convolve(self, impedance: np.ndarray, wavelet: np.ndarray) -> np.ndarray:
        """Convert impedance to seismic amplitude via wavelet convolution.

        Reflectivity is computed from the impedance contrast between adjacent
        samples, then convolved with the Ricker wavelet.
        """
        seismic = np.zeros_like(impedance)
        for i in range(self.n_traces):
            # Reflection coefficient series (same length as impedance trace)
            rc = np.zeros(self.n_samples)
            imp = impedance[i]
            denom = imp[:-1] + imp[1:]
            # Avoid division by zero
            valid = denom != 0
            rc[1:][valid] = (imp[1:][valid] - imp[:-1][valid]) / denom[valid]

            # Convolve with wavelet; trim/pad to ensure output has exactly n_samples
            conv = np.convolve(rc, wavelet, mode="full")
            half = (len(wavelet) - 1) // 2
            trimmed = conv[half: half + self.n_samples]
            # If trimmed is shorter than n_samples (edge case), zero-pad on the right
            if len(trimmed) < self.n_samples:
                trimmed = np.pad(trimmed, (0, self.n_samples - len(trimmed)))
            seismic[i] = trimmed

        return seismic
