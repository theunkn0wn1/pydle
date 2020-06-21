import attr
from typing import Optional


@attr.s
class User:
    """ Some IRC user """
    nickname = attr.ib(type=str)
    username = attr.ib(type=Optional[str], default=None)
    realname = attr.ib(type=Optional[str], default=None)
    hostname = attr.ib(type=Optional[str], default=None)
