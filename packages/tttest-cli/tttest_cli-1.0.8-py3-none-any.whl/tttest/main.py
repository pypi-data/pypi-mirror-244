from tttest.cli import cli_run
from tttest.serve import api_serve
from tttest.serve import mock_serve
from tttest.version import get_version_banner


def serve():
    print(get_version_banner('serve'))
    api_serve.serve()


def mock():
    print(get_version_banner('mock'))
    mock_serve.mock()


def run():
    print(get_version_banner())
    cli_run.run()


if __name__ == '__main__':
    dir()
    mock()
    # serve()
    # run()
