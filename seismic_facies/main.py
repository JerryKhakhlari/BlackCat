"""End-to-end seismic facies characterisation workflow.

Run this module directly to execute a complete analysis pipeline:

1. Generate synthetic seismic data with ground-truth facies labels.
2. Extract seismic attributes from the amplitude volume.
3. Train a Random-Forest facies classifier on the attributes.
4. Predict facies labels on the full volume.
5. Plot and save the results.

Usage
-----
    python -m seismic_facies.main
    # or
    python seismic_facies/main.py

All output figures are written to the ``output/`` directory.
"""

import os
import numpy as np

from .data_generation import SeismicDataGenerator
from .feature_extraction import SeismicAttributeExtractor
from .facies_classification import FaciesClassifier
from .visualization import SeismicVisualizer


def run_pipeline(
    n_traces: int = 100,
    n_samples: int = 200,
    n_facies: int = 4,
    output_dir: str = "output",
    random_state: int = 42,
) -> dict:
    """Execute the full seismic facies characterisation pipeline.

    Parameters
    ----------
    n_traces : int
        Number of synthetic seismic traces.
    n_samples : int
        Number of time samples per trace.
    n_facies : int
        Number of geological facies to simulate.
    output_dir : str
        Directory where output figures are saved.
    random_state : int
        Seed for reproducibility.

    Returns
    -------
    dict
        Dictionary with keys ``accuracy``, ``report``, ``confusion_matrix``,
        ``feature_importances``, and ``attribute_names``.
    """
    os.makedirs(output_dir, exist_ok=True)

    # ------------------------------------------------------------------ #
    # Step 1 – Generate synthetic seismic data                            #
    # ------------------------------------------------------------------ #
    print("Step 1: Generating synthetic seismic data …")
    generator = SeismicDataGenerator(
        n_traces=n_traces,
        n_samples=n_samples,
        n_facies=n_facies,
        random_state=random_state,
    )
    data = generator.generate()
    seismic = data["seismic"]
    true_facies = data["facies"]
    print(f"  Seismic shape : {seismic.shape}")
    print(f"  Facies labels : {np.unique(true_facies).tolist()}")

    # ------------------------------------------------------------------ #
    # Step 2 – Extract seismic attributes                                 #
    # ------------------------------------------------------------------ #
    print("Step 2: Extracting seismic attributes …")
    extractor = SeismicAttributeExtractor(window=5)
    attributes = extractor.extract(seismic)
    attr_names = extractor.attribute_names()
    print(f"  Attributes : {attr_names}")

    # ------------------------------------------------------------------ #
    # Step 3 – Train the facies classifier                                #
    # ------------------------------------------------------------------ #
    print("Step 3: Training facies classifier …")
    classifier = FaciesClassifier(n_estimators=100, random_state=random_state)
    stats = classifier.fit(attributes, true_facies)
    print(f"  Test accuracy : {stats['accuracy']:.4f}")
    print("  Classification report:")
    print(stats["report"])

    # ------------------------------------------------------------------ #
    # Step 4 – Predict facies on the full volume                          #
    # ------------------------------------------------------------------ #
    print("Step 4: Predicting facies …")
    pred_facies = classifier.predict(attributes)

    # ------------------------------------------------------------------ #
    # Step 5 – Visualise and save results                                 #
    # ------------------------------------------------------------------ #
    print("Step 5: Saving figures …")
    viz = SeismicVisualizer()

    # Seismic section
    fig = viz.plot_seismic_section(seismic, title="Synthetic Seismic Section")
    fig.savefig(os.path.join(output_dir, "seismic_section.png"), dpi=150)

    # True vs predicted facies
    fig = viz.plot_side_by_side(seismic, true_facies, pred_facies, n_facies=n_facies)
    fig.savefig(os.path.join(output_dir, "facies_comparison.png"), dpi=150)

    # Individual attribute sections
    for idx, name in enumerate(attr_names):
        fig = viz.plot_attribute(attributes[:, :, idx], name=name.replace("_", " ").title())
        fig.savefig(os.path.join(output_dir, f"attr_{name}.png"), dpi=150)

    # Confusion matrix
    fig = viz.plot_confusion_matrix(stats["confusion_matrix"], n_facies=n_facies)
    fig.savefig(os.path.join(output_dir, "confusion_matrix.png"), dpi=150)

    # Feature importances
    importances = classifier.feature_importances()
    fig = viz.plot_feature_importances(importances, attr_names)
    fig.savefig(os.path.join(output_dir, "feature_importances.png"), dpi=150)

    print(f"  Figures saved to '{output_dir}/'")

    import matplotlib.pyplot as plt
    plt.close("all")

    return {
        "accuracy": stats["accuracy"],
        "report": stats["report"],
        "confusion_matrix": stats["confusion_matrix"],
        "feature_importances": importances,
        "attribute_names": attr_names,
    }


if __name__ == "__main__":
    run_pipeline()
