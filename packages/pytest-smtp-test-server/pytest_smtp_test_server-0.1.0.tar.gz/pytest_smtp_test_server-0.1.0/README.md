# pytest-smtp-test-server

pytest plugin for using [`smtp-test-server`](https://git.codebau.dev/jed/smtp-test-server) as pytest mock fixtures.

## Installation

### Installation with "pip"

```Bash
pip install pytest-smtp-test-server
```

### Installation with "poetry"

```Bash
poetry add --group dev pytest-smtp-test-server
```

## Usage

After installation, one could easily use one of the provided fixtures in your pytest test case:

```Python
def test_mail_sending(smtp_mock):
    my_mail_sending_method(host=smtp_mock.host, port=smtp_mock.port)
    assert len(smtp_mock.messages) == 1
```

## Scopes

Fixtures are provided for different [pytest fixture scopes](https://docs.pytest.org/en/stable/explanation/fixtures.html)
for your convenience:

| fixture name          | pytest fixture scope |
|-----------------------|----------------------|
| `smtp_mock`           | function             |
| `class_smtp_mock`     | class                |
| `module_smtp_mock`    | module               |
| `package_smtp_mock`   | package              |
| `session_smtp_mock`   | session              |

If you require more control over hosts and ports, consider using
[`smtp-test-server`](https://git.codebau.dev/jed/smtp-test-server) directly.
