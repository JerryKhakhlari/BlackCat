"""Seismic attribute extraction for facies characterisation.

Attributes computed per sample include instantaneous amplitude, phase and
frequency, as well as envelope and a simple texture measure (local variance).
These attributes form the feature vectors fed to the classifier.
"""

import numpy as np
from scipy.signal import hilbert


class SeismicAttributeExtractor:
    """Extract a suite of seismic attributes from a 2-D amplitude array.

    Parameters
    ----------
    window : int
        Half-window length (in samples) used when computing windowed statistics
        such as local variance.  The full window is ``2*window + 1`` samples.
    """

    def __init__(self, window: int = 5) -> None:
        if window < 1:
            raise ValueError("window must be >= 1")
        self.window = window

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def extract(self, seismic: np.ndarray) -> np.ndarray:
        """Extract all attributes and stack them into a feature array.

        Parameters
        ----------
        seismic : ndarray of shape ``(n_traces, n_samples)``
            Raw seismic amplitude volume.

        Returns
        -------
        ndarray of shape ``(n_traces, n_samples, n_attributes)``
            Stacked attribute cube.  The attribute order is:
            [amplitude, envelope, inst_phase, inst_frequency, local_variance].
        """
        amplitude = seismic  # amplitude is the raw trace
        envelope = self.instantaneous_amplitude(seismic)
        phase = self.instantaneous_phase(seismic)
        frequency = self.instantaneous_frequency(seismic)
        variance = self.local_variance(seismic)

        attributes = np.stack([amplitude, envelope, phase, frequency, variance], axis=-1)
        return attributes

    # ------------------------------------------------------------------
    # Individual attribute methods
    # ------------------------------------------------------------------

    @staticmethod
    def instantaneous_amplitude(seismic: np.ndarray) -> np.ndarray:
        """Compute instantaneous amplitude (envelope) via the Hilbert transform.

        Parameters
        ----------
        seismic : ndarray of shape ``(n_traces, n_samples)``

        Returns
        -------
        ndarray of shape ``(n_traces, n_samples)``
        """
        analytic = hilbert(seismic, axis=1)
        return np.abs(analytic)

    @staticmethod
    def instantaneous_phase(seismic: np.ndarray) -> np.ndarray:
        """Compute instantaneous phase (radians) via the Hilbert transform.

        Parameters
        ----------
        seismic : ndarray of shape ``(n_traces, n_samples)``

        Returns
        -------
        ndarray of shape ``(n_traces, n_samples)``
        """
        analytic = hilbert(seismic, axis=1)
        return np.angle(analytic)

    @staticmethod
    def instantaneous_frequency(seismic: np.ndarray, sampling_interval: float = 0.002) -> np.ndarray:
        """Compute instantaneous frequency (Hz).

        Derived as the time derivative of the unwrapped instantaneous phase.

        Parameters
        ----------
        seismic : ndarray of shape ``(n_traces, n_samples)``
        sampling_interval : float
            Sampling interval in seconds.

        Returns
        -------
        ndarray of shape ``(n_traces, n_samples)``
        """
        analytic = hilbert(seismic, axis=1)
        phase = np.unwrap(np.angle(analytic), axis=1)
        # Finite-difference derivative of unwrapped phase
        freq = np.gradient(phase, sampling_interval, axis=1) / (2.0 * np.pi)
        return freq

    def local_variance(self, seismic: np.ndarray) -> np.ndarray:
        """Compute the local variance within a sliding window along each trace.

        Uses a vectorized cumulative-sum approach for efficiency.

        Parameters
        ----------
        seismic : ndarray of shape ``(n_traces, n_samples)``

        Returns
        -------
        ndarray of shape ``(n_traces, n_samples)``
        """
        n_traces, n_samples = seismic.shape
        variance = np.zeros_like(seismic)
        w = self.window

        # Cumulative sums for fast windowed mean and mean-of-squares
        cs = np.cumsum(seismic, axis=1)
        cs2 = np.cumsum(seismic ** 2, axis=1)

        # Padded versions so we can do left - right in one broadcast step
        pad = np.zeros((n_traces, 1), dtype=seismic.dtype)
        cs_pad = np.hstack([pad, cs])
        cs2_pad = np.hstack([pad, cs2])

        for j in range(n_samples):
            lo = max(0, j - w)
            hi = min(n_samples, j + w + 1)
            count = hi - lo
            s = cs_pad[:, hi] - cs_pad[:, lo]
            s2 = cs2_pad[:, hi] - cs2_pad[:, lo]
            variance[:, j] = s2 / count - (s / count) ** 2

        return variance

    def attribute_names(self) -> list[str]:
        """Return the ordered list of attribute names produced by :meth:`extract`."""
        return [
            "amplitude",
            "envelope",
            "instantaneous_phase",
            "instantaneous_frequency",
            "local_variance",
        ]
