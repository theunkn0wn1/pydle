"""
channel.py - {summery}

{long description}

Copyright (c) 2018 The Fuel Rats Mischief,
All rights reserved.

Licensed under the BSD 3-Clause License.

See LICENSE.md
"""
from datetime import datetime
from typing import Set, List

from pydle.channel import Channel
from pydle.user import User


class RfcChannel(Channel):
    """
    A channel defined under RFC1459
    """

    def __init__(self,
                 title: str,
                 users: Set[User] = None,
                 modes: List[str] = None,
                 topic: str = None,
                 topic_by: str = None,
                 created: datetime = None,
                 password: str = None,
                 ban_list: List = None,
                 public: bool = None
                 ):
        self.modes = modes if modes else set()
        self.topic = topic
        self.topic_by = topic_by
        self.created = created
        self.password = password
        self.ban_list = ban_list
        self.public = public

        super().__init__(title, users)
