import time
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import swprocess


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parent

DATA_DIR = PROJECT_DIR / "data"
RESULTS_DIR = PROJECT_DIR / "results"
FIGURES_DIR = PROJECT_DIR / "figures"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# USER CONFIGURATION
# ============================================================
#
# Dataset organization and file numbering are the responsibility
# of the operator prior to processing.
#
# Example:
#   range(1, 7)  ->  1.dat ... 6.dat
#   range(7, 16) ->  7.dat ... 15.dat
#
# Each range defines one acquisition dataset.


SETS = [
    range(1, 7),      # Dataset 1
    range(7, 16),    # Dataset 2
]


# ============================================================
# INPUT DATA
# ============================================================

dataset_files = [
    [DATA_DIR / f"{i}.dat" for i in file_range]
    for file_range in SETS
]

print("Dataset summary:")

for i, fnames in enumerate(dataset_files):

    if not fnames:
        raise ValueError(
            f"Dataset {i + 1} does not contain any input files."
        )

    missing = [
        fname
        for fname in fnames
        if not fname.exists()
    ]

    if missing:
        raise FileNotFoundError(
            f"Missing files in Dataset {i + 1}: {missing}"
        )

    print(
        f"  Dataset {i + 1}: "
        f"{len(fnames)} files "
        f"({fnames[0].name} - {fnames[-1].name})"
    )


# ============================================================
# MASW PROCESSING PARAMETERS
# ============================================================


# ------------------------------------------------------------
# 1. PROCESSING WORKFLOW
# ------------------------------------------------------------

# Processing workflow used by swprocess.
#
# "time-domain":
#   Processes the input seismic records in the time domain
#   before applying the selected wavefield transformation.
#
# Available workflow options depend on the installed
# swprocess version.

workflow = "time-domain"


# ------------------------------------------------------------
# 2. PRE-PROCESSING
# ------------------------------------------------------------

# Enable time-domain trimming.
#
# True:
#   Restricts the input records to the interval defined by
#   trim_begin and trim_end.
#
# False:
#   Uses the full recorded time interval.

trim = True

# Start of the analysis window [s].
#
# Must be within the recorded time range.
# Must be smaller than trim_end when trimming is enabled.

trim_begin = 0

# End of the analysis window [s].
#
# Must be greater than trim_begin when trimming is enabled
# and must be within the recorded time range.

trim_end = 0.5


# Enable interactive muting of the seismic records.
#
# True:
#   Allows the operator to define a narrow signal window
#   interactively.
#
# False:
#   No interactive muting is applied.
#
# Interactive muting can be useful when the usable surface-wave
# signal occupies a specific portion of the record.

mute = False

# Method used to define the signal window when muting is enabled.
#
# "interactive":
#   Allows the operator to select the signal window
#   interactively.
#
# Available method options depend on the installed
# swprocess version.

method = "interactive"

# Additional keyword arguments for the selected signal-window
# method.
#
# Use an empty dictionary when the selected method does not
# require additional parameters.

window_kwargs = {}


# ------------------------------------------------------------
# 3. FREQUENCY-DOMAIN SAMPLING
# ------------------------------------------------------------

# Enable zero-padding of the time-domain records before
# frequency-domain transformation.
#
# Zero-padding increases the density of the frequency sampling
# without adding new physical information to the recorded signal.

pad = True

# Desired linear frequency interval [Hz] after zero-padding.
#
# Must be greater than zero.
#
# Smaller values produce denser frequency sampling but may
# increase computational cost.

df = 0.5


# ------------------------------------------------------------
# 4. WAVEFIELD TRANSFORMATION
# ------------------------------------------------------------

# Wavefield transformation used to generate the dispersion image.
#
# "fdbf":
#   Frequency-Domain Beamforming.
#
# Other transformations may be available in swprocess,
# depending on the installed version.

transform = "fdbf"


# ------------------------------------------------------------
# 5. FREQUENCY SEARCH RANGE
# ------------------------------------------------------------

# Minimum frequency included in the dispersion analysis [Hz].
#
# Must be greater than zero and lower than fmax.
#
# Select according to the usable frequency content of the
# acquisition and the spatial resolution provided by the array.

