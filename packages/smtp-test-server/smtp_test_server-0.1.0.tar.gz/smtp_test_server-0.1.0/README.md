# smtp-test-server

Based on the [`aiosmtpd`](https://github.com/aio-libs/aiosmtpd), this packages offers you a simple way to integrate
a SMTP server into your test code.

Currently, the server does not support authentication, TLS or anything special instead of sending mails.

All mails are collected in the `messages` property of the mock and can be evaluated there.

Looking for a `pytest` SMTP mock fixture? Take a look at this project:
[git.codebau.dev/pytest-plugins/pytest-smtp-test-server](https://git.codebau.dev/pytest-plugins/pytest-smtp-test-server).

## Installation

### Installation with "pip"

```Bash
pip install smtp-test-server
```

### Installation with "poetry"

```Bash
poetry add --group dev smtp-test-server
```

## Usage

Simple usage, with auto assigning a free port number on `127.0.0.1`:

```Python
from smtp_test_server.context import SmtpMockServer

def test_send_mail():
    with SmtpMockServer() as smtp_mock:
        my_mail_method(smtp_host=smtp_mock.host, smtp_port=smtp_mock.port)
    assert len(smtp_mock.messages) == 1
    assert smtp_mock.messages[0]["from"] == "my-test@sender.org"
```

Want to have more control over host and port? Use it like this:

```Python
with SmtpMockServer(bind_host="223.12.9.177", bind_port=2525):
    ...
```

Ports are automatically closed when leaving the context.
