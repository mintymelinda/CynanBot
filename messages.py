from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone

from twitchio import Message

import CynanBotCommon.utils as utils
from CynanBotCommon.chatBand.chatBandManager import ChatBandManager
from CynanBotCommon.chatLogger.chatLogger import ChatLogger
from CynanBotCommon.timber.timber import Timber
from CynanBotCommon.timedDict import TimedDict
from generalSettingsRepository import GeneralSettingsRepository
from twitch.twitchUtils import TwitchUtils
from users.user import User


class AbsMessage(ABC):

    @abstractmethod
    async def handleMessage(self, twitchUser: User, message: Message) -> bool:
        pass


class CatJamMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchUtils: TwitchUtils,
        catJamMessage: str = 'catJAM',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not utils.isValidStr(catJamMessage):
            raise ValueError(f'catJamMessage argument is malformed: \"{catJamMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__catJamMessage: str = catJamMessage
        self.__lastCatJamMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, twitchUser: User, message: Message) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isCatJamMessageEnabled():
            return False
        elif not twitchUser.isCatJamMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.content)

        if self.__catJamMessage in splits and self.__lastCatJamMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await self.__twitchUtils.safeSend(message.channel, self.__catJamMessage)
            self.__timber.log('CatJamMessage', f'Handled catJAM message for {message.author.name} in {twitchUser.getHandle()}')
            return True

        return False


class ChatBandMessage(AbsMessage):

    def __init__(
        self,
        chatBandManager: ChatBandManager,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber
    ):
        if not isinstance(chatBandManager, ChatBandManager):
            raise ValueError(f'chatBandManager argument is malformed: \"{chatBandManager}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__chatBandManager: ChatBandManager = chatBandManager
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber

    async def handleMessage(self, twitchUser: User, message: Message) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isChatBandEnabled():
            return False
        elif not twitchUser.isChatBandEnabled():
            return False

        if await self.__chatBandManager.playInstrumentForMessage(
            twitchChannel = twitchUser.getHandle(),
            author = message.author.name,
            message = utils.cleanStr(message.content)
        ):
            self.__timber.log('ChatBandMessage', f'Handled chat band message for {message.author.name} in {twitchUser.getHandle()}')
            return True

        return False


class ChatLogMessage(AbsMessage):

    def __init__(
        self,
        chatLogger: ChatLogger
    ):
        if not isinstance(chatLogger, ChatLogger):
            raise ValueError(f'chatLogger argument is malformed: \"{chatLogger}\"')

        self.__chatLogger: ChatLogger = chatLogger

    async def handleMessage(self, twitchUser: User, message: Message) -> bool:
        if not twitchUser.isChatLoggingEnabled():
            return False

        self.__chatLogger.logMessage(
            twitchChannel = twitchUser.getHandle(),
            userId = str(message.author.id),
            userName = message.author.name,
            msg = utils.cleanStr(message.content)
        )

        return True


class CynanMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchUtils: TwitchUtils,
        cynanUserName: str = 'CynanMachae',
        cooldown: timedelta = timedelta(days = 3)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not utils.isValidStr(cynanUserName):
            raise ValueError(f'cynanUserName argument is malformed: \"{cynanUserName}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__cynanUserName: str = cynanUserName
        self.__cooldown: timedelta = cooldown
        self.__lastCynanMessageTime = datetime.now(timezone.utc) - cooldown

    async def handleMessage(self, twitchUser: User, message: Message) -> bool:
        if twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif message is None:
            raise ValueError(f'message argument is malformed: \"{message}\"')

        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isCynanMessageEnabled():
            return False
        elif not twitchUser.isCynanMessageEnabled():
            return False
        elif message.author.name.lower() != self.__cynanUserName.lower():
            return False

        now = datetime.now(timezone.utc)

        if now > self.__lastCynanMessageTime + self.__cooldown:
            self.__lastCynanMessageTime = now
            await self.__twitchUtils.safeSend(message.channel, f'/me waves to @{self.__cynanUserName} 👋')
            self.__timber.log('CynanMessage', f'Handled Cynan message for {message.author.name} in {twitchUser.getHandle()}')
            return True

        return False


class DeerForceMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchUtils: TwitchUtils,
        deerForceMessage: str = 'D e e R F o r C e',
        cooldown: timedelta = timedelta(minutes = 30)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not utils.isValidStr(deerForceMessage):
            raise ValueError(f'deerForceMessage argument is malformed: \"{deerForceMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__deerForceMessage: str = deerForceMessage
        self.__lastDeerForceMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, twitchUser: User, message: Message) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isDeerForceMessageEnabled():
            return False
        elif not twitchUser.isDeerForceMessageEnabled():
            return False

        text = utils.cleanStr(message.content)

        if text.lower() == self.__deerForceMessage.lower() and self.__lastDeerForceMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await self.__twitchUtils.safeSend(message.channel, self.__deerForceMessage)
            self.__timber.log('DeerForceMessage', f'Handled Deer Force message for {message.author.name} in {twitchUser.getHandle()}')
            return True

        return False


class EyesMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchUtils: TwitchUtils,
        eyesMessage: str = '👀',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not utils.isValidStr(eyesMessage):
            raise ValueError(f'eyesMessage argument is malformed: \"{eyesMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__eyesMessage: str = eyesMessage
        self.__lastEyesMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, twitchUser: User, message: Message) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isEyesMessageEnabled():
            return False
        elif not twitchUser.isEyesMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.content)

        if self.__eyesMessage in splits and self.__lastEyesMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await self.__twitchUtils.safeSend(message.channel, self.__eyesMessage)
            self.__timber.log('EyesMessage', f'Handled eyes message for {message.author.name} in {twitchUser.getHandle()}')
            return True

        return False


class ImytSlurpMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchUtils: TwitchUtils,
        imytSlurpMessage: str = 'imytSlurp',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not utils.isValidStr(imytSlurpMessage):
            raise ValueError(f'imytSlurpMessage argument is malformed: \"{imytSlurpMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__imytSlurpMessage: str = imytSlurpMessage
        self.__lastImytSlurpMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, twitchUser: User, message: Message) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isImytSlurpMessageEnabled():
            return False
        elif not twitchUser.isImytSlurpEnabled():
            return False

        splits = utils.getCleanedSplits(message.content)

        if self.__imytSlurpMessage in splits and self.__lastImytSlurpMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await self.__twitchUtils.safeSend(message.channel, self.__imytSlurpMessage)
            self.__timber.log('ImytSlurpMessage', f'Handled imytSlurp message for {message.author.name} in {twitchUser.getHandle()}')
            return True

        return False


class JamCatMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchUtils: TwitchUtils,
        jamCatMessage: str = 'jamCAT',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtils):
            raise ValueError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not utils.isValidStr(jamCatMessage):
            raise ValueError(f'jamCatMessage argument is malformed: \"{jamCatMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__jamCatMessage: str = jamCatMessage
        self.__lastCatJamMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(
        self,
        twitchUser: User,
        message: Message
    ) -> bool:
        if twitchUser is None:
            raise ValueError(f'twitchUser argument is malformed: \"{twitchUser}\"')
        elif message is None:
            raise ValueError(f'message argument is malformed: \"{message}\"')

        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isJamCatMessageEnabled():
            return False
        elif not twitchUser.isJamCatMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.content)

        if self.__jamCatMessage in splits and self.__lastCatJamMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await self.__twitchUtils.safeSend(message.channel, self.__jamCatMessage)
            self.__timber.log('JamCatMessage', f'Handled jamCAT message for {message.author.name} in {twitchUser.getHandle()}')
            return True

        return False


class RatJamMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchUtils: TwitchUtils,
        ratJamMessage: str = 'ratJAM',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(ratJamMessage):
            raise ValueError(f'ratJamMessage argument is malformed: \"{ratJamMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__ratJamMessage: str = ratJamMessage
        self.__lastRatJamMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, twitchUser: User, message: Message) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isRatJamMessageEnabled():
            return False
        elif not twitchUser.isRatJamMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.content)

        if self.__ratJamMessage in splits and self.__lastRatJamMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await self.__twitchUtils.safeSend(message.channel, self.__ratJamMessage)
            self.__timber.log('RatJamMessage', f'Handled ratJAM message for {message.author.name} in {twitchUser.getHandle()}')
            return True

        return False


class RoachMessage(AbsMessage):

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        timber: Timber,
        twitchUtils: TwitchUtils,
        roachMessage: str = 'ROACH',
        cooldown: timedelta = timedelta(minutes = 20)
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(timber, Timber):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidStr(roachMessage):
            raise ValueError(f'roachMessage argument is malformed: \"{roachMessage}\"')
        elif not isinstance(cooldown, timedelta):
            raise ValueError(f'cooldown argument is malformed: \"{cooldown}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__timber: Timber = timber
        self.__twitchUtils: TwitchUtils = twitchUtils
        self.__roachMessage: str = roachMessage
        self.__lastMessageTimes: TimedDict = TimedDict(cooldown)

    async def handleMessage(self, twitchUser: User, message: Message) -> bool:
        generalSettings = await self.__generalSettingsRepository.getAllAsync()

        if not generalSettings.isRoachMessageEnabled():
            return False
        elif not twitchUser.isRoachMessageEnabled():
            return False

        splits = utils.getCleanedSplits(message.content)

        if self.__roachMessage in splits and self.__lastMessageTimes.isReadyAndUpdate(twitchUser.getHandle()):
            await self.__twitchUtils.safeSend(message.channel, self.__roachMessage)
            self.__timber.log('RoachMessage', f'Handled {self.__roachMessage} message for {message.author.name} in {twitchUser.getHandle()}')
            return True

        return False


class StubMessage(AbsMessage):

    def __init__(self):
        pass

    async def handleMessage(self, twitchUser: User, message: Message) -> bool:
        return False
