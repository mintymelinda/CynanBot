import traceback

from .absChatCommand import AbsChatCommand
from ..cheerActions.cheerActionsRepositoryInterface import CheerActionsRepositoryInterface
from ..cheerActions.editCheerActionResult.alreadyDisabledEditCheerActionResult import \
    AlreadyDisabledEditCheerActionResult
from ..cheerActions.editCheerActionResult.notFoundEditCheerActionResult import NotFoundEditCheerActionResult
from ..cheerActions.editCheerActionResult.successfullyDisabledEditCheerActionResult import \
    SuccessfullyDisabledEditCheerActionResult
from ..misc import utils as utils
from ..misc.administratorProviderInterface import AdministratorProviderInterface
from ..timber.timberInterface import TimberInterface
from ..twitch.configuration.twitchContext import TwitchContext
from ..twitch.twitchUtilsInterface import TwitchUtilsInterface
from ..users.usersRepositoryInterface import UsersRepositoryInterface


class DisableCheerActionChatCommand(AbsChatCommand):

    def __init__(
        self,
        administratorProvider: AdministratorProviderInterface,
        cheerActionsRepository: CheerActionsRepositoryInterface,
        timber: TimberInterface,
        twitchUtils: TwitchUtilsInterface,
        usersRepository: UsersRepositoryInterface
    ):
        if not isinstance(administratorProvider, AdministratorProviderInterface):
            raise TypeError(f'administratorProvider argument is malformed: \"{administratorProvider}\"')
        elif not isinstance(cheerActionsRepository, CheerActionsRepositoryInterface):
            raise TypeError(f'cheerActionsRepository argument is malformed: \"{cheerActionsRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(twitchUtils, TwitchUtilsInterface):
            raise TypeError(f'twitchUtils argument is malformed: \"{twitchUtils}\"')
        elif not isinstance(usersRepository, UsersRepositoryInterface):
            raise TypeError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__administratorProvider: AdministratorProviderInterface = administratorProvider
        self.__cheerActionsRepository: CheerActionsRepositoryInterface = cheerActionsRepository
        self.__timber: TimberInterface = timber
        self.__twitchUtils: TwitchUtilsInterface = twitchUtils
        self.__usersRepository: UsersRepositoryInterface = usersRepository

    async def handleChatCommand(self, ctx: TwitchContext):
        user = await self.__usersRepository.getUserAsync(ctx.getTwitchChannelName())
        userId = await ctx.getTwitchChannelId()
        administrator = await self.__administratorProvider.getAdministratorUserId()

        if userId != ctx.getAuthorId() and administrator != ctx.getAuthorId():
            self.__timber.log('DisableCheerActionChatCommand', f'{ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried using this command!')
            return
        elif not user.areCheerActionsEnabled:
            return

        splits = utils.getCleanedSplits(ctx.getMessageContent())
        if len(splits) < 2:
            await self.__twitchUtils.safeSend(ctx, f'⚠ A bits amount is necessary for the !disablecheeraction command. Example: !disablecheeraction 100')
            return

        bitsString: str | None = splits[1]
        try:
            bits = int(bitsString)
        except Exception as e:
            self.__timber.log('DisableCheerActionChatCommand', f'Bits amount given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is malformed ({bitsString=}): {e}', e, traceback.format_exc())
            await self.__twitchUtils.safeSend(ctx, f'⚠ Bits amount argument is malformed. Example: !disablecheeraction 100')
            return

        if bits < 1 or bits > utils.getIntMaxSafeSize():
            self.__timber.log('DisableCheerActionChatCommand', f'Bits amount given by {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} is out of bounds ({bitsString=} ({bits=})')
            await self.__twitchUtils.safeSend(ctx, f'⚠ Bits amount argument is out of bounds. Example: !disablecheeraction 100')
            return

        result = await self.__cheerActionsRepository.disableAction(
            bits = bits,
            twitchChannelId = userId
        )

        if isinstance(result, AlreadyDisabledEditCheerActionResult):
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Cheer action {bits} is already disabled: {result.cheerAction.printOut()}')
        elif isinstance(result, NotFoundEditCheerActionResult):
            await self.__twitchUtils.safeSend(ctx, f'⚠ Found no corresponding cheer action for bit amount {bits}')
        elif isinstance(result, SuccessfullyDisabledEditCheerActionResult):
            await self.__twitchUtils.safeSend(ctx, f'ⓘ Cheer action {bits} is now disabled: {result.cheerAction.printOut()}')
        else:
            self.__timber.log('DisableCheerActionChatCommand', f'An unknown error occurred when {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()} tried to disable cheer action {bits}')
            await self.__twitchUtils.safeSend(ctx, f'⚠ An unknown error occurred when trying to disable cheer action {bits}')

        self.__timber.log('DisableCheerActionChatCommand', f'Handled !disablecheeraction command for {ctx.getAuthorName()}:{ctx.getAuthorId()} in {user.getHandle()}')