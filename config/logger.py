import logging

from pprint import pformat


class Logger:
    """
    A custom logger class with pretty formatting for log messages.

    Attributes
    ----------
    __logger : logging.Logger
        The underlying logger instance.

    Methods
    -------
    info(message)
        Logs an informational message.
    debug(message)
        Logs a debug message.
    get_name()
        Returns the name of the logger.
    """

    class __PrettyFormatter(logging.Formatter):
        """
        A custom formatter to pretty-print log messages.

        Methods
        -------
        format(record)
            Formats the log record to strip leading/trailing whitespace from each line.
        """

        def format(self, record):
            """
            Format the specified log record.

            Parameters
            ----------
            record : logging.LogRecord
                The log record to be formatted.

            Returns
            -------
            str
                The formatted log message.
            """

            record.message = "\n".join(map(str.strip, record.getMessage().splitlines()))

            return super().format(record)

    __logger: logging.Logger

    def __init__(self, name: str, level=logging.INFO) -> None:
        """
        Initialize the Logger instance.

        Parameters
        ----------
        name : str
            The name of the logger.
        level : int, optional
            The logging level (default is logging.INFO)
        """

        self.__logger = logging.getLogger(name)
        self.__logger.setLevel(level)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(self.__PrettyFormatter("%(message)s"))
        self.__logger.addHandler(console_handler)

    def info(self, message) -> None:
        """
        Log an informational message.

        Parameters
        ----------
        message : any
            The message to log.
        """

        self.__logger.info(f"{pformat(message)}\n")

    def debug(self, message) -> None:
        """
        Log a debug message.

        Parameters
        ----------
        message : any
            The message to log.
        """

        self.__logger.debug(f"{pformat(message)}\n")

    def get_name(self) -> str:
        """
        Get the name of the logger.

        Returns
        -------
        str
            The name of the logger.
        """

        return self.__logger.name


if __name__ == '__main__':
    raise SystemExit("Cannot run this file.")
