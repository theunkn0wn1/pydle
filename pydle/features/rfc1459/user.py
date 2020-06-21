from pydle.user import User
import attr
from typing import Optional, List


@attr.s
class RFC1459User(User):
    away = attr.ib(type=bool, default=False)
    away_message = attr.ib(type=Optional[str], default=None)
    modes = attr.ib(type=List[str], factory=list)
