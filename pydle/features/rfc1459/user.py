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

    __slots__ = ['away', 'away_message', 'except_list', 'invite_except_list']

    def __init__(self, away: bool, away_message: Optional[str], **kwargs):
        """
        RFC user constructor

        Args:
            away (bool): is this user marked away?
            away_message (Optional[str]): away message, if it is set
            **kwargs (Dict): arguments passed to base User constructor
        """
        super().__init__(**kwargs)
        self.away = away
        self.away_message = away_message
