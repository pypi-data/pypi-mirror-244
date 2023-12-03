"""
Implementation of the fixtures
"""
from smtp_test_server.context import SmtpMockServer


def smtp_server_fixture():
    """
    All auto-config SMTP Server fixture
    """
    with SmtpMockServer() as srv:
        yield srv