fmin = 3

# Maximum frequency included in the dispersion analysis [Hz].
#
# Must be greater than fmin.
#
# Select according to the usable bandwidth of the acquisition,
# receiver response, sampling interval, signal quality, and
# spatial resolution of the array.

fmax = 100


# ------------------------------------------------------------
# 6. VELOCITY SEARCH RANGE
# ------------------------------------------------------------

# Minimum trial phase velocity [m/s].
#
# Must be greater than zero and lower than vmax.
#
# This value defines the lower boundary of the velocity search
# domain. Picks reaching this boundary should be inspected,
# because the actual maximum of the dispersion power may lie
# below the selected search range.

vmin = 100

# Maximum trial phase velocity [m/s].
#
# Must be greater than vmin.
#
# This value defines the upper boundary of the velocity search
# domain. Picks reaching this boundary should be inspected,
# because the actual maximum of the dispersion power may lie
# above the selected search range.

vmax = 500


# Number of trial velocity values evaluated within the velocity
# search range.
#
# Must be a positive integer.
#
# Increasing nvel produces finer velocity sampling but also
# increases computational cost.

nvel = 400

# Distribution used to sample trial velocities.
#
# "linear":
#   Uniform spacing between vmin and vmax.
#
# Available options depend on the installed swprocess version.

vspace = "linear"


# ------------------------------------------------------------
# 7. FDBF PARAMETERS
# ------------------------------------------------------------

# Weighting applied during Frequency-Domain Beamforming.
#
# "sqrt":
#   Applies square-root weighting.
#
# The weighting affects the contribution of the recorded
# wavefield to the beamforming result.

fdbf_weighting = "sqrt"

# Steering geometry used by the FDBF implementation.
#
# "cylindrical":
#   Uses cylindrical-wave steering.
#
# The selected steering model should be consistent with the
# physical source-wavefield assumptions of the investigation.

fdbf_steering = "cylindrical"


# ------------------------------------------------------------
# 8. SIGNAL-TO-NOISE RATIO
# ------------------------------------------------------------

# Enable SNR calculation.
#
# True:
#   Calculates SNR using the signal and noise windows defined
#   below.
#
# False:
#   SNR is not calculated.
#
# SNR is used here as a diagnostic of signal quality. It is not
# currently used to automatically reject dispersion picks.

snr = True

# Beginning of the noise window [s].
#
# The noise window should represent a portion of the record
# without the target surface-wave signal.

noise_begin = -0.009

# End of the noise window [s].
#
# Must be greater than noise_begin.

noise_end = 0

# Beginning of the signal window [s].
#
# The interval should contain the surface-wave signal used
# for the SNR calculation.

signal_begin = 0

# End of the signal window [s].
#
# Must be greater than signal_begin.

signal_end = 0.5

# Enable zero-padding for the SNR frequency-domain calculation.

pad_snr = True

# Desired linear frequency interval for the SNR calculation [Hz].
#
# Must be greater than zero.

df_snr = 1


# ============================================================
# CREATE MASW SETTINGS
# ============================================================

settings = swprocess.Masw.create_settings_dict(
    workflow=workflow,
    trim=trim,
    trim_begin=trim_begin,
    trim_end=trim_end,
    mute=mute,
    method=method,
    window_kwargs=window_kwargs,
    transform=transform,
    fmin=fmin,
    fmax=fmax,
    pad=pad,
    df=df,
    vmin=vmin,
    vmax=vmax,
    nvel=nvel,
    vspace=vspace,
    weighting=fdbf_weighting,
    steering=fdbf_steering,
    snr=snr,
    noise_begin=noise_begin,
    noise_end=noise_end,
    signal_begin=signal_begin,
    signal_end=signal_end,
    pad_snr=pad_snr,
    df_snr=df_snr,
)


# ============================================================
# PROCESSING
# ============================================================

processing_start = time.perf_counter()

wavefieldtransforms = [
    swprocess.Masw.run(
        fnames=fnames,
        settings=settings,
    )
    for fnames in dataset_files
]

