from abc import ABC, abstractmethod
from typing import Any

from CynanBot.transparent.transparentResponse import TransparentResponse


class TransparentXmlMapperInterface(ABC):

    @abstractmethod
    async def parseTransparentResponse(
        self,
        xmlContents: dict[str, Any] | Any | None
    ) -> TransparentResponse | None:
        pass