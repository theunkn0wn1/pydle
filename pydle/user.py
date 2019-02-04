"""
user.py - {summery}

{long description}

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md
"""


class User:
    """
    Base user object, represents an IRC user
    """

    # define our data members, this saves on memory and improves performance
    __slots__ = ['nickname', 'username', 'realname', 'hostname']
    def __init__(self, nickname: str, username: str, realname: str, hostname: str):
        """
        constructs a new User.

        Args:
            nickname (str): user's nickname
            username (str): user's username
            realname (str): user's real name
            hostname (str): user's host mask
        """
        self.nickname = nickname
        self.username = username
        self.realname = realname
        self.hostname = hostname
