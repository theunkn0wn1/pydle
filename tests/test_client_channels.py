def test_client_same_channel(client_fx):
    assert client_fx.is_same_channel('#lobby', '#lobby')
    assert not client_fx.is_same_channel('#lobby', '#support')
    assert not client_fx.is_same_channel('#lobby', 'jilles')


def test_client_in_channel(client_fx):
    client_fx._create_channel('#lobby')
    assert client_fx.in_channel('#lobby')


def test_client_is_channel(client_fx):
    # Test always true...
    assert client_fx.is_channel('#lobby')
    assert client_fx.is_channel('WiZ')
    assert client_fx.is_channel('irc.fbi.gov')


def test_channel_creation(client_fx):
    client_fx._create_channel('#pydle')
    assert '#pydle' in client_fx.channels
    assert client_fx.channels['#pydle']['users'] == set()


def test_channel_destruction(client_fx):
    client_fx._create_channel('#pydle')
    client_fx._destroy_channel('#pydle')
    assert '#pydle' not in client_fx.channels


def test_channel_user_destruction(client_fx):
    client_fx._create_channel('#pydle')
    client_fx._create_user('WiZ')
    client_fx.channels['#pydle']['users'].add('WiZ')

    client_fx._destroy_channel('#pydle')
    assert '#pydle' not in client_fx.channels
    assert 'WiZ' not in client_fx.users
