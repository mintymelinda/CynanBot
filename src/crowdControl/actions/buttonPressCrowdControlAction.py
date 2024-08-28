from datetime import datetime

from .crowdControlAction import CrowdControlAction
from .crowdControlActionType import CrowdControlActionType
from .crowdControlButton import CrowdControlButton


class ButtonPressCrowdControlAction(CrowdControlAction):

    def __init__(
        self,
        button: CrowdControlButton,
        dateTime: datetime,
        actionId: str,
        chatterUserId: str,
        chatterUserName: str,
        twitchChannel: str,
        twitchChannelId: str
    ):
        super().__init__(
            dateTime = dateTime,
            actionId = actionId,
            chatterUserId = chatterUserId,
            chatterUserName = chatterUserName,
            twitchChannel = twitchChannel,
            twitchChannelId = twitchChannelId
        )

        if not isinstance(button, CrowdControlButton):
            raise TypeError(f'button argument is malformed: \"{button}\"')

        self.__button: CrowdControlButton = button

    def actionType(self) -> CrowdControlActionType:
        return CrowdControlActionType.BUTTON_PRESS

    def button(self) -> CrowdControlButton:
        return self.__button