print("\nProcessing summary:")

for i, wavefieldtransform in enumerate(wavefieldtransforms):

    frequency_min = wavefieldtransform.frequencies.min()
    frequency_max = wavefieldtransform.frequencies.max()

    print(f"\nDataset {i + 1}")

    print(
        f"  Frequency range: "
        f"{frequency_min:.1f}–{frequency_max:.1f} Hz"
    )

    print(
        f"  Velocity search range: "
        f"{vmin}–{vmax} m/s"
    )


# ============================================================
# ACQUISITION GEOMETRY DIAGNOSTICS
# ============================================================

def print_array_summary(wavefieldtransforms):
    """
    Print acquisition geometry and sensor information.

    The diagnostics distinguish physical sensor positions from
    source-to-receiver offsets and report the geometry used by
    the MASW processing workflow.
    """

    print("\nAcquisition geometry diagnostics:")

    for i, wavefieldtransform in enumerate(wavefieldtransforms):

        array = wavefieldtransform.array

        positions = np.asarray(
            array.position(),
            dtype=float,
        )

        offsets = np.asarray(
            array.offsets,
            dtype=float,
        )

        sensor_span = (
            positions.max() - positions.min()
        )

        receiver_spacing = np.diff(
            np.sort(positions)
        )

        uniform_spacing = (
            np.allclose(
                receiver_spacing,
                receiver_spacing[0],
            )
            if len(receiver_spacing) > 0
            else True
        )

        wavelength_reference = (
            2 * np.pi / array.kres
        )

        print(f"\nDataset {i + 1}")

        print("  Sensor positions:")
        print(f"    {positions}")

        print(
            f"  Minimum sensor position: "
            f"{positions.min():.3f} m"
        )

        print(
            f"  Maximum sensor position: "
            f"{positions.max():.3f} m"
        )

        print(
            f"  Sensor array span: "
            f"{sensor_span:.3f} m"
        )

        print(
            f"  Number of channels: "
            f"{array.nchannels}"
        )

        print(
            f"  Number of sensors: "
            f"{len(array.sensors)}"
        )

        print(
            f"  Source position: "
            f"x = {array.source.x:.3f} m"
        )

        source_inside_array = (
            positions.min()
            <= array.source.x
            <= positions.max()
        )

        print(
            f"  Source inside sensor range: "
            f"{source_inside_array}"
        )

        print(
            f"  Array center distance: "
            f"{array.array_center_distance}"
        )

        print(
            f"  Wavenumber resolution: "
            f"{array.kres:.6f} rad/m"
        )

        print(
            f"  Reference wavelength: "
            f"{wavelength_reference:.3f} m"
        )

        print(
            f"  Source-to-receiver offset range: "
            f"{offsets.min():.3f} to "
            f"{offsets.max():.3f} m"
        )

        print("  Receiver spacings:")
        print(
            f"    {receiver_spacing}"
        )

        print(
            f"  Uniform receiver spacing: "
            f"{uniform_spacing}"
        )

        print("  Sensors:")

        for j, sensor in enumerate(array.sensors):
            print(
                f"    Sensor {j + 1}: {sensor}"
            )


print_array_summary(wavefieldtransforms)

processing_elapsed = (
    time.perf_counter() - processing_start
)

print(
    f"\nProcessing time: "
    f"{processing_elapsed:.2f} s"
)


# ============================================================
# VISUALIZATION CONFIGURATION
# ============================================================

# Normalization applied to the dispersion image.
#
# "frequency-maximum":
#   Normalizes power independently across frequency.
#
# This improves visualization of frequency-dependent energy
# but does not represent absolute power variation between
# frequencies.

wavefield_normalization = "frequency-maximum"

# Display the array-resolution reference wavelength.

display_lambda_res = True

# Display the near-field reference.
#
# None:
#   Near-field reference is not displayed.
#
# Integer:
#   Number of array-center distances used for the reference.
#
# swprocess documents approximately 15% error for one array
# center distance and approximately 5% for two.

display_nearfield = False
number_of_array_center_distances = 1

# SNR reference displayed on the SNR plot.
#
# This is a visualization threshold only. It does not currently
# reject dispersion picks.

