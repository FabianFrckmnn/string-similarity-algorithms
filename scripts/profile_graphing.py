"""
Profiling Graph Utility

This module provides utility functions to create visual representations of profiling data.
The functions generate graph files from profiling data, combine and average multiple profiling
runs, and save the results in various formats. It relies on external tools like `gprof2dot`
and `dot` to convert profiling data into graphical representations.

The module can be used to automate the creation of profiling graphs for performance analysis
and comparison between different runs of a program.

Functions
---------
__makedirs()
    Creates directories for storing profiling averages, dot files, and graph files.
__graph_profiles(prof_dir, dot_dir, graph_dir)
    Converts profiling data from `.prof` files into `.dot` files and then generates `.png` images.
__combine_and_average_profiles(prof_files, output_file)
    Combines and averages multiple profiling statistics files into a single `.prof` file.
__graph_average_profiles()
    Creates average profiling graphs by combining profiling files with the same prefix and
    generates the corresponding `.dot` and `.png` files.

Examples
--------
The functions in this module are typically called together in a sequence:

>>> __makedirs()
>>> __graph_profiles(PROFILING_DIR, PROFILING_DOT_DIR, PROFILING_GRAPH_DIR)
>>> __graph_average_profiles()

Dependencies
------------
- `gprof2dot` (command-line tool)
- `dot` (from Graphviz)

Raises
------
SystemExit
    If this file is executed as a standalone script.

Notes
-----
This module uses private functions (denoted by a double underscore) and is intended to be
called as a utility within other scripts or processes. It should not be run directly.
"""


import os
import pstats
import subprocess

from itertools import chain
from config.config import THRESHOLDS, PROFILING_DIR, PROFILING_AVERAGES_DIR, PROFILING_DOT_DIR, PROFILING_GRAPH_DIR


def __makedirs():
    """
    Create directories for storing profiling results.

    This function ensures that the directories for storing profiling averages,
    dot files, and graph files exist. If they do not exist, they are created.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    os.makedirs(PROFILING_AVERAGES_DIR, exist_ok=True)
    os.makedirs(PROFILING_DOT_DIR, exist_ok=True)
    os.makedirs(PROFILING_GRAPH_DIR, exist_ok=True)


def __graph_profiles(prof_dir, dot_dir, graph_dir):
    """
    Convert profiling data into dot and graph files.

    This function iterates through all `.prof` files in the specified profiling
    directory, converts them to `.dot` files using `gprof2dot`, and then generates
    `.png` graph files using the `dot` command.

    Parameters
    ----------
    prof_dir : str
        The directory containing the `.prof` profiling files.
    dot_dir : str
        The directory where the generated `.dot` files will be stored.
    graph_dir : str
        The directory where the generated `.png` graph files will be stored.

    Returns
    -------
    None
    """
    for filename in os.listdir(prof_dir):
        if filename.endswith(".prof"):
            prof_path = os.path.join(prof_dir, filename)
            dot_filename = filename.replace(".prof", ".dot")
            dot_path = os.path.join(dot_dir, dot_filename)
            png_filename = filename.replace(".prof", ".png")
            png_path = os.path.join(graph_dir, png_filename)

            subprocess.run(["gprof2dot", "-f", "pstats", prof_path, "-o", dot_path])
            subprocess.run(["dot", "-Tpng", dot_path, "-o", png_path])


def __combine_and_average_profiles(prof_files, output_file):
    """
    Combine and average multiple profiling files into a single profile.

    This function reads multiple profiling `.prof` files, combines their statistics,
    and calculates the average statistics across all files. The averaged profiling
    data is then saved to a new `.prof` file.

    Parameters
    ----------
    prof_files : list of str
        List of paths to the profiling `.prof` files to be combined and averaged.
    output_file : str
        The name of the output file for the combined and averaged profiling results.

    Returns
    -------
    None
    """
    combined_stats = None

    for prof_file in prof_files:
        stats = pstats.Stats(prof_file)

        if combined_stats is None:
            combined_stats = stats
        else:
            combined_stats.add(stats)

    combined_stats.total_calls = combined_stats.total_calls / len(prof_files)
    combined_stats.total_tt = combined_stats.total_tt / len(prof_files)

    combined_stats.dump_stats(PROFILING_AVERAGES_DIR.joinpath(f"{output_file}_average.prof"))


def __graph_average_profiles():
    """
    Create average profiling graphs for groups of profiling files.

    This function groups profiling files by their prefixes, combines and averages them,
    and generates the corresponding dot and graph files for the averages.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    datasets = set([f[:13] for f in os.listdir(PROFILING_DIR) if f.endswith(".prof")])
    for group in set(chain(THRESHOLDS.keys(), datasets)):
        prof_files = [os.path.join(PROFILING_DIR, f) for f in os.listdir(PROFILING_DIR) if
                      f.endswith(".prof") and group in f]
        __combine_and_average_profiles(prof_files, group)

    os.makedirs(PROFILING_DOT_DIR / "averages", exist_ok=True)
    os.makedirs(PROFILING_GRAPH_DIR / "averages", exist_ok=True)
    __graph_profiles(PROFILING_AVERAGES_DIR, PROFILING_DOT_DIR / "averages", PROFILING_GRAPH_DIR / "averages")


if __name__ == '__main__':
    __makedirs()
    __graph_profiles(PROFILING_DIR, PROFILING_DOT_DIR, PROFILING_GRAPH_DIR)
    __graph_average_profiles()
