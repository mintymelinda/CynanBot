from datetime import datetime

from .absChannelPointRedemption import AbsChannelPointRedemption
from ..crowdControl.actions.buttonPressCrowdControlAction import ButtonPressCrowdControlAction
from ..crowdControl.actions.crowdControlButton import CrowdControlButton
from ..crowdControl.actions.gameShuffleCrowdControlAction import GameShuffleCrowdControlAction
from ..crowdControl.crowdControlMachineInterface import CrowdControlMachineInterface
from ..crowdControl.idGenerator.crowdControlIdGeneratorInterface import CrowdControlIdGeneratorInterface
from ..crowdControl.mapper.crowdControlInputTypeMapperInterface import CrowdControlInputTypeMapperInterface
from ..crowdControl.utils.crowdControlUserInputUtilsInterface import CrowdControlUserInputUtilsInterface
from ..location.timeZoneRepositoryInterface import TimeZoneRepositoryInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchChannel import TwitchChannel
from ..twitch.configuration.twitchChannelPointsMessage import TwitchChannelPointsMessage
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.crowdControl.crowdControlInputType import CrowdControlInputType
from ..users.userIdsRepositoryInterface import UserIdsRepositoryInterface


class CrowdControlPointRedemption(AbsChannelPointRedemption):

    def __init__(
        self,
        crowdControlIdGenerator: CrowdControlIdGeneratorInterface,
        crowdControlInputTypeMapper: CrowdControlInputTypeMapperInterface,
        crowdControlMachine: CrowdControlMachineInterface,
        crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface,
        timber: TimberInterface,
        timeZoneRepository: TimeZoneRepositoryInterface,
        twitchUtils: TwitchUtilsInterface,
        userIdsRepository: UserIdsRepositoryInterface
    ):
        if not isinstance(crowdControlIdGenerator, CrowdControlIdGeneratorInterface):
            raise TypeError(f'crowdControlIdGenerator argument is malformed: \"{crowdControlIdGenerator}\"')
        elif not isinstance(crowdControlInputTypeMapper, CrowdControlInputTypeMapperInterface):
            raise TypeError(f'crowdControlBoosterPackMapper argument is malformed: \"{crowdControlInputTypeMapper}\"')
        elif not isinstance(crowdControlMachine, CrowdControlMachineInterface):
            raise TypeError(f'crowdControlMachine argument is malformed: \"{crowdControlMachine}\"')
        elif not isinstance(crowdControlUserInputUtils, CrowdControlUserInputUtilsInterface):
            raise TypeError(f'crowdControlUserInputUtils argument is malformed: \"{crowdControlUserInputUtils}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(timeZoneRepository, TimeZoneRepositoryInterface):
            raise TypeError(f'timeZoneRepository argument is malformed: \"{timeZoneRepository}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(userIdsRepository, UserIdsRepositoryInterface):
            raise TypeError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__crowdControlIdGenerator: CrowdControlIdGeneratorInterface = crowdControlIdGenerator
        self.__crowdControlInputTypeMapper: CrowdControlInputTypeMapperInterface = crowdControlInputTypeMapper
        self.__crowdControlMachine: CrowdControlMachineInterface = crowdControlMachine
        self.__crowdControlUserInputUtils: CrowdControlUserInputUtilsInterface = crowdControlUserInputUtils
        self.__timber: TimberInterface = timber
        self.__timeZoneRepository: TimeZoneRepositoryInterface = timeZoneRepository
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__userIdsRepository: UserIdsRepositoryInterface = userIdsRepository

    async def handlePointRedemption(
        self,
        twitchChannel: TwitchChannel,
        twitchChannelPointsMessage: TwitchChannelPointsMessage
    ) -> bool:
        twitchUser = twitchChannelPointsMessage.getTwitchUser()
        if not twitchUser.isCrowdControlEnabled:
            return False

        boosterPacks = twitchUser.crowdControlBoosterPacks
        if boosterPacks is None or len(boosterPacks) == 0:
            return False

        boosterPack = boosterPacks.get(twitchChannelPointsMessage.getRewardId(), None)
        if boosterPack is None:
            return False

        now = datetime.now(self.__timeZoneRepository.getDefault())
        actionId = await self.__crowdControlIdGenerator.generateActionId()
        twitchChannelId = await self.__userIdsRepository.requireUserId(twitchUser.getHandle())

        if boosterPack.inputType is CrowdControlInputType.GAME_SHUFFLE:
            self.__crowdControlMachine.submitAction(GameShuffleCrowdControlAction(
                dateTime = now,
                actionId = actionId,
                chatterUserId = twitchChannelPointsMessage.getUserId(),
                chatterUserName = twitchChannelPointsMessage.getUserName(),
                twitchChannel = twitchUser.getHandle(),
                twitchChannelId = twitchChannelId
            ))

            self.__timber.log('CrowdControlPointRedemption', f'Created new game shuffle crowd control action from channel point redemption ({twitchChannelPointsMessage=})')
            return True

        button: CrowdControlButton | None

        if boosterPack.inputType is CrowdControlInputType.USER_INPUT_BUTTON:
            button = await self.__crowdControlUserInputUtils.parseButtonFromUserInput(
                userInput = twitchChannelPointsMessage.getRedemptionMessage()
            )
        else:
            button = await self.__crowdControlInputTypeMapper.toButton(
                inputType = boosterPack.inputType
            )

        if button is None:
            self.__timber.log('CrowdControlPointRedemption', f'Unable to create crowd control action from channel point redemption ({twitchChannelPointsMessage=}) ({button=})')
            return False

        self.__crowdControlMachine.submitAction(ButtonPressCrowdControlAction(
            button = button,
            dateTime = now,
            actionId = actionId,
            chatterUserId = twitchChannelPointsMessage.getUserId(),
            chatterUserName = twitchChannelPointsMessage.getUserName(),
            twitchChannel = twitchUser.getHandle(),
            twitchChannelId = twitchChannelId
        ))

        self.__timber.log('CrowdControlPointRedemption', f'Created new button press crowd control action from channel point redemption ({twitchChannelPointsMessage=}) ({button=})')
        return True