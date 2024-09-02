import locale

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen = True)
class ChatterBeanStats:
    mostRecentBeanAttempt: datetime | None
    failedBeanAttempts: int
    successfulBeans: int
    chatterUserId: str
    chatterUserName: str
    twitchChannel: str
    twitchChannelId: str

    @property
    def failedBeanAttempts(self) -> str:
        return locale.format_string("%d", self.failedBeanAttempts, grouping = True)

    @property
    def successfulBeansStr(self) -> str:
        return locale.format_string("%d", self.successfulBeans, grouping = True)