"""
Configuration module for setting up directory paths, thresholds, and other constants.

This module defines various constants and paths used throughout the project. It provides
directory structures for input, output, and profiling data, and sets default values for
worker threads and debug flags. Additionally, it configures algorithm thresholds and
evaluation metrics for the string similarity algorithms.

Attributes
----------
MAX_WORKERS : int
    Maximum number of concurrent workers for parallel operations. Calculated as the minimum
    of 32 or the number of CPU cores available + 4.
DEBUG_FLAG : bool
    Global flag to indicate if the application is in debug mode. Set to `False` by default.
ROOT_DIR : pathlib.Path
    Root directory of the project, determined relative to the location of this file.
DATA_DIR : pathlib.Path
    Path to the 'data' directory, where all data-related files are stored.
INPUT_DIR : pathlib.Path
    Path to the 'input' directory, containing raw and cleaned input files.
RAW_DIR : pathlib.Path
    Path to the 'raw' input directory, which holds unprocessed data files.
CLEAN_DIR : pathlib.Path
    Path to the 'clean' input directory, which holds preprocessed data files.
VALIDATION_DIR : pathlib.Path
    Path to the directory where files awaiting validation are stored.
PROFILING_DIR : pathlib.Path
    Path to the 'profiling' directory, which contains profiling results.
PROFILING_AVERAGES_DIR : pathlib.Path
    Directory for storing average profiling results.
PROFILING_DOT_DIR : pathlib.Path
    Directory for storing dot files generated during profiling.
FIGURES_DIR : pathlib.Path
    Path to the 'figures' directory for storing graphs and visualizations.
CONF_MAT_DIR : pathlib.Path
    Directory to store confusion matrix images.
PROFILING_GRAPH_DIR : pathlib.Path
    Directory to store profiling graphs.
MODEL_DIR : pathlib.Path
    Directory for storing machine learning models or intermediary results.
THRESHOLDS : DotDict
    Dictionary-like object containing the similarity thresholds for different algorithms.
    The keys are algorithm names, and the values are similarity thresholds.
METRICS : list of str
    List of evaluation metrics used to measure the performance of algorithms.

Raises
------
SystemExit
    If this file is executed as a standalone script.
"""


import os

from pathlib import Path

from config.dotdict import DotDict


MAX_WORKERS = min(32, os.cpu_count() + 4)
DEBUG_FLAG = False

ROOT_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
RAW_DIR = INPUT_DIR / "raw"
CLEAN_DIR = INPUT_DIR / "clean"
VALIDATION_DIR = DATA_DIR / "await_validation"
PROFILING_DIR = DATA_DIR / "profiling"
PROFILING_AVERAGES_DIR = PROFILING_DIR / "averages"
PROFILING_DOT_DIR = PROFILING_DIR / "dot"

FIGURES_DIR = ROOT_DIR / "figures"
CONF_MAT_DIR = FIGURES_DIR / "confusion_matrices"
PROFILING_GRAPH_DIR = FIGURES_DIR / "prof_graph"

MODEL_DIR = ROOT_DIR / "models"

THRESHOLDS = DotDict({
    "regex": 0.5,
    "levenshtein": 0.8,  # not the distance anymore, but similarity in percent
    "jaccard": 0.5,
    "tfidf": 0.5,
    "ngram": 0.5,
    "dice": 0.5,
})

METRICS = ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"]


if __name__ == '__main__':
    raise SystemExit("Cannot run this file.")
