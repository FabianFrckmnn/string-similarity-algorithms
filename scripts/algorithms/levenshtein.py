import pandas as pd

from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from rapidfuzz import process
from rapidfuzz.distance import Levenshtein

from config.config import THRESHOLDS, RAW_DIR, MAX_WORKERS, DEBUG_FLAG
from config.logger import Logger
from utils.io import export_data_for_validation


NAME = "levenshtein"
match_norm_series: pd.Series = None
match_original_series: pd.Series = None
data_norm_series: pd.Series = None
data_original_series: pd.Series = None
indices = None


def __calculate_best_match(idx):
    match_original = match_original_series.iloc[idx]
    match_norm = match_norm_series.iloc[idx]
    s1_clean = match_norm.strip()

    if not s1_clean:
        return {
            "MATCH": match_original,
            "BEST_FOUND_MATCH": None,
            "TRUE_MATCH": None,
            "BEST_MATCH": None,
        }

    best_match = process.extractOne(
        s1_clean,
        data_norm_series,
        scorer=Levenshtein.normalized_similarity,
        processor=None
    )

    if best_match:
        best_match_idx = best_match[2]
        best_match_score = best_match[1]
        best_match_original = data_original_series.iloc[best_match_idx]

        return {
            "MATCH": match_original,
            "BEST_FOUND_MATCH": best_match_original,
            "TRUE_MATCH": None,
            "BEST_MATCH": best_match_score,
        }
    else:
        return {
            "MATCH": match_original,
            "BEST_FOUND_MATCH": None,
            "TRUE_MATCH": None,
            "BEST_MATCH": None,
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
    global match_norm_series, match_original_series, data_norm_series, data_original_series, indices
    data_df, data_norm_series, data_original_series = data
    match_df, match_norm_series, match_original_series = match

    indices = match_df.index.tolist()


def export_results(df, match_file_name, data_column) -> pd.DataFrame:
    df["BEST_MATCH_BINARY"] = df["BEST_MATCH"] >= THRESHOLDS.levenshtein
    return export_data_for_validation(df, match_file_name, data_column, "LEVENSHTEIN")


if __name__ == '__main__':
    log = Logger(__name__)
    log.info(f"Please run this algorithm via main.py, the unittest or use one of the jupyter notebooks!")
    exit(1)
