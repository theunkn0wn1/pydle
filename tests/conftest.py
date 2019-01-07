import asyncio
import os

import pytest

from .bot_fixtures import TestClient, TestSetupClient


def pytest_addoption(parser):
    # Add option to skip meta (test suite-testing) tests.
    parser.addoption('--skip-meta', action='store_true', help='skip test suite-testing tests')
    # Add option to skip slow tests.
    parser.addoption('--skip-slow', action='store_true', help='skip slow tests')
    # Add option to skip real life tests.
    parser.addoption('--skip-real', action='store_true', help='skip real life tests')

    # add options to specify IRC server
    parser.addoption("--server", help="irc server to connect to during testing",
                     default="localhost")
    parser.addoption("--port", type=int, help="port to connect on", default=6667)
    parser.addoption("--use-tls", action="store_true")


def pytest_runtest_setup(item):
    if 'meta' in item.keywords and item.config.getoption('--skip-meta'):
        pytest.skip('skipping meta test (--skip-meta given)')
    if 'slow' in item.keywords and item.config.getoption('--skip-slow'):
        pytest.skip('skipping slow test (--skip-slow given)')

    if 'real' in item.keywords:
        if item.config.getoption('--skip-real'):
            pytest.skip('skipping real life test (--skip-real given)')
        if (not os.getenv('PYDLE_TESTS_REAL_HOST') or
                not os.getenv('PYDLE_TESTS_REAL_PORT')):
            pytest.skip('skipping real life test (no real server given)')


@pytest.fixture(scope="session")
def client_fx(pytestconfig):
    """
    Provides a featurized and connected Irc Client


    """

    host = pytestconfig.getoption("--server")
    port = pytestconfig.getoption("--port")
    use_tls = pytestconfig.getoption("--use-tls")

    loop = asyncio.get_event_loop_policy().new_event_loop()

    client = TestClient(eventloop=loop)

    loop.run_until_complete(client.connect(hostname=host, port=port, tls=use_tls, tls_verify=False))

    return client


@pytest.fixture(scope="session")
def first_run(pytestconfig):
    loop = asyncio.get_event_loop_policy().new_event_loop()

    host = pytestconfig.getoption("--server")
    port = pytestconfig.getoption("--port")
    use_tls = pytestconfig.getoption("--use-tls")

    # register ourselves a nickname then exit
    setup_client = TestSetupClient(eventloop=loop)
    setup_client.run(hostname=host, port=port, tls=use_tls, tls_verify=False)
