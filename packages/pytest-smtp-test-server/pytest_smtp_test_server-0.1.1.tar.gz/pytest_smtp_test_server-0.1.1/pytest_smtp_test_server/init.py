"""
Code for Plugin Initialisation
"""
from _pytest.config import Config
from _pytest.config.argparsing import Parser

from pytest_smtp_test_server.internal import Plugin


def configure(config: Config, plugin_name: str = "smtp_test_server"):
    """
    Configure Pytest Plugin
    """
    config.pluginmanager.register(Plugin(config), name=f"{plugin_name}_plugin")


def unconfigure(config: Config, plugin_name: str = "smtp_test_server"):
    """
    Unconfigure Pytest Plugin
    """
    config.pluginmanager.unregister(name=f"{plugin_name}_plugin")


def add_option(parser: Parser, plugin_name: str = "mail_mock"):  # pylint: disable=unused-argument
    """
    Configure Options
    """
