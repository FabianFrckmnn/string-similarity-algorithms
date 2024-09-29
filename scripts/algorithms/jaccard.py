import pandas as pd
import numpy as np

from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer

from config.config import THRESHOLDS, RAW_DIR, MAX_WORKERS, DEBUG_FLAG
from config.logger import Logger
from utils.io import export_data_for_validation


NAME = "jaccard"
match_norm_series = None
match_original_series = None
data_original_series = None
data_vectors = None
vectorizer = None
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

    match_vector = vectorizer.transform([s1_clean])

    intersection = data_vectors.multiply(match_vector).sum(axis=1)
    union = data_vectors.sum(axis=1) + match_vector.sum() - intersection

    with np.errstate(divide="ignore", invalid="ignore"):
        jaccard_similarities = intersection / union
        jaccard_similarities = jaccard_similarities.A1
        jaccard_similarities = np.nan_to_num(jaccard_similarities)

    max_similarity = jaccard_similarities.max()
    best_match_idx = jaccard_similarities.argmax()
    best_match_original = data_original_series.iloc[best_match_idx]

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
    global match_norm_series, match_original_series, data_original_series, data_vectors, vectorizer, indices
    data_df, data_norm_series, data_original_series = data
    match_df, match_norm_series, match_original_series = match

    vectorizer = CountVectorizer(binary=True)
    indices = match_df.index.tolist()

    vectorizer.fit(data_norm_series)
    data_vectors = vectorizer.transform(data_norm_series)


def export_results(df, match_file_name, data_column) -> pd.DataFrame:
    df["BEST_MATCH_BINARY"] = df["BEST_MATCH"] >= THRESHOLDS.jaccard
    return export_data_for_validation(df, match_file_name, data_column, "JACCARD")


if __name__ == '__main__':
    log = Logger(__name__)
    log.info(f"Please run this algorithm via main.py, the unittest or use one of the jupyter notebooks!")
    exit(1)

