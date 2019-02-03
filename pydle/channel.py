"""
channel.py - {summery}

{long description}

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md
"""
from typing import Set

from .user import User


class Channel:
    """
    Represents an individual channel
    """

    def __init__(self, title: str, users: Set[User]):
        self._users = users if users else set()
        self._name = title

    @property
    def users(self) -> Set[User]:
        return self._users

    @users.setter
    def users(self, value: Set[User]):
        self._users = value

    @property
    def name(self):
        return self._name