minimum_snr = 3.2


# ============================================================
# WAVEFIELD AND ACQUISITION FIGURES
# ============================================================

figures = []

for wavefieldtransform in wavefieldtransforms:

    fig = plt.figure(
        figsize=(6, 6),
        dpi=150,
    )

    gs = GridSpec(
        nrows=4,
        ncols=4,
        height_ratios=(1.7, 0.5, 1.5, 4),
        width_ratios=(1, 0.3, 1, 0.05),
        hspace=0.2,
        wspace=0.1,
    )

    ax0 = fig.add_subplot(gs[0, :])
    ax1 = fig.add_subplot(gs[2:4, 0])
    ax2 = fig.add_subplot(gs[2, 2])
    ax3 = fig.add_subplot(gs[3, 2])
    ax4 = fig.add_subplot(gs[3, 3])

    # Acquisition geometry.
    wavefieldtransform.array.plot(ax=ax0)

    ax0.set_yticks([])
    ax0.legend(ncol=2)

    # Seismic record waterfall.
    wavefieldtransform.array.waterfall(
        ax=ax1,
        amplitude_detrend=False,
        amplitude_normalization="each",
    )

    if trim:
        ax1.set_ylim(
            (trim_end, trim_begin)
        )

    # Signal-to-noise ratio.
    wavefieldtransform.plot_snr(
        ax=ax2,
        plot_kwargs=dict(
            color="black",
            label="SNR",
        ),
    )

    snr_xlim = ax2.get_xlim()

    ax2.plot(
        snr_xlim,
        [minimum_snr] * 2,
        linewidth=2,
        color="red",
        label=f"SNR = {minimum_snr}",
    )

    ax2.set_xlim(snr_xlim)
    ax2.set_xticklabels([])
    ax2.set_xlabel("")
    ax2.set_ylabel("SNR")
    ax2.set_yscale("log")
    ax2.legend(loc="upper left")

    # Near-field reference.
    nearfield = (
        number_of_array_center_distances
        if display_nearfield
        else None
    )

    # Dispersion image.
    wavefieldtransform.plot(
        fig=fig,
        ax=ax3,
        cax=ax4,
        normalization=wavefield_normalization,
        nearfield=nearfield,
    )

    dispersion_xlim = ax3.get_xlim()
    dispersion_ylim = ax3.get_ylim()

    # Array-resolution wavelength reference.
    if display_lambda_res:

        kres = wavefieldtransform.array.kres

        kvelocity = (
            2
            * np.pi
            * wavefieldtransform.frequencies
            / kres
        )

        ax3.plot(
            wavefieldtransform.frequencies,
            kvelocity,
            label=(
                r"$\lambda_{a,ref}$"
                f" = {2 * np.pi / kres:.2f} m"
            ),
            linewidth=1.5,
            color="black",
            linestyle="--",
        )

        ax3.legend(loc="upper right")

    ax3.set_xlim(dispersion_xlim)
    ax2.set_xlim(dispersion_xlim)
    ax3.set_ylim(dispersion_ylim)

    ax2.set_xscale("log")
    ax2.set_xticks([])

    ax3.set_xscale("log")

    figures.append(fig)

    plt.show()


# ============================================================
# DISPERSION CURVE EXTRACTION
# ============================================================

domains = [
    ["frequency", "velocity"],
    ["wavelength", "velocity"],
]

xtype = [x for x, _ in domains]
ytype = [y for _, y in domains]


# Dataset identifiers must be unique.
dataset_identifiers = [
    f"dataset_{i + 1}"
    for i in range(len(wavefieldtransforms))
]


# Generate colors for visualization only.
cmap = plt.get_cmap(
    "Paired",
    len(dataset_identifiers),
)

colors = [
    mpl.colors.to_hex(
        cmap.colors[i]
    )
    for i in range(
        len(dataset_identifiers)
    )
]


if len(dataset_files) != len(dataset_identifiers):
    raise ValueError(
        "Number of datasets and dataset identifiers must match."
    )


# Calculate dispersion picks once and store them.
peaks = []

