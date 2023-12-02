from typing import Any, Dict, Optional

import CynanBot.misc.utils as utils
from CynanBot.misc.simpleDateTime import SimpleDateTime
from CynanBot.twitch.websocket.websocketConnectionStatus import \
    WebsocketConnectionStatus


class WebsocketSession():

    def __init__(
        self,
        keepAliveTimeoutSeconds: int,
        connectedAt: SimpleDateTime,
        reconnectUrl: Optional[str],
        sessionId: str,
        status: Optional[WebsocketConnectionStatus]
    ):
        if not utils.isValidInt(keepAliveTimeoutSeconds):
            raise ValueError(f'keepAliveTimeoutSeconds argument is malformed: \"{keepAliveTimeoutSeconds}\"')
        elif not isinstance(connectedAt, SimpleDateTime):
            raise ValueError(f'connectedAt argument is malformed: \"{connectedAt}\"')
        elif reconnectUrl is not None and not utils.isValidUrl(reconnectUrl):
            raise ValueError(f'reconnectUrl argument is malformed: \"{reconnectUrl}\"')
        elif not utils.isValidStr(sessionId):
            raise ValueError(f'sessionId argument is malformed: \"{sessionId}\"')
        elif status is not None and not isinstance(status, WebsocketConnectionStatus):
            raise ValueError(f'status argument is malformed: \"{status}\"')

        self.__keepAliveTimeoutSeconds: int = keepAliveTimeoutSeconds
        self.__connectedAt: SimpleDateTime = connectedAt
        self.__reconnectUrl: Optional[str] = reconnectUrl
        self.__sessionId: str = sessionId
        self.__status: Optional[WebsocketConnectionStatus] = status

    def getConnectedAt(self) -> SimpleDateTime:
        return self.__connectedAt

    def getKeepAliveTimeoutSeconds(self) -> int:
        return self.__keepAliveTimeoutSeconds

    def getReconnectUrl(self) -> Optional[str]:
        return self.__reconnectUrl

    def getSessionId(self) -> str:
        return self.__sessionId

    def getStatus(self) -> Optional[WebsocketConnectionStatus]:
        return self.__status

    def __repr__(self) -> str:
        dictionary = self.toDictionary()
        return str(dictionary)

    def toDictionary(self) -> Dict[str, Any]:
        return {
            'connectedAt': self.__connectedAt,
            'keepAliveTimeoutSeconds': self.__keepAliveTimeoutSeconds,
            'reconnectUrl': self.__reconnectUrl,
            'sessionId': self.__sessionId,
            'status': self.__status
        }
