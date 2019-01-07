def test_client_fx_same_nick(client_fx):
    assert client_fx.is_same_nick('WiZ', 'WiZ')
    assert not client_fx.is_same_nick('WiZ', 'jilles')
    assert not client_fx.is_same_nick('WiZ', 'wiz')


def test_user_creation(client_fx):
    client_fx._create_user('WiZ')
    assert 'WiZ' in client_fx.users
    assert client_fx.users['WiZ']['nickname'] == 'WiZ'


def test_user_invalid_creation(client_fx):
    client_fx._create_user('irc.fbi.gov')
    assert 'irc.fbi.gov' not in client_fx.users


def test_user_renaming(client_fx):
    client_fx._create_user('WiZ')
    client_fx._rename_user('WiZ', 'jilles')

    assert 'WiZ' not in client_fx.users
    assert 'jilles' in client_fx.users
    assert client_fx.users['jilles']['nickname'] == 'jilles'


def test_user_renaming_creation(client_fx):
    client_fx._rename_user('null', 'WiZ')

    assert 'WiZ' in client_fx.users
    assert 'null' not in client_fx.users


def test_user_renaming_invalid_creation(client_fx):
    client_fx._rename_user('null', 'irc.fbi.gov')

    assert 'irc.fbi.gov' not in client_fx.users
    assert 'null' not in client_fx.users


def test_user_renaming_channel_users(client_fx):
    client_fx._create_user('WiZ')
    client_fx._create_channel('#lobby')
    client_fx.channels['#lobby']['users'].add('WiZ')

    client_fx._rename_user('WiZ', 'jilles')
    assert 'WiZ' not in client_fx.channels['#lobby']['users']
    assert 'jilles' in client_fx.channels['#lobby']['users']


def test_user_deletion(client_fx):
    client_fx._create_user('WiZ')
    client_fx._destroy_user('WiZ')

    assert 'WiZ' not in client_fx.users


def test_user_channel_deletion(client_fx):
    client_fx._create_channel('#lobby')
    client_fx._create_user('WiZ')
    client_fx.channels['#lobby']['users'].add('WiZ')

    client_fx._destroy_user('WiZ', '#lobby')
    assert 'WiZ' not in client_fx.users
    assert client_fx.channels['#lobby']['users'] == set()


def test_user_channel_incomplete_deletion(client_fx):
    client_fx._create_channel('#lobby')
    client_fx._create_channel('#foo')
    client_fx._create_user('WiZ')
    client_fx.channels['#lobby']['users'].add('WiZ')
    client_fx.channels['#foo']['users'].add('WiZ')

    client_fx._destroy_user('WiZ', '#lobby')
    assert 'WiZ' in client_fx.users
    assert client_fx.channels['#lobby']['users'] == set()


def test_user_synchronization(client_fx):
    client_fx._create_user('WiZ')
    client_fx._sync_user('WiZ', {'hostname': 'og.irc.developer'})

    assert client_fx.users['WiZ']['hostname'] == 'og.irc.developer'


def test_user_synchronization_creation(client_fx):
    client_fx._sync_user('WiZ', {})
    assert 'WiZ' in client_fx.users


def test_user_invalid_synchronization(client_fx):
    client_fx._sync_user('irc.fbi.gov', {})
    assert 'irc.fbi.gov' not in client_fx.users


def test_user_mask_format(client_fx):
    client_fx._create_user('WiZ')
    assert client_fx._format_user_mask('WiZ') == 'WiZ!*@*'

    client_fx._sync_user('WiZ', {'username': 'wiz'})
    assert client_fx._format_user_mask('WiZ') == 'WiZ!wiz@*'

    client_fx._sync_user('WiZ', {'hostname': 'og.irc.developer'})
    assert client_fx._format_user_mask('WiZ') == 'WiZ!wiz@og.irc.developer'

    client_fx._sync_user('WiZ', {'username': None})
    assert client_fx._format_user_mask('WiZ') == 'WiZ!*@og.irc.developer'
