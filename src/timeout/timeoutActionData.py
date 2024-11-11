from dataclasses import dataclass

from ..users.userInterface import UserInterface


@dataclass(frozen = True)
class TimeoutActionData:
    bits: int | None
    durationSeconds: int
    chatMessage: str | None
    instigatorUserId: str
    instigatorUserName: str
    moderatorTwitchAccessToken: str
    moderatorUserId: str
    pointRedemptionEventId: str | None
    pointRedemptionMessage: str | None
    pointRedemptionRewardId: str | None
    timeoutTargetUserId: str
    timeoutTargetUserName: str
    twitchChannelId: str
    twitchChatMessageId: str | None
    userTwitchAccessToken: str
    user: UserInterface