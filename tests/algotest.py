import unittest

import pandas as pd
import numpy as np

from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from sklearn.feature_extraction.text import CountVectorizer

from config.config import THRESHOLDS, RAW_DIR, MAX_WORKERS, DEBUG_FLAG
from config.profiler import Profiler
from config.logger import Logger
from utils.io import export_data_for_validation
from scripts.datahandler import get_data
from scripts.algorithms import dice, jaccard, levenshtein, ngram, regex, tfidf
from scripts.preprocessing import preprocess


class TestSettings:
    algorithm = dice
    data_column = "STREET"
    match_column = "STREET"
    match_file_name = "847ff2869e9fa08110422d98fe15553a1931fc8d59876977b3ab0f45.csv"

    def __init__(self):
        self.log = Logger(__name__)
        self.log.info(f"Logger {self.log.get_name()} initialized.")
        self.match_file = RAW_DIR.joinpath(self.match_file_name)
        if not DEBUG_FLAG:
            self.__confirm_test()
            self.prof = Profiler(name=f"TEST_{self.match_file_name[:5]}_{self.algorithm.NAME}")

    def __confirm_test(self):
        self.log.info("Debug flag is false.")
        self.log.info(
            f"Are you sure you want to run {self.algorithm.NAME} on file {self.match_file_name} and column {self.match_column}?")
        self.log.info("[Y]es | [N]o")
        response = input()
        if response.lower() == "n":
            exit(0)
        elif response.lower() == "y":
            return
        else:
            self.log.info("Invalid response.")
            self.__confirm_test()


# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    case = TestSettings()
    algorithm = case.algorithm

    data, match = get_data(DEBUG_FLAG, case.match_file)

    if not DEBUG_FLAG:
        data = data.assign(
            STREET=data["STREET_NAME"] + " " + data["STREET_NO"],
            FULLNAME=data["FIRSTNAME"] + " " + data["LASTNAME"]
        )
        case.log.info("Starting profiling...")
        case.prof.enable()

    case.log.info("Preprocessing...")
    prep_data = preprocess(data, case.data_column)
    prep_match = preprocess(match, case.match_column)

    case.log.info("Preparing algorithm...")
    algorithm.prep_(prep_data, prep_match)

    results = case.algorithm.perform_matching()
    results_df = pd.DataFrame(results)

    case.log.info("Exporting results...")
    if DEBUG_FLAG:
        results_df = case.algorithm.export_results(results_df, "DEBUG", "DEBUG")
        exit(0)
    results_df = case.algorithm.export_results(results_df, case.match_file_name, case.data_column)

    case.log.info("Saving profile...")
    case.prof.disable()
    case.prof.save_show_profile()

    # unittest.main()
