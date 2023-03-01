from twitchio.ext.pubsub.topics import Topic

import CynanBotCommon.utils as utils


class PubSubEntry():

    def __init__(self, userId: int, userName: str, topic: Topic):
        if not utils.isValidInt(userId):
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif not isinstance(topic, Topic):
            raise ValueError(f'topic argument is malformed: \"{topic}\"')

        self.__userId: int = userId
        self.__userName: str = userName
        self.__topic: Topic = topic

    def getTopic(self) -> Topic:
        return self.__topic

    def getUserId(self) -> int:
        return self.__userId

    def getUserName(self) -> str:
        return self.__userName
