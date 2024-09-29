import pandas as pd
import numpy as np

from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer

from config.config import THRESHOLDS, RAW_DIR, MAX_WORKERS, DEBUG_FLAG
from config.logger import Logger
from utils.io import export_data_for_validation


NAME = "dice"
match_ngrams_matrix = None
match_original_series = None
data_ngrams_matrix = None
data_original_series = None
n = 2  # Always bigram for dice coefficient
indices = None


def __dice_coefficient(match_vector, data_vectors):
    intersection = data_vectors.multiply(match_vector).sum(axis=1)

    match_size = match_vector.sum()
    data_sizes = data_vectors.sum(axis=1)

    numerator = 2 * intersection
    denominator = match_size + data_sizes

    with np.errstate(divide="ignore", invalid="ignore"):
        dice_coefficients = numerator / denominator
        dice_coefficients = np.nan_to_num(dice_coefficients)

    return np.asarray(dice_coefficients).flatten()


def __calculate_best_match(idx):
    match_original = match_original_series.iloc[idx]
    match_vector = match_ngrams_matrix[idx]

    if match_vector.nnz == 0:
        return {
            "MATCH": match_original,
            "BEST_FOUND_MATCH": None,
            "TRUE_MATCH": None,
            "BEST_MATCH": None,
        }

    dice_coefficients = __dice_coefficient(match_vector, data_ngrams_matrix)
    max_similarity_idx = dice_coefficients.argmax()
    max_similarity = dice_coefficients[max_similarity_idx]
    best_match_original = data_original_series.iloc[max_similarity_idx]

    return {
        "MATCH": match_original,
        "BEST_FOUND_MATCH": best_match_original,
        "TRUE_MATCH": None,
        "BEST_MATCH": max_similarity,
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
    global match_ngrams_matrix, match_original_series, data_ngrams_matrix, data_original_series, n, indices
    data_df, data_norm_series, data_original_series = data
    match_df, match_norm_series, match_original_series = match

    vectorizer = CountVectorizer(analyzer="char", ngram_range=(n, n), binary=False)
    indices = match_df.index.tolist()

    all_texts = pd.concat([data_norm_series, match_norm_series])
    vectorizer.fit(all_texts)

    data_ngrams_matrix = vectorizer.transform(data_norm_series)
    match_ngrams_matrix = vectorizer.transform(match_norm_series)


def export_results(df, match_file_name, data_column) -> pd.DataFrame:
    df["BEST_MATCH_BINARY"] = df["BEST_MATCH"] >= THRESHOLDS.dice
    return export_data_for_validation(df, match_file_name, data_column, "DICE")


if __name__ == '__main__':
    log = Logger(__name__)
    log.info(f"Please run this algorithm via main.py, the unittest or use one of the jupyter notebooks!")
    exit(1)
