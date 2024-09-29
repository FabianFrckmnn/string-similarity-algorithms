"""
Project Name: Data Matching and String Similarity Pipeline

Overview
--------
This project is designed to process and match records from multiple CSV files using a variety of string similarity algorithms. The goal is to identify and link related records across different data sources. The project employs multiple algorithms, such as Levenshtein distance, Jaccard similarity, Dice coefficient, N-gram similarity, regex-based matching, and TF-IDF cosine similarity, to determine the similarity between string fields.

The project consists of several core modules for data handling, preprocessing, algorithm implementation, evaluation, and profiling. It provides a flexible configuration system, enabling users to easily switch between algorithms and adjust matching parameters based on the desired threshold and column criteria.

Key Features
------------
- **Data Preprocessing**: Cleans and normalizes input data to ensure consistent formatting for matching.
- **String Matching Algorithms**: Supports various string similarity algorithms to compare and match records.
- **Performance Profiling**: Measures execution time and memory usage for different parts of the pipeline.
- **Evaluation Metrics**: Computes accuracy, precision, recall, F1-score, and ROC-AUC to assess algorithm performance.
- **Jupyter Notebooks**: Demonstrates the usage of each algorithm and compares results interactively.
- **Modular Design**: Organized directory structure for configurations, scripts, tests, and utilities.

Project Structure
-----------------
- `config/`: Configuration files for paths, algorithm thresholds, logging, and profiling.
- `data/`: Input data files and directories for profiling results.
- `figures/`: Stores confusion matrices and other figures generated during evaluation.
- `models/`: Directory to store machine learning models or intermediary results.
- `notebooks/`: Jupyter Notebooks for demonstrating and evaluating algorithms.
- `scripts/`: Main scripts for data handling, algorithm implementation, and evaluation.
- `tests/`: Unit tests for validating the functionality of the project components.
- `utils/`: Helper functions and utilities for file I/O and data formatting.

How It Works
------------
1. **Load and Preprocess Data**: The data is read from CSV files, and specific columns are selected for matching based on configuration settings.
2. **Algorithm Selection**: The user can choose from multiple string similarity algorithms to perform matching based on predefined or custom criteria.
3. **Matching and Evaluation**: The selected algorithm processes the data and produces matching results, which are then evaluated using standard metrics.
4. **Profiling and Logging**: Profiling tools track the execution time and resource utilization, while logging captures the progress and results.

Use Cases
---------
The project can be used for various data matching scenarios, such as:
- Matching customer records from multiple databases to identify duplicates.
- Linking address information from different sources.
- Comparing free-form text entries to find similar descriptions.

Dependencies
------------
- Python 3.7 or above
- Required packages listed in `requirements.txt` or `environment.yml`
"""


import pandas as pd

from config.config import RAW_DIR, DEBUG_FLAG
from config.profiler import Profiler
from config.logger import Logger
from scripts.datahandler import get_data
from scripts.preprocessing import preprocess
from scripts.algorithms import dice, jaccard, levenshtein, ngram, regex, tfidf


__docformat__ = "numpy en"


TO_MATCH = {
    "847ff2869e9fa08110422d98fe15553a1931fc8d59876977b3ab0f45.csv": ["STREET", "FULLNAME"],
    "5679d4fb298abda0f9c8ac05a042d8c542489a8b5ad0f628a3d76aba.csv": ["STREET", "FULLNAME"],
    "6864d8088e15d75b89292c1146260c93111bdfbad77d3d73da8d5e31.csv": ["CONTACT"],
    "77112c0ac2e616623999e02bb91921c69a269f94619ef19ca2f7844a.csv": ["STREET", "FULLNAME"],
    "fa225c615c7bd91813b036c77dcdf41178b744a82ca150feaa5c3a2c.csv": ["STREET", "FULLNAME"]
}
ALGORITHM = levenshtein


if __name__ == '__main__':
    log = Logger(__name__)
    for match_file_name, match_columns in TO_MATCH.items():
        match_file = RAW_DIR.joinpath(match_file_name)

        prof = Profiler(name=f"{match_file_name[:13]}_{ALGORITHM.NAME}")
        prof.enable()

        for column in match_columns:
            log.info(f"Starting matching for {match_file_name} on column {column}")

            data_column = "FULLNAME" if column == "CONTACT" else column
            match_column = column

            data, match = get_data(DEBUG_FLAG, match_file)

            data = data.assign(
                STREET=data["STREET_NAME"] + " " + data["STREET_NO"],
                FULLNAME=data["FIRSTNAME"] + " " + data["LASTNAME"]
            )

            if "FULLNAME" not in match.columns and "FIRSTNAME" in match.columns and "LASTNAME" in match.columns:
                match = match.assign(FULLNAME=match["FIRSTNAME"] + " " + match["LASTNAME"])

            prep_data = preprocess(data, data_column)
            prep_match = preprocess(match, match_column)
            ALGORITHM.prep_(prep_data, prep_match)

            results = ALGORITHM.perform_matching()
            results_df = pd.DataFrame(results)
            results_df = ALGORITHM.export_results(results_df, match_file_name, data_column)

        prof.disable()
        prof.save_show_profile()
