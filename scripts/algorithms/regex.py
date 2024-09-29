import re

import pandas as pd
import numpy as np

from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

from config.config import THRESHOLDS, RAW_DIR, MAX_WORKERS
from config.logger import Logger
from utils.io import export_data_for_validation


NAME = "regex"
match_norm_series: pd.Series = None
match_original_series: pd.Series = None
data_norm_series: pd.Series = None
data_original_series: pd.Series = None
data_norm_array_lower = None
indices = None


def __regex_matching(s1_clean, s2_series):
    pattern = re.compile(re.escape(s1_clean), re.IGNORECASE)
    return s2_series.str.contains(pattern, regex=True)


def __reverse_regex_matching(s1_clean):
    s1_lower = s1_clean.lower()
    positions = np.char.find(s1_lower, data_norm_array_lower)
    return positions >= 0


def __calculate_best_match(idx):
    match_original = match_original_series.iloc[idx]
    match_norm = match_norm_series.iloc[idx]
    s1_clean = match_norm

    s1_in_s2 = __regex_matching(s1_clean, data_norm_series)
    s2_in_s1 = __reverse_regex_matching(s1_clean)
    mask = s1_in_s2 | s2_in_s1
    matches = data_original_series[mask]

    if not matches.empty:
        best_match = matches.iloc[0]
        score = True
    else:
        best_match = None
        score = False

    return {
        "MATCH": match_original,
        "BEST_FOUND_MATCH": best_match,
        "TRUE_MATCH": None,
        "BEST_MATCH": score
    }


def perform_matching():
    results = []
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(__calculate_best_match, idx): idx for idx in indices}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Matching", unit="match"):
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Exception occurred for index {futures[future]}: {e}")
        return results


def prep_(data: tuple[pd.DataFrame, pd.Series, pd.Series], match: tuple[pd.DataFrame, pd.Series, pd.Series]):
    global match_norm_series, match_original_series, data_norm_series, data_original_series, data_norm_array_lower, indices
    data_df, data_norm_series, data_original_series = data
    match_df, match_norm_series, match_original_series = match

    indices = match_df.index.tolist()

    data_norm_array_lower = data_norm_series.str.lower().values.astype(str)


def export_results(df, match_file_name, data_column) -> pd.DataFrame:
    df["BEST_MATCH_BINARY"] = df["BEST_MATCH"] >= THRESHOLDS.regex
    return export_data_for_validation(df, match_file_name, data_column, "REGEX")


if __name__ == '__main__':
    log = Logger(__name__)
    log.info(f"Please run this algorithm via main.py, the unittest or use one of the jupyter notebooks!")
    exit(1)
