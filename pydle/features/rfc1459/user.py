"""
user.py - {summery}

{long description}

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md
"""
from typing import Optional

from pydle.user import User


class RfcUser(User):
    """
    A RFC 1459 user object
    """

    def __init__(self, away: bool, away_message: Optional[str], **kwargs):
        super().__init__(**kwargs)
        self.away = away
        self.away_message = away_message
