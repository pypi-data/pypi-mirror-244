"""
Base Code for the pytest Plugin
"""
from _pytest.config import Config

CONFIG_KEY = "__pytest_smtp_test_server.plugin:CONFIG__"


class Plugin:  # pylint: disable=too-few-public-methods
    """
    The main plugin class
    """

    def __init__(self, config: Config) -> None:
        """
        Initialize the class, and simply store the value of the command line argument, as class attribute.

        :param config: Pytest configuration
        """
        setattr(Plugin, CONFIG_KEY, config)
