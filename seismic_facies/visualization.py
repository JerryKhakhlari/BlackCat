"""Visualization utilities for seismic facies characterisation results.

All plotting is done with *matplotlib*.  Functions return the
:class:`matplotlib.figure.Figure` object so callers can either display it
interactively or save it to disk.
"""

from __future__ import annotations

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.figure import Figure


# Use a non-interactive backend by default so the module can be imported in
# headless environments (CI, servers) without raising a display error.
matplotlib.use("Agg")


class SeismicVisualizer:
    """Collection of plotting helpers for seismic facies analysis.

    Parameters
    ----------
    cmap_seismic : str
        Matplotlib colormap name for seismic amplitude displays.
    cmap_facies : str
        Matplotlib colormap name for facies label displays.
    figsize : tuple[float, float]
        Default figure size ``(width, height)`` in inches.
    """

    def __init__(
        self,
        cmap_seismic: str = "seismic",
        cmap_facies: str = "tab10",
        figsize: tuple[float, float] = (14, 6),
    ) -> None:
        self.cmap_seismic = cmap_seismic
        self.cmap_facies = cmap_facies
        self.figsize = figsize

    # ------------------------------------------------------------------
    # Public methods
    # ------------------------------------------------------------------

    def plot_seismic_section(
        self,
        seismic: np.ndarray,
        title: str = "Seismic Section",
        xlabel: str = "Trace",
        ylabel: str = "Sample",
    ) -> Figure:
        """Plot a 2-D seismic amplitude section as an image.

        Parameters
        ----------
        seismic : ndarray of shape ``(n_traces, n_samples)``
        title, xlabel, ylabel : str
            Axis labels and plot title.

        Returns
        -------
        matplotlib.figure.Figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        vmax = np.percentile(np.abs(seismic), 99)
        ax.imshow(
            seismic.T,
            aspect="auto",
            cmap=self.cmap_seismic,
            vmin=-vmax,
            vmax=vmax,
            interpolation="nearest",
        )
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.tight_layout()
        return fig

    def plot_facies_section(
        self,
        facies: np.ndarray,
        n_facies: int,
        title: str = "Facies Section",
        xlabel: str = "Trace",
        ylabel: str = "Sample",
    ) -> Figure:
        """Plot a 2-D facies label section with a discrete colourmap.

        Parameters
        ----------
        facies : ndarray of shape ``(n_traces, n_samples)``
            Integer facies labels.
        n_facies : int
            Total number of distinct facies.

        Returns
        -------
        matplotlib.figure.Figure
        """
        cmap = plt.get_cmap(self.cmap_facies, n_facies)
        fig, ax = plt.subplots(figsize=self.figsize)
        im = ax.imshow(
            facies.T,
            aspect="auto",
            cmap=cmap,
            vmin=-0.5,
            vmax=n_facies - 0.5,
            interpolation="nearest",
        )
        cbar = fig.colorbar(im, ax=ax, ticks=range(n_facies))
        cbar.set_label("Facies")
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.tight_layout()
        return fig

    def plot_side_by_side(
        self,
        seismic: np.ndarray,
        true_facies: np.ndarray,
        pred_facies: np.ndarray,
        n_facies: int,
    ) -> Figure:
        """Show the seismic section, true facies, and predicted facies side by side.

        Parameters
        ----------
        seismic : ndarray of shape ``(n_traces, n_samples)``
        true_facies : ndarray of shape ``(n_traces, n_samples)``
        pred_facies : ndarray of shape ``(n_traces, n_samples)``
        n_facies : int

        Returns
        -------
        matplotlib.figure.Figure
        """
        cmap_f = plt.get_cmap(self.cmap_facies, n_facies)
        vmax = np.percentile(np.abs(seismic), 99)

        fig, axes = plt.subplots(1, 3, figsize=(self.figsize[0] * 1.5, self.figsize[1]))

        # Seismic
        axes[0].imshow(seismic.T, aspect="auto", cmap=self.cmap_seismic, vmin=-vmax, vmax=vmax)
        axes[0].set_title("Seismic Amplitude")
        axes[0].set_xlabel("Trace")
        axes[0].set_ylabel("Sample")

        # True facies
        im1 = axes[1].imshow(
            true_facies.T,
            aspect="auto",
            cmap=cmap_f,
            vmin=-0.5,
            vmax=n_facies - 0.5,
        )
        fig.colorbar(im1, ax=axes[1], ticks=range(n_facies), label="Facies")
        axes[1].set_title("True Facies")
        axes[1].set_xlabel("Trace")

        # Predicted facies
        im2 = axes[2].imshow(
            pred_facies.T,
            aspect="auto",
            cmap=cmap_f,
            vmin=-0.5,
            vmax=n_facies - 0.5,
        )
        fig.colorbar(im2, ax=axes[2], ticks=range(n_facies), label="Facies")
        axes[2].set_title("Predicted Facies")
        axes[2].set_xlabel("Trace")

        plt.tight_layout()
        return fig

    def plot_attribute(
        self,
        attribute: np.ndarray,
        name: str = "Attribute",
    ) -> Figure:
        """Plot a single 2-D seismic attribute section.

        Parameters
        ----------
        attribute : ndarray of shape ``(n_traces, n_samples)``
        name : str
            Attribute name used as the plot title.

        Returns
        -------
        matplotlib.figure.Figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        im = ax.imshow(attribute.T, aspect="auto", cmap="viridis", interpolation="nearest")
        fig.colorbar(im, ax=ax, label=name)
        ax.set_title(name)
        ax.set_xlabel("Trace")
        ax.set_ylabel("Sample")
        plt.tight_layout()
        return fig

    def plot_confusion_matrix(
        self,
        cm: np.ndarray,
        n_facies: int,
        title: str = "Confusion Matrix",
    ) -> Figure:
        """Plot a confusion matrix as a heatmap.

        Parameters
        ----------
        cm : ndarray of shape ``(n_facies, n_facies)``
            Confusion matrix returned by :func:`sklearn.metrics.confusion_matrix`.
        n_facies : int
            Number of facies classes.

        Returns
        -------
        matplotlib.figure.Figure
        """
        fig, ax = plt.subplots(figsize=(6, 5))
        im = ax.imshow(cm, interpolation="nearest", cmap="Blues")
        fig.colorbar(im, ax=ax)

        tick_labels = [f"F{i}" for i in range(n_facies)]
        ax.set_xticks(range(n_facies))
        ax.set_yticks(range(n_facies))
        ax.set_xticklabels(tick_labels)
        ax.set_yticklabels(tick_labels)
        ax.set_xlabel("Predicted label")
        ax.set_ylabel("True label")
        ax.set_title(title)

        # Annotate cells
        thresh = cm.max() / 2.0
        for i in range(n_facies):
            for j in range(n_facies):
                ax.text(
                    j,
                    i,
                    str(cm[i, j]),
                    ha="center",
                    va="center",
                    color="white" if cm[i, j] > thresh else "black",
                    fontsize=9,
                )

        plt.tight_layout()
        return fig

    def plot_feature_importances(
        self,
        importances: np.ndarray,
        attribute_names: list[str],
        title: str = "Feature Importances",
    ) -> Figure:
        """Bar chart of random-forest feature importances.

        Parameters
        ----------
        importances : ndarray of shape ``(n_attrs,)``
        attribute_names : list of str

        Returns
        -------
        matplotlib.figure.Figure
        """
        idx = np.argsort(importances)[::-1]
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(range(len(importances)), importances[idx], color="steelblue")
        ax.set_xticks(range(len(importances)))
        ax.set_xticklabels([attribute_names[i] for i in idx], rotation=30, ha="right")
        ax.set_ylabel("Importance")
        ax.set_title(title)
        plt.tight_layout()
        return fig
