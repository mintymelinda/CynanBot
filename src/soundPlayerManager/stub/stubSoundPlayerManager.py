from typing import Collection

from ..soundAlert import SoundAlert
from ..soundPlayerManagerInterface import SoundPlayerManagerInterface


class StubSoundPlayerManager(SoundPlayerManagerInterface):

    async def isPlaying(self) -> bool:
        return False

    async def playPlaylist(
        self,
        filePaths: Collection[str],
        volume: int | None = None
    ) -> bool:
        return False

    async def playSoundAlert(
        self,
        alert: SoundAlert,
        volume: int | None = None
    ) -> bool:
        return False

    async def playSoundFile(
        self,
        filePath: str | None,
        volume: int | None = None
    ) -> bool:
        return False