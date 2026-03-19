# BlackCat — Seismic Facies Characterisation in Python

> Use of Python in Geophysics

## Overview

This project implements a complete **seismic facies characterisation** workflow
using Python and standard scientific computing tools
(*NumPy*, *SciPy*, *scikit-learn*, *matplotlib*).

Seismic facies characterisation is a key step in subsurface geological
interpretation.  It involves classifying regions of a seismic volume into
distinct *facies*—groups of samples that share similar amplitude and texture
characteristics—which can then be mapped to rock/fluid types.

### Pipeline

```
Synthetic seismic data
        │
        ▼
Seismic attribute extraction
  (amplitude, envelope, instantaneous phase & frequency, local variance)
        │
        ▼
Random-Forest facies classifier (scikit-learn)
        │
        ▼
Predicted facies volume  +  performance metrics  +  figures
```

## Project Structure

```
BlackCat/
├── seismic_facies/
│   ├── __init__.py
│   ├── data_generation.py      # Synthetic seismic / layered-earth model
│   ├── feature_extraction.py   # Seismic attribute computation
│   ├── facies_classification.py# Random-Forest classifier wrapper
│   ├── visualization.py        # Plotting utilities (matplotlib)
│   └── main.py                 # End-to-end pipeline entry-point
├── tests/
│   ├── __init__.py
│   └── test_seismic_facies.py  # pytest test suite (24 tests)
├── requirements.txt
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Running the Pipeline

```bash
python -m seismic_facies.main
```

Output figures are written to the `output/` directory.

## Running Tests

```bash
pip install pytest
pytest tests/ -v
```

## Module Reference

| Module | Class / Function | Description |
|---|---|---|
| `data_generation` | `SeismicDataGenerator` | Generates synthetic seismic traces with a layered-earth model and ground-truth facies labels via Ricker wavelet convolution |
| `feature_extraction` | `SeismicAttributeExtractor` | Computes instantaneous amplitude, phase, frequency and local variance via the Hilbert transform |
| `facies_classification` | `FaciesClassifier` | Trains a `RandomForestClassifier` on the attribute feature vectors; reports accuracy, classification report and confusion matrix |
| `visualization` | `SeismicVisualizer` | Produces publication-quality figures of seismic sections, facies maps, confusion matrices and feature importances |

## Key Parameters

| Parameter | Default | Description |
|---|---|---|
| `n_traces` | 100 | Number of seismic traces |
| `n_samples` | 200 | Time/depth samples per trace |
| `n_facies` | 4 | Number of geological facies |
| `dominant_frequency` | 30 Hz | Ricker wavelet dominant frequency |
| `sampling_interval` | 0.002 s | Trace sampling interval (2 ms) |
| `n_estimators` | 100 | Trees in the Random Forest |
