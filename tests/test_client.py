import time
import pydle

from pytest import raises, mark
from .fixtures import with_client
from .mocks import Mock, MockEventLoop

pydle.client.PING_TIMEOUT = 10


## Initialization.

@with_client(invalid_kwarg=False)
def test_client_superfluous_arguments(client_fx):
    assert client_fx.logger.warning.called


## Connection.

def test_client_reconnect(client_fx):
    client_fx.disconnect(expected=True)
    assert not client_fx.connected

    client_fx.connect(reconnect=True)
    assert client_fx.connected

@mark.slow
def test_client_unexpected_disconnect_reconnect(client_fx):
    client_fx._reconnect_delay = Mock(return_value=0)
    client_fx.disconnect(expected=False)
    assert client_fx._reconnect_delay.called

    time.sleep(0.1)
    assert client_fx.connected

def test_client_unexpected_reconnect_give_up(client_fx):
    client_fx.RECONNECT_ON_ERROR = False
    client_fx.disconnect(expected=False)
    assert not client_fx.connected

@mark.slow
def test_client_unexpected_disconnect_reconnect_delay(client_fx):
    client_fx._reconnect_delay = Mock(return_value=1)
    client_fx.disconnect(expected=False)

    assert not client_fx.connected
    time.sleep(1.1)
    assert client_fx.connected

def test_client_reconnect_delay_calculation(client_fx):
    client_fx.RECONNECT_DELAYED = False
    assert client_fx._reconnect_delay() == 0

    client_fx.RECONNECT_DELAYED = True
    for expected_delay in client_fx.RECONNECT_DELAYS:
        delay = client_fx._reconnect_delay()
        assert delay == expected_delay

        client_fx._reconnect_attempts += 1

    assert client_fx._reconnect_delay() == client_fx.RECONNECT_DELAYS[-1]

def test_client_disconnect_on_connect(client_fx):
    client_fx.disconnect = Mock()

    client_fx.connect('mock://local', 1337)
    assert client_fx.connected
    assert client_fx.disconnect.called

@with_client(connected=False)
def test_client_connect_invalid_params(client_fx):
    with raises(ValueError):
        client_fx.connect()
    with raises(ValueError):
        client_fx.connect(port=1337)

@mark.slow
def test_client_timeout(client_fx):
    client_fx.on_data_error = Mock()
    time.sleep(pydle.client.PING_TIMEOUT + 1)

    assert client_fx.on_data_error.called
    assert isinstance(client_fx.on_data_error.call_args[0][0], TimeoutError)

def test_client_server_tag(client_fx):
    ev = MockEventLoop()
    assert client_fx.server_tag is None

    client_fx.connect('Mock.local', 1337, eventloop=ev)
    assert client_fx.server_tag == 'mock'
    client_fx.disconnect()

    client_fx.connect('irc.mock.local', 1337, eventloop=ev)
    assert client_fx.server_tag == 'mock'
    client_fx.disconnect()

    client_fx.connect('mock', 1337, eventloop=ev)
    assert client_fx.server_tag == 'mock'
    client_fx.disconnect()

    client_fx.connect('127.0.0.1', 1337, eventloop=ev)
    assert client_fx.server_tag == '127.0.0.1'

    client_fx.network = 'MockNet'
    assert client_fx.server_tag == 'mocknet'
    client_fx.disconnect()


## Messages.

def test_client_message(client_fx):
    client_fx.on_raw_install = Mock()
    server.send('INSTALL', 'gentoo')
    assert client_fx.on_raw_install.called

    message = client_fx.on_raw_install.call_args[0][0]
    assert isinstance(message, pydle.protocol.Message)
    assert message.command == 'INSTALL'
    assert message.params == ('gentoo',)

def test_client_unknown(client_fx):
    client_fx.on_unknown = Mock()
    server.send('INSTALL', 'gentoo')
    assert client_fx.on_unknown.called
