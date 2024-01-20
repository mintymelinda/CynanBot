import aiofiles.ospath

import CynanBot.misc.utils as utils
from CynanBot.soundPlayerHelper.soundAlert import SoundAlert
from CynanBot.soundPlayerHelper.soundPlayerHelperInterface import \
    SoundPlayerHelperInterface
from CynanBot.soundPlayerHelper.soundPlayerSettingsRepositoryInterface import \
    SoundPlayerSettingsRepositoryInterface
from CynanBot.systemCommandHelper.systemCommandHelperInterface import \
    SystemCommandHelperInterface
from CynanBot.timber.timberInterface import TimberInterface


class SoundPlayerHelper(SoundPlayerHelperInterface):

    def __init__(
        self,
        soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface,
        systemCommandHelper: SystemCommandHelperInterface,
        timber: TimberInterface
    ):
        if not isinstance(soundPlayerSettingsRepository, SoundPlayerSettingsRepositoryInterface):
            raise ValueError(f'soundPlayerSettingsRepository argument is malformed: \"{soundPlayerSettingsRepository}\"')
        elif not isinstance(systemCommandHelper, SystemCommandHelperInterface):
            raise ValueError(f'systemCommandHelper argument is malformed: \"{systemCommandHelper}\"')
        elif not isinstance(timber, TimberInterface):
            raise ValueError(f'timber argument is malformed: \"{timber}\"')

        self.__soundPlayerSettingsRepository: SoundPlayerSettingsRepositoryInterface = soundPlayerSettingsRepository
        self.__systemCommandHelper: SystemCommandHelperInterface = systemCommandHelper
        self.__timber: TimberInterface = timber

    async def play(self, soundAlert: SoundAlert):
        if not isinstance(soundAlert, SoundAlert):
            raise ValueError(f'soundAlert argument is malformed: \"{soundAlert}\"')

        filePath = await self.__soundPlayerSettingsRepository.getFilePathFor(soundAlert)

        if not utils.isValidStr(filePath):
            return

        filePath = utils.cleanPath(filePath)

        if not await aiofiles.ospath.exists(filePath):
            self.__timber.log('SoundPlayerHelper', f'File for sound alert {soundAlert} does not exist ({filePath=})')
            return
        elif not await aiofiles.ospath.isfile(filePath):
            self.__timber.log('SoundPlayerHelper', f'File for sound alert {soundAlert} is not a file ({filePath=})')
            return

        self.__timber.log('SoundPlayerHelper', f'Playing sound alert {soundAlert} ({filePath=})...')
        await self.__systemCommandHelper.executeVlcCommand(filePath)
