from abc import ABC, abstractmethod

from frozenlist import FrozenList

from ..absCheerAction import AbsCheerAction
from ...users.userInterface import UserInterface


class SoundAlertCheerActionHelperInterface(ABC):

    @abstractmethod
    async def handleSoundAlertCheerAction(
        self,
        actions: FrozenList[AbsCheerAction],
        bits: int,
        broadcasterUserId: str,
        cheerUserId: str,
        cheerUserName: str,
        message: str,
        moderatorTwitchAccessToken: str,
        moderatorUserId: str,
        userTwitchAccessToken: str,
        user: UserInterface
    ) -> bool:
        pass
