# MASW Processing and Dispersion Analysis

## Overview

This repository provides a reproducible Python workflow for processing and analyzing Multichannel Analysis of Surface Waves (MASW) data.

The workflow uses [`swprocess`](https://github.com/jpvantassel/swprocess) to process active-source seismic records, perform wavefield transformation, generate dispersion images, and extract experimental dispersion-curve picks.

The project is designed as a general and adaptable workflow for research-oriented MASW investigations, with emphasis on transparent processing parameters, acquisition geometry, quality-control diagnostics, and reproducible results.

The main objectives are to provide a structured workflow for:

* Organizing and validating MASW acquisition datasets.
* Inspecting acquisition geometry and receiver configuration.
* Configuring preprocessing and MASW processing parameters.
* Applying Frequency-Domain Beamforming (FDBF).
* Computing signal-to-noise ratio (SNR).
* Generating dispersion images.
* Automatically extracting dispersion-curve picks.
* Reporting acquisition and processing quality-control information.
* Exporting processed results and figures.

## Methodology

The processing workflow follows these main stages:

1. Input data organization and validation.
2. Acquisition geometry inspection.
3. Signal preprocessing.
4. Wavefield transformation.
5. Signal-to-noise analysis.
6. Dispersion image generation.
7. Automatic dispersion-curve extraction.
8. Quality-control diagnostics.
9. Visualization.
10. Export of results and figures.

### Current Processing Configuration

The example workflow currently uses:

* Time-domain MASW workflow.
* Frequency-Domain Beamforming (FDBF).
* Frequency range: 3–100 Hz.
* Velocity search range: 100–500 m/s.
* 400 velocity samples.
* Square-root FDBF weighting.
* Cylindrical steering.
* Signal-to-noise ratio (SNR) analysis.
* Configurable signal and noise time windows.
* Configurable preprocessing and transformation parameters.

These values represent the current example configuration and are not intended as universal MASW processing parameters. Processing settings should be adapted to the acquisition geometry, seismic data quality, expected subsurface conditions, and objectives of each investigation.

## Quality Control and Acquisition Diagnostics

The workflow reports acquisition and processing information that can be used to assess the consistency between the seismic dataset, acquisition geometry, processing configuration, and resulting dispersion information.

The current diagnostics include:

* Number of input records.
* Number of channels and sensors.
* Sensor positions.
* Physical sensor-array span.
* Source position.
* Source location relative to the receiver array.
* Receiver geometry and spacing.
* Offset range.
* Wavenumber-resolution information.
* Frequency search limits.
* Velocity search limits.
* Number of extracted dispersion picks.
* Minimum and maximum picked velocities.
* Number of picks reaching the lower velocity-search boundary.
* Number of picks reaching the upper velocity-search boundary.

These diagnostics are intended to provide processing traceability and help identify potential limitations or inconsistencies that may affect interpretation of the dispersion results.

## Project Structure

```text
MASW-Uncertainty-Analysis/
│
├── data/
│   └── MASW input data
│
├── figures/
│   └── Generated figures
│
├── results/
│   └── Exported dispersion results
│
├── masw_processing.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Requirements

The workflow has been developed and tested with:

* Python 3.11
* `swprocess` 0.3.0
* NumPy 1.24.2
* Matplotlib 3.7.1

The exact package versions are specified in `requirements.txt` to support reproducible execution.

## Installation

Clone the repository and install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Place the MASW input files in the `data/` directory.

Dataset groups and processing parameters can be configured directly in `masw_processing.py`.

Run the processing workflow with:

```bash
python masw_processing.py
```

The workflow generates:

* Dispersion and acquisition figures in `figures/`.
* Extracted dispersion results in `results/`.

## Reproducibility

The processing configuration is explicitly defined in the Python script, including preprocessing, wavefield transformation, frequency and velocity ranges, velocity sampling, FDBF parameters, and SNR settings.

The Python package versions are fixed in `requirements.txt` to provide a reproducible computational environment.

The workflow is designed so that acquisition-specific parameters can be modified without changing the underlying processing structure.

## Scientific Scope

This repository provides the processing foundation for quantitative analysis of MASW dispersion data.

The current implementation focuses on acquisition validation, wavefield processing, dispersion imaging, automatic peak picking, and quality-control diagnostics.

The project is intended to serve as a foundation for subsequent analysis of dispersion-curve variability and uncertainty, including the evaluation of factors associated with acquisition geometry, processing parameters, and dispersion-curve extraction.

## Reference Software

This workflow uses `swprocess`, an open-source Python package for surface-wave processing developed and maintained by Joseph P. Vantassel and collaborators. The package supports active-source MASW processing and rigorous surface-wave dispersion statistics.

For research applications using `swprocess`, consult the official documentation and citation guidance:

* [swprocess documentation](https://swprocess.readthedocs.io/en/latest/)
* [swprocess GitHub repository](https://github.com/jpvantassel/swprocess)

## Citation

If this repository is used in research or technical work, please cite the repository and the underlying software according to the applicable citation information.

For `swprocess`, the developers request citation of the associated software and scientific publication describing its workflow for robust estimates of surface-wave dispersion uncertainty.

## License

This repository does not currently specify a project license.

A license should be added before distributing the repository as open-source software.

```

### Dos decisiones que dejé intencionalmente para después

**1. `data/`**

No afirmé que vas a distribuir los datos reales. Si esos `.dat` no pueden publicarse, podemos dejar `data/` fuera del repositorio y explicar en el README cómo incorporar datos localmente.

**2. License**

No pondría todavía `MIT`, `GPL`, etc. Primero tenemos que decidir qué licencia quieres para **tu propio código**. Además, `swprocess` 0.3.0 está publicado bajo GPLv3+, pero eso no significa automáticamente que tu repositorio tenga que usar la misma licencia; hay que revisar la relación entre tu código y la dependencia antes de elegirla.

**Este README ya lo puedes usar como base oficial.** El siguiente paso de nuestra auditoría debería ser revisar `masw_processing.py` con el mismo estándar, antes de hacer el primer push.
```