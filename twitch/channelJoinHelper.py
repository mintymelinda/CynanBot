import asyncio
import random
from typing import List, Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.backgroundTaskHelper import BackgroundTaskHelper
from CynanBotCommon.timber.timber import Timber
from twitch.channelJoinListener import ChannelJoinListener
from twitch.finishedJoiningChannelsEvent import FinishedJoiningChannelsEvent
from twitch.joinChannelsEvent import JoinChannelsEvent
from users.usersRepository import UsersRepository


class ChannelJoinHelper():

    def __init__(
        self,
        backgroundTaskHelper: BackgroundTaskHelper,
        timber: Timber,
        usersRepository: UsersRepository,
        sleepTimeSeconds: float = 16,
        maxChannelsToJoin: int = 10
    ):
        if not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise ValueError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')
        elif not utils.isValidNum(sleepTimeSeconds):
            raise ValueError(f'sleepTimeSeconds argument is malformed: \"{sleepTimeSeconds}\"')
        elif sleepTimeSeconds < 12 or sleepTimeSeconds > 60:
            raise ValueError(f'sleepTimeSeconds argument is out of bounds: {sleepTimeSeconds}')
        elif not utils.isValidInt(maxChannelsToJoin):
            raise ValueError(f'maxChannelsToJoin argument is malformed: \"{maxChannelsToJoin}\"')
        elif maxChannelsToJoin < 3 or maxChannelsToJoin > 10:
            raise ValueError(f'maxChannelsToJoin argument is out of bounds: {maxChannelsToJoin}')

        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__timber: Timber = timber
        self.__usersRepository: UsersRepository = usersRepository
        self.__sleepTimeSeconds: float = sleepTimeSeconds
        self.__maxChannelsToJoin: int = maxChannelsToJoin

        self.__channelJoinListener: Optional[ChannelJoinListener] = None
        self.__isJoiningChannels: bool = False

    def joinChannels(self):
        if self.__isJoiningChannels:
            self.__timber.log('ChannelJoinHelper', 'Not starting channel join process as it has already been started!')
            return

        self.__isJoiningChannels = True
        self.__timber.log('ChannelJoinHelper', f'Starting channel join process...')
        self.__backgroundTaskHelper.createTask(self.__joinChannels())

    async def __joinChannels(self):
        channelJoinListener = self.__channelJoinListener

        if channelJoinListener is None:
            raise RuntimeError(f'channelJoinListener has not been set: \"{channelJoinListener}\"')

        allChannels: List[str] = list()
        users = await self.__usersRepository.getUsersAsync()

        for user in users:
            allChannels.append(user.getHandle())

        if len(allChannels) == 0:
            self.__timber.log('ChannelJoinHelper', f'There are no channels to join')
            self.__isJoiningChannels = False
            return

        allChannels.sort(key = lambda userHandle: userHandle.lower())
        self.__timber.log('ChannelJoinHelper', f'Will be joining a total of {len(allChannels)} channel(s)...')

        workingChannels: List[str] = list()
        workingChannels.extend(allChannels)

        while len(workingChannels) >= 1:
            newChannelsToJoin: List[str] = list()

            while len(workingChannels) >= 1 and len(newChannelsToJoin) < self.__maxChannelsToJoin - 1:
                userHandle = random.choice(workingChannels)
                workingChannels.remove(userHandle)
                newChannelsToJoin.append(userHandle)

            newChannelsToJoin.sort(key = lambda userHandle: userHandle.lower())

            await channelJoinListener.onNewChannelJoinEvent(JoinChannelsEvent(
                channels = newChannelsToJoin
            ))

            await asyncio.sleep(self.__sleepTimeSeconds)

        await channelJoinListener.onNewChannelJoinEvent(FinishedJoiningChannelsEvent(
            allChannels = allChannels
        ))

        self.__timber.log('ChannelJoinHelper', f'Finished joining {len(allChannels)} channel(s)')
        self.__isJoiningChannels = False

    def setChannelJoinListener(self, listener: Optional[ChannelJoinListener]):
        if listener is not None and not isinstance(listener, ChannelJoinListener):
            raise ValueError(f'listener argument is malformed: \"{listener}\"')

        self.__channelJoinListener = listener