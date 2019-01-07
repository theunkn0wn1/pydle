"""
test_bot.py - {summery}

{long description}

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md
"""

from logging import getLogger

from pydle import Client

LOG = getLogger("{}".format(__name__))

SASL_USER = "pydle[test_bot]"
SASL_PASS = "tests"
SASL_IDENT = "pydle"


class TestSetupClient(Client):
    """
    Small client fixture to setup an account on the irc server
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(nickname=SASL_USER, *args, **kwargs)

    async def on_connect(self):
        await self.message("nickserv", "REGISTER {} pydle@example.com".format(SASL_PASS))
        await self.disconnect(expected=True)


class TestClient(Client):
    """
    The actual test client, preconfigured to connect via sasl
    """
    def __init__(self, **kwargs):
        super().__init__(nickname=SASL_USER,
                         sasl_username=SASL_USER,
                         sasl_identity=SASL_IDENT,
                         sasl_password=SASL_PASS,
                         **kwargs
                         )
