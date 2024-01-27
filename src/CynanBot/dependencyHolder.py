from typing import Optional

from CynanBot.administratorProviderInterface import \
    AdministratorProviderInterface
from CynanBot.backgroundTaskHelper import BackgroundTaskHelper
from CynanBot.chatLogger.chatLoggerInterface import ChatLoggerInterface
from CynanBot.cuteness.cutenessUtilsInterface import CutenessUtilsInterface
from CynanBot.generalSettingsRepository import GeneralSettingsRepository
from CynanBot.sentMessageLogger.sentMessageLoggerInterface import \
    SentMessageLoggerInterface
from CynanBot.soundPlayerHelper.soundPlayerHelperInterface import \
    SoundPlayerHelperInterface
from CynanBot.timber.timberInterface import TimberInterface
from CynanBot.trivia.triviaUtilsInterface import TriviaUtilsInterface
from CynanBot.twitch.twitchPredictionWebsocketUtilsInterface import \
    TwitchPredictionWebsocketUtilsInterface
from CynanBot.twitch.twitchUtilsInterface import TwitchUtilsInterface
from CynanBot.websocketConnection.websocketConnectionServerInterface import \
    WebsocketConnectionServerInterface


class DependencyHolder():

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        backgroundTaskHelper: BackgroundTaskHelper,
        chatLogger: ChatLoggerInterface,
        cutenessUtils: Optional[CutenessUtilsInterface],
        generalSettingsRepository: GeneralSettingsRepository,
        sentMessageLogger: SentMessageLoggerInterface,
        soundPlayerHelper: Optional[SoundPlayerHelperInterface],
        timber: TimberInterface,
        triviaUtils: Optional[TriviaUtilsInterface],
        twitchPredictionWebsocketUtils: Optional[TwitchPredictionWebsocketUtilsInterface],
        twitchUtils: TwitchUtilsInterface,
        websocketConnectionServer: Optional[WebsocketConnectionServerInterface]
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(backgroundTaskHelper, BackgroundTaskHelper):
            raise TypeError(f'backgroundTaskHelper argument is malformed: \"{backgroundTaskHelper}\"')
        elif not isinstance(chatLogger, ChatLoggerInterface):
            raise TypeError(f'chatLogger argument is malformed: \"{chatLogger}\"')
        elif cutenessUtils is not None and not isinstance(cutenessUtils, CutenessUtilsInterface):
            raise TypeError(f'cutenessUtils argument is malformed: \"{cutenessUtils}\"')
        elif not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise TypeError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(sentMessageLogger, SentMessageLoggerInterface):
            raise TypeError(f'sentMessageLogger argument is malformed: \"{sentMessageLogger}\"')
        elif soundPlayerHelper is not None and not isinstance(soundPlayerHelper, SoundPlayerHelperInterface):
            raise TypeError(f'vlcHelper argument is malformed: \"{soundPlayerHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif triviaUtils is not None and not isinstance(triviaUtils, TriviaUtilsInterface):
            raise TypeError(f'triviaUtils argument is malformed: \"{triviaUtils}\"')
        elif twitchPredictionWebsocketUtils is not None and not isinstance(twitchPredictionWebsocketUtils, TwitchPredictionWebsocketUtilsInterface):
            raise TypeError(f'twitchPredictionWebsocketUtils argument is malformed: \"{twitchPredictionWebsocketUtils}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif websocketConnectionServer is not None and not isinstance(websocketConnectionServer, WebsocketConnectionServerInterface):
            raise TypeError(f'websocketConnectionServer argument is malformed: \"{websocketConnectionServer}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__backgroundTaskHelper: BackgroundTaskHelper = backgroundTaskHelper
        self.__chatLogger: ChatLoggerInterface = chatLogger
        self.__cutenessUtils: Optional[CutenessUtilsInterface] = cutenessUtils
        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__sentMessageLogger: SentMessageLoggerInterface = sentMessageLogger
        self.__soundPlayerHelper: Optional[SoundPlayerHelperInterface] = soundPlayerHelper
        self.__timber: TimberInterface = timber
        self.__triviaUtils: Optional[TriviaUtilsInterface] = triviaUtils
        self.__twitchPredictionWebsocketUtils: Optional[TwitchPredictionWebsocketUtilsInterface] = twitchPredictionWebsocketUtils
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__websocketConnectionServer: Optional[WebsocketConnectionServerInterface] = websocketConnectionServer

    def getAdministratorProvider(self) -> AdministratorProviderInterface:
        return self.__administratorProvider

    def getBackgroundTaskHelper(self) -> BackgroundTaskHelper:
        return self.__backgroundTaskHelper

    def getChatLogger(self) -> ChatLoggerInterface:
        return self.__chatLogger

    def getCutenessUtils(self) -> Optional[CutenessUtilsInterface]:
        return self.__cutenessUtils

    def getGeneralSettingsRepository(self) -> GeneralSettingsRepository:
        return self.__generalSettingsRepository

    def getSentMessageLogger(self) -> SentMessageLoggerInterface:
        return self.__sentMessageLogger

    def getSoundPlayerHelper(self) -> Optional[SoundPlayerHelperInterface]:
        return self.__soundPlayerHelper

    def getTimber(self) -> TimberInterface:
        return self.__timber

    def getTriviaUtils(self) -> Optional[TriviaUtilsInterface]:
        return self.__triviaUtils

    def getTwitchPredictionWebsocketUtils(self) -> Optional[TwitchPredictionWebsocketUtilsInterface]:
        return self.__twitchPredictionWebsocketUtils

    def getTwitchUtils(self) -> TwitchUtilsInterface:
        return self.__twitchUtils

    def getWebsocketConnectionServer(self) -> Optional[WebsocketConnectionServerInterface]:
        return self.__websocketConnectionServer
