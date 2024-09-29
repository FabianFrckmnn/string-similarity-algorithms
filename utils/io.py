"""
Utility functions for handling CSV I/O, data export, and visualization.

This module provides helper functions for reading from and writing to CSV files,
exporting data for validation and evaluation, and generating visualizations like
evaluation metrics plots and confusion matrices. The functions are designed to
integrate seamlessly with other parts of the data matching and evaluation pipeline.

Functions
---------
_to_csv(df, path)
    Saves a DataFrame to a CSV file at the specified path using semicolon (;) as a separator.
_from_csv(path)
    Reads a CSV file from the specified path into a DataFrame, using semicolon (;) as a separator.
export_data_for_validation(df, input_file, column, algorithm)
    Exports data to a CSV file for validation purposes, using a structured directory format.
export_eval_data(df, dataset_name)
    Saves evaluation results to a CSV file for a given dataset name.
load_validated_data(dataset_name)
    Loads and merges validated data files for a specified dataset from various subdirectories.
plot_metrics(df, dataset_name)
    Creates a bar plot of evaluation metrics for each algorithm and saves it as an image.
plot_confusion_matrix(confusion_matrix, algorithm, dataset_name)
    Creates and saves a confusion matrix heatmap for a given algorithm and dataset.

Raises
------
SystemExit
    If this file is executed as a standalone script.
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from os import PathLike, listdir, path
from datetime import date

from config.config import DATA_DIR, VALIDATION_DIR, FIGURES_DIR, CONF_MAT_DIR


def _to_csv(df: pd.DataFrame, path: str | PathLike[str]) -> None:
    """
    Save a DataFrame to a CSV file.

    This function saves the given DataFrame to a CSV file at the specified path, using
    a semicolon (`;`) as the separator and UTF-8 encoding.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame to be saved.
    path : str or PathLike
        The path to save the CSV file.

    Returns
    -------
    None
    """
    df.to_csv(path, sep=";", encoding="utf-8", index=True)
    return


def _from_csv(path: str | PathLike[str]) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame.

    This function reads a CSV file from the specified path into a DataFrame,
    using a semicolon (`;`) as the separator and UTF-8 encoding.

    Parameters
    ----------
    path : str or PathLike
        The path to the CSV file.

    Returns
    -------
    pd.DataFrame
        The loaded DataFrame.
    """
    return pd.read_csv(path, sep=";", encoding="utf-8", index_col=0)


def export_data_for_validation(df: pd.DataFrame, input_file: str, column: str, algorithm: str) -> pd.DataFrame:
    """
    Export data for validation purposes.

    This function saves the DataFrame to a CSV file in a structured directory format
    based on the input file name, column name, and algorithm. The output is stored in
    the `VALIDATION_DIR`.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing the data to be validated.
    input_file : str
        The name of the input file (used to create the directory structure).
    column : str
        The column name being validated.
    algorithm : str
        The name of the matching algorithm used.

    Returns
    -------
    pd.DataFrame
        The original DataFrame.
    """
    df.columns = ["MATCH", *[f"{algorithm}_{col}" for col in df.columns][1:]]
    _to_csv(df, VALIDATION_DIR.joinpath(input_file[:13]).joinpath(column).joinpath(f"{date.today()}_{algorithm}_NEED_VALIDATION.csv"))
    return df


def export_eval_data(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
    """
    Export evaluation results.

    This function saves evaluation results from a DataFrame to a CSV file in the `DATA_DIR`
    with a filename based on the current date and the dataset name.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing evaluation results.
    dataset_name : str
        The name of the dataset being evaluated.

    Returns
    -------
    pd.DataFrame
        The original DataFrame.
    """
    _to_csv(df, DATA_DIR.joinpath(f"{date.today()}_{dataset_name}_eval_results.csv"))
    return df


def load_validated_data(dataset_name) -> pd.DataFrame:
    """
    Load validated data from multiple directories.

    This function searches for validated CSV files in subdirectories of the `VALIDATION_DIR`
    that match the specified dataset name. It merges all matching files into a single
    DataFrame, avoiding duplicate columns.

    Parameters
    ----------
    dataset_name : str
        The name of the dataset to be loaded.

    Returns
    -------
    pd.DataFrame
        The merged DataFrame containing all validated data.
    """
    dynamic_dirs = [d for d in VALIDATION_DIR.iterdir() if d.is_dir()]

    list_of_dfs = []
    for dn_dir in dynamic_dirs:
        validated_dir = dn_dir / dataset_name / "validated"
        csv_files = [file for file in validated_dir.glob("*.csv") if file.is_file()]
        dfs = [pd.read_csv(csv_file, index_col=0) for csv_file in csv_files]
        if dfs:
            merged_df = pd.concat(dfs, axis=1, join="outer")
            merged_df = merged_df.loc[:, ~merged_df.columns.duplicated()]
            list_of_dfs.append(merged_df)

    if list_of_dfs:
        DATA = pd.concat(list_of_dfs, axis=0, ignore_index=True)
    else:
        DATA = pd.DataFrame()

    return DATA


def plot_metrics(df: pd.DataFrame, dataset_name: str) -> plt.Figure:
    """
    Create a bar plot of evaluation metrics for each algorithm.

    This function generates a bar plot from a DataFrame containing evaluation metrics
    and saves it as a PNG image in the `FIGURES_DIR`.

    Parameters
    ----------
    df : pd.DataFrame
        The DataFrame containing evaluation metrics for each algorithm.
    dataset_name : str
        The name of the dataset being evaluated.

    Returns
    -------
    plt.Figure
        The matplotlib Figure object of the created plot.
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    df.T.plot(kind="bar", ax=ax, title=f"Evaluation metrics for each algorithm on {dataset_name}")
    ax.set_ylabel("Score")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=15)
    plt.tight_layout()

    plt.savefig(FIGURES_DIR.joinpath(f"{date.today()}_{dataset_name}_eval_results.png"))
    return fig


def plot_confusion_matrix(confusion_matrix, algorithm: str, dataset_name: str) -> plt.Figure:
    """
    Create a confusion matrix heatmap.

    This function generates a heatmap from a given confusion matrix and saves it as a
    PNG image in the `CONF_MAT_DIR`.

    Parameters
    ----------
    confusion_matrix : array-like
        The confusion matrix to be visualized.
    algorithm : str
        The name of the matching algorithm used.
    dataset_name : str
        The name of the dataset being evaluated.

    Returns
    -------
    plt.Figure
        The matplotlib Figure object of the created heatmap.
    """
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(confusion_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=["False", "True"],
                yticklabels=["False", "True"])
    plt.title(f"Confusion Matrix for {algorithm} on {dataset_name}")
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")

    plt.savefig(CONF_MAT_DIR.joinpath(f"{date.today()}_{dataset_name}_cm_{algorithm}.png"))
    return fig


if __name__ == '__main__':
    raise SystemExit("Cannot run this file.")
