"""
Profiler: A class for profiling code execution and saving performance statistics.

This class extends the `cProfile.Profile` class and provides methods for saving and
displaying profiling statistics. It allows users to measure the performance of specific
code segments and export the profiling results for analysis.

Attributes
----------
__name : str
    Name of the profiler, used as a prefix for the output profiling file.

Methods
-------
_save_profile()
    Saves the profiling results to a file in the `PROFILING_DIR` directory with a
    filename pattern of `{name}_profiling.prof`.
_show_profile()
    Displays the profiling statistics, sorted by cumulative time, and prints the top
    10 results to the console.
save_show_profile()
    Saves the profiling results and then displays the top profiling statistics.

Raises
------
SystemExit
    If this file is executed as a standalone script.
"""


import cProfile
import pstats

from config.config import PROFILING_DIR


class Profiler(cProfile.Profile):
    """
    A custom profiler class for saving and displaying profiling statistics.

    This class inherits from `cProfile.Profile` and provides additional methods for
    saving the profiling results to a file and displaying the top statistics in the
    console. The results can be used to analyze the performance of different parts
    of the code, making it easier to identify bottlenecks.

    Parameters
    ----------
    name : str
        The name of the profiler, used to create a unique filename for the profiling results.

    Methods
    -------
    _save_profile()
        Saves the profiling results to a file in the `PROFILING_DIR` directory.
    _show_profile()
        Displays the profiling statistics, sorted by cumulative time.
    save_show_profile()
        Combines `_save_profile` and `_show_profile` to save and display the profiling results.
    """

    def __init__(self, name: str):
        """
        Initialize the Profiler with a given name.

        Parameters
        ----------
        name : str
            The name of the profiler. It is used to create a unique filename for the profiling
            results file in the `PROFILING_DIR` directory.
        """
        self.__name = name
        super().__init__()

    def _save_profile(self):
        """
        Save the profiling statistics to a file.

        This method saves the profiling results to a `.prof` file located in the `PROFILING_DIR`
        directory. The filename is generated using the format `{name}_profiling.prof`.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self.dump_stats(PROFILING_DIR.joinpath(f"{self.__name}_profiling.prof"))

    def _show_profile(self):
        """
        Display the profiling statistics sorted by cumulative time.

        This method loads the profiling statistics from the saved `.prof` file and prints the top
        10 results sorted by cumulative execution time (`cumtime`).

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        stats = pstats.Stats(PROFILING_DIR.joinpath(f"{self.__name}_profiling.prof").__str__())
        stats.sort_stats("cumtime").print_stats(10)

    def save_show_profile(self):
        """
        Save and display the profiling statistics.

        This method combines `_save_profile` and `_show_profile` to first save the profiling
        results to a file and then display the top profiling statistics in the console.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self._save_profile()
        self._show_profile()


if __name__ == '__main__':
    raise SystemExit("Cannot run this file.")
