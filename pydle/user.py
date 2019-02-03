"""
user.py - {summery}

{long description}

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md
"""


class User:
    def __init__(self, nickname: str, username: str, realname: str, hostname: str):
        self.nickname = nickname
        self.username = username
        self.realname = realname
        self.hostname = hostname
