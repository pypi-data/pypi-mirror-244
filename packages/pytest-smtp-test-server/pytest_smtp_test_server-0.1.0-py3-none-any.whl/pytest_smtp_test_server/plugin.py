"""
Plugin Bootstrap Code
"""
import pytest

from pytest_smtp_test_server.fixture import smtp_server_fixture
from pytest_smtp_test_server.init import add_option, configure, unconfigure
from pytest_smtp_test_server.version_check import check_pytest_version, check_python_version

check_python_version()
check_pytest_version()

pytest_configure = configure
pytest_unconfigure = unconfigure
pytest_addoption = add_option

smtp_mock = pytest.fixture(scope="function")(smtp_server_fixture)
class_smtp_mock = pytest.fixture(scope="class")(smtp_server_fixture)
session_smtp_mock = pytest.fixture(scope="session")(smtp_server_fixture)
package_smtp_mock = pytest.fixture(scope="package")(smtp_server_fixture)
module_smtp_mock = pytest.fixture(scope="module")(smtp_server_fixture)