for i, (
    wavefieldtransform,
    identifier,
) in enumerate(
    zip(
        wavefieldtransforms,
        dataset_identifiers,
    )
):

    velocity = wavefieldtransform.find_peak_power(
        by="frequency-maximum"
    )

    peak = swprocess.peaks.Peaks(
        wavefieldtransform.frequencies,
        velocity,
        identifier=identifier,
    )

    peaks.append(peak)

    frequencies = np.asarray(
        peak.frequency
    )

    velocities = np.asarray(
        peak.velocity
    )

    lower_limit = np.isclose(
        velocities,
        vmin,
    )

    upper_limit = np.isclose(
        velocities,
        vmax,
    )

    print(f"\n{identifier}")

    print(
        f"  Frequency range: "
        f"{frequencies.min():.1f}–"
        f"{frequencies.max():.1f} Hz"
    )

    print(
        f"  Velocity range: "
        f"{velocities.min():.1f}–"
        f"{velocities.max():.1f} m/s"
    )

    print(
        f"  Number of picks: "
        f"{len(velocities)}"
    )

    print(
        f"  Picks at vmin ({vmin} m/s): "
        f"{np.sum(lower_limit)}"
    )

    print(
        f"  Picks at vmax ({vmax} m/s): "
        f"{np.sum(upper_limit)}"
    )

    if np.any(upper_limit):

        print("  Frequencies at vmax:")

        for frequency, velocity_value in zip(
            frequencies[upper_limit],
            velocities[upper_limit],
        ):
            print(
                f"    {frequency:.1f} Hz "
                f"-> {velocity_value:.1f} m/s"
            )

    if np.any(lower_limit):

        print("  Frequencies at vmin:")

        for frequency, velocity_value in zip(
            frequencies[lower_limit],
            velocities[lower_limit],
        ):
            print(
                f"    {frequency:.1f} Hz "
                f"-> {velocity_value:.1f} m/s"
            )


# ============================================================
# DISPERSION CURVE FIGURE
# ============================================================

fig, axs = plt.subplots(
    ncols=len(xtype),
    figsize=(6, 3),
    dpi=150,
    gridspec_kw=dict(
        wspace=0.4
    ),
)

for peak, color, identifier in zip(
    peaks,
    colors,
    dataset_identifiers,
):

    peaksuite = swprocess.PeaksSuite.from_peaks(
        [peak]
    )

    peaksuite.plot(
        xtype=xtype,
        ax=axs,
        ytype=ytype,
        plot_kwargs=dict(
            color=color,
            label=identifier,
        ),
    )

axs[-1].legend(
    bbox_to_anchor=(1.1, 0.5),
    loc="center left",
)

dispersion_curve_figure_path = (
    FIGURES_DIR
    / "masw_dispersion_curves.png"
)

fig.savefig(
    dispersion_curve_figure_path,
    dpi=300,
    bbox_inches="tight",
)

print(
    f"Figure saved: {dispersion_curve_figure_path}"
)

plt.show()

# ============================================================
# EXPORT CONFIGURATION
# ============================================================

prefix = "masw_dispersion"

json_path = (
    RESULTS_DIR
    / f"{prefix}.json"
)

json_path.unlink(
    missing_ok=True
)


# ============================================================
# EXPORT DISPERSION RESULTS
# ============================================================

for i, peak in enumerate(peaks):

    peak.to_json(
        fname=json_path,
        append=i > 0,
    )


# ============================================================
# EXPORT FIGURES
# ============================================================

for i, (
    figure,
    identifier,
) in enumerate(
    zip(
        figures,
        dataset_identifiers,
    )
):

    figure_path = (
        FIGURES_DIR
        / f"{prefix}_{identifier}.png"
    )

    figure.savefig(
        figure_path,
        dpi=300,
        bbox_inches="tight",
    )

    print(
        f"Figure saved: {figure_path}"
    )


# ============================================================
# FINAL SUMMARY
# ============================================================

print(
    f"\nResults saved to: "
    f"{RESULTS_DIR}"
)

print(
    f"Figures saved to: "
    f"{FIGURES_DIR}"
)