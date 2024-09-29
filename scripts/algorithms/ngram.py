import pandas as pd
import numpy as np

from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer

from config.config import THRESHOLDS, RAW_DIR, MAX_WORKERS, DEBUG_FLAG
from config.logger import Logger
from utils.io import export_data_for_validation


NAME: str = "ngram"
match_ngrams_matrix = None
match_original_series: pd.Series = None
data_ngrams_matrix = None
data_original_series: pd.Series = None
indices: list = None
n: int = 2


def __ngram_similarity(match_vector, data_vectors):
    intersection = data_vectors.multiply(match_vector).sum(axis=1)
    match_size = match_vector.sum()
    data_sizes = data_vectors.sum(axis=1)

    intersection = np.asarray(intersection).flatten()
    data_sizes = np.asarray(data_sizes).flatten()

    union = match_size + data_sizes - intersection

    with np.errstate(divide="ignore", invalid="ignore"):
        similarities = intersection / union
        similarities = np.nan_to_num(similarities)

    return similarities


def __calculate_best_match(idx):
    try:
        match_original = match_original_series.iloc[idx]
        match_vector = match_ngrams_matrix[idx]

        if match_vector.nnz == 0:
            return {
                "MATCH": match_original,
                "BEST_FOUND_MATCH": None,
                "TRUE_MATCH": None,
                "BEST_MATCH": None,
            }

        similarities = __ngram_similarity(match_vector, data_ngrams_matrix)

        max_similarity_idx = similarities.argmax()
        max_similarity = similarities[max_similarity_idx]
        best_match_original = data_original_series.iloc[max_similarity_idx]

        return {
            "MATCH": match_original,
            "BEST_FOUND_MATCH": best_match_original,
            "TRUE_MATCH": None,
            "BEST_MATCH": max_similarity,
        }
    except Exception as e:
        print(f"Error in calculate_best_match at index {idx}: {e}")
        raise


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

    all_texts = pd.concat([data_norm_series, match_norm_series], ignore_index=True)
    vectorizer.fit(all_texts)

    data_ngrams_matrix = vectorizer.transform(data_norm_series)
    match_ngrams_matrix = vectorizer.transform(match_norm_series)


def export_results(df, match_file_name, data_column) -> pd.DataFrame:
    df["BEST_MATCH_BINARY"] = df["BEST_MATCH"] >= THRESHOLDS.ngram
    return export_data_for_validation(df, match_file_name, data_column, "NGRAM")


if __name__ == '__main__':
    log = Logger(__name__)
    log.info(f"Please run this algorithm via main.py, the unittest or use one of the jupyter notebooks!")
    exit(1)
