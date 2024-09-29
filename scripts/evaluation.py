"""
Evaluation and Visualization Script for String Matching Algorithms

This script evaluates the performance of various string matching algorithms on different datasets.
It calculates standard evaluation metrics such as accuracy, precision, recall, F1-score, and ROC-AUC.
The script also generates evaluation metric plots and confusion matrix heatmaps for each algorithm.

The results of the evaluation and the generated figures are stored in the configured directories,
making it easy to analyze and compare the performance of the algorithms.

Functions
---------
No defined functions. This script runs as a standalone evaluation tool.

Attributes
----------
datasets : list of str
    List of dataset names to evaluate. Possible values are "STREET", "FULLNAME", and "BOTH".
THRESHOLDS : dict
    Dictionary containing the similarity thresholds for each matching algorithm.
METRICS : list of str
    List of evaluation metrics used to assess the performance of the algorithms.

Examples
--------
To run the script and evaluate all configured datasets:

$ python evaluate.py

The script will generate CSV files with evaluation results and confusion matrices, as well as
graphs for each dataset and algorithm.

Raises
------
SystemExit
    If this file is executed as a standalone script without any defined functions.

Notes
-----
- The script assumes that the validated data for each dataset has been preprocessed and stored
  in the `VALIDATION_DIR` directory.
- Evaluation results and confusion matrices are saved in the `DATA_DIR` and `FIGURES_DIR` directories.

Dependencies
------------
- `pandas`
- `matplotlib`
- `scikit-learn`
- `config.config`
- `utils.io`

Make sure all dependencies are installed and configured correctly before running this script.
"""


import pandas as pd
import matplotlib.pyplot as plt

from config.config import METRICS, THRESHOLDS, DATA_DIR
from utils.io import load_validated_data, export_eval_data, plot_metrics, plot_confusion_matrix, _to_csv
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score


if __name__ == '__main__':
    datasets = ["STREET", "FULLNAME", "BOTH"]

    for dataset_name in datasets:
        if dataset_name == "BOTH":
            data_street = load_validated_data("STREET")
            data_fullname = load_validated_data("FULLNAME")
            DATA = pd.concat([data_street, data_fullname], ignore_index=True)
        else:
            DATA = load_validated_data(dataset_name)

        if DATA.empty:
            print(f"No data found for dataset '{dataset_name}'. Skipping...")
            continue

        eval_df = pd.DataFrame(index=METRICS)
        for algo in THRESHOLDS:
            y_true_col = f"{algo.upper()}_TRUE_MATCH"
            y_pred_col = f"{algo.upper()}_BEST_MATCH_BINARY"

            if y_true_col not in DATA.columns or y_pred_col not in DATA.columns:
                print(f"Columns for algorithm '{algo}' not found in dataset '{dataset_name}'. Skipping...")
                continue

            y_true = DATA[y_true_col]
            y_pred = DATA[y_pred_col]

            mask = y_true.notna() & y_pred.notna()
            y_true = y_true[mask]
            y_pred = y_pred[mask]

            if y_true.empty:
                print(f"No valid data for algorithm '{algo}' in dataset '{dataset_name}'. Skipping...")
                continue

            if y_true.dtype == "object":
                y_true = y_true.astype(bool)
                y_pred = y_pred.astype(bool)

            valid_labels = (0, 1)
            if not set(y_true.unique()).issubset(valid_labels) or not set(y_pred.unique()).issubset(valid_labels):
                print(f"Invalid labels detected in algorithm '{algo}' for dataset '{dataset_name}'. Skipping...")
                continue

            accuracy = accuracy_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred)
            recall = recall_score(y_true, y_pred)
            f1 = f1_score(y_true, y_pred)
            roc_auc = roc_auc_score(y_true, y_pred)

            eval_df[algo] = [accuracy, precision, recall, f1, roc_auc]

        if eval_df.empty:
            print(f"No evaluation data for dataset '{dataset_name}'. Skipping...")
            continue

        eval_df = export_eval_data(eval_df, dataset_name)
        metrics_fig = plot_metrics(eval_df, dataset_name)
        plt.close(metrics_fig)

        cm_list = []
        for algo in THRESHOLDS:
            y_true_col = f"{algo.upper()}_TRUE_MATCH"
            y_pred_col = f"{algo.upper()}_BEST_MATCH_BINARY"

            if y_true_col not in DATA.columns or y_pred_col not in DATA.columns:
                continue

            y_true = DATA[y_true_col]
            y_pred = DATA[y_pred_col]

            mask = y_true.notna() & y_pred.notna()
            y_true = y_true[mask]
            y_pred = y_pred[mask]

            if y_true.empty:
                continue

            if y_true.dtype == "object":
                y_true = y_true.astype(bool)
                y_pred = y_pred.astype(bool)

            valid_labels = (0, 1)
            if not set(y_true.unique()).issubset(valid_labels) or not set(y_pred.unique()).issubset(valid_labels):
                continue

            cm = confusion_matrix(y_true, y_pred)
            cm_df = pd.DataFrame(cm, index=["True Negative", "True Positive"], columns=["Predicted Negative", "Predicted Positive"])
            _to_csv(cm_df, DATA_DIR.joinpath("confusion_matrices").joinpath(f"{algo}_{dataset_name}_confusion_matrix.csv"))

            cm_fig = plot_confusion_matrix(cm, algo, dataset_name)
            cm_list.append(cm_fig)
            plt.close(cm_fig)