import traceback

import aiofiles.ospath

from .googleTtsChoice import GoogleTtsChoice
from .googleTtsFileManagerInterface import GoogleTtsFileManagerInterface
from .googleTtsMessageCleanerInterface import GoogleTtsMessageCleanerInterface
from .googleTtsVoiceChooserInterface import GoogleTtsVoiceChooserInterface
from ..tempFileHelper.ttsTempFileHelperInterface import TtsTempFileHelperInterface
from ..ttsCommandBuilderInterface import TtsCommandBuilderInterface
from ..ttsEvent import TtsEvent
from ..ttsManagerInterface import TtsManagerInterface
from ..ttsSettingsRepositoryInterface import TtsSettingsRepositoryInterface
from ...google.googleApiServiceInterface import GoogleApiServiceInterface
from ...google.googleTextSynthesisInput import GoogleTextSynthesisInput
from ...google.googleTextSynthesisResponse import GoogleTextSynthesisResponse
from ...google.googleTextSynthesizeRequest import GoogleTextSynthesizeRequest
from ...google.googleVoiceAudioConfig import GoogleVoiceAudioConfig
from ...google.settings.googleSettingsRepositoryInterface import GoogleSettingsRepositoryInterface
from ...misc import utils as utils
from ...soundPlayerManager.soundPlayerManagerInterface import SoundPlayerManagerInterface
from ...timber.timberInterface import TimberInterface


class GoogleTtsManager(TtsManagerInterface):

    def __init__(
        self,
        googleApiService: GoogleApiServiceInterface,
        googleSettingsRepository: GoogleSettingsRepositoryInterface,
        googleTtsFileManager: GoogleTtsFileManagerInterface,
        googleTtsMessageCleaner: GoogleTtsMessageCleanerInterface,
        googleTtsVoiceChooser: GoogleTtsVoiceChooserInterface,
        soundPlayerManager: SoundPlayerManagerInterface,
        timber: TimberInterface,
        ttsCommandBuilder: TtsCommandBuilderInterface,
        ttsSettingsRepository: TtsSettingsRepositoryInterface,
        ttsTempFileHelper: TtsTempFileHelperInterface
    ):
        if not isinstance(googleApiService, GoogleApiServiceInterface):
            raise TypeError(f'googleApiService argument is malformed: \"{googleApiService}"')
        elif not isinstance(googleSettingsRepository, GoogleSettingsRepositoryInterface):
            raise TypeError(f'googleSettingsRepository argument is malformed: \"{googleSettingsRepository}\"')
        elif not isinstance(googleTtsFileManager, GoogleTtsFileManagerInterface):
            raise TypeError(f'googleTtsFileManager argument is malformed: \"{googleTtsFileManager}\"')
        elif not isinstance(googleTtsMessageCleaner, GoogleTtsMessageCleanerInterface):
            raise TypeError(f'googleTtsMessageCleaner argument is malformed: \"{googleTtsMessageCleaner}\"')
        elif not isinstance(googleTtsVoiceChooser, GoogleTtsVoiceChooserInterface):
            raise TypeError(f'googleTtsVoiceChooser argument is malformed: \"{googleTtsVoiceChooser}\"')
        elif not isinstance(soundPlayerManager, SoundPlayerManagerInterface):
            raise TypeError(f'soundPlayerManager argument is malformed: \"{soundPlayerManager}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not isinstance(ttsCommandBuilder, TtsCommandBuilderInterface):
            raise TypeError(f'ttsCommandBuilder argument is malformed: \"{ttsCommandBuilder}\"')
        elif not isinstance(ttsSettingsRepository, TtsSettingsRepositoryInterface):
            raise TypeError(f'ttsSettingsRepository argument is malformed: \"{ttsSettingsRepository}\"')
        elif not isinstance(ttsTempFileHelper, TtsTempFileHelperInterface):
            raise TypeError(f'ttsTempFileHelper argument is malformed: \"{ttsTempFileHelper}\"')

        self.__googleApiService: GoogleApiServiceInterface = googleApiService
        self.__googleSettingsRepository: GoogleSettingsRepositoryInterface = googleSettingsRepository
        self.__googleTtsFileManager: GoogleTtsFileManagerInterface = googleTtsFileManager
        self.__googleTtsMessageCleaner: GoogleTtsMessageCleanerInterface = googleTtsMessageCleaner
        self.__googleTtsVoiceChooser: GoogleTtsVoiceChooserInterface = googleTtsVoiceChooser
        self.__soundPlayerManager: SoundPlayerManagerInterface = soundPlayerManager
        self.__timber: TimberInterface = timber
        self.__ttsCommandBuilder: TtsCommandBuilderInterface = ttsCommandBuilder
        self.__ttsSettingsRepository: TtsSettingsRepositoryInterface = ttsSettingsRepository
        self.__ttsTempFileHelper: TtsTempFileHelperInterface = ttsTempFileHelper

        self.__isLoading: bool = False

    async def isPlaying(self) -> bool:
        if self.__isLoading:
            return True

        # TODO Technically this method use is incorrect, as it is possible for SoundPlayerManager
        #  to be playing media, but it could be media that is completely unrelated to Google TTS,
        #  and yet in this scenario, this method would still return true. So for the fix for this
        #  is probably a way to check if SoundPlayerManager is currently playing, AND also a check
        #  to see specifically what media it is currently playing.
        return await self.__soundPlayerManager.isPlaying()

    async def playTtsEvent(self, event: TtsEvent) -> bool:
        if not isinstance(event, TtsEvent):
            raise TypeError(f'event argument is malformed: \"{event}\"')

        if not await self.__ttsSettingsRepository.isEnabled():
            return False
        elif await self.isPlaying():
            self.__timber.log('GoogleTtsManager', f'There is already an ongoing Google TTS event!')
            return False

        self.__isLoading = True
        fileName = await self.__processTtsEvent(event)

        if not utils.isValidStr(fileName) or not await aiofiles.ospath.exists(fileName):
            self.__timber.log('GoogleTtsManager', f'Failed to write TTS message in \"{event.twitchChannel}\" to a temporary file ({event=}) ({fileName=})')
            self.__isLoading = False
            return False

        self.__timber.log('GoogleTtsManager', f'Playing TTS message in \"{event.twitchChannel}\" from \"{fileName}\"...')

        await self.__soundPlayerManager.playSoundFile(
            filePath = fileName,
            volume = await self.__googleSettingsRepository.getMediaPlayerVolume()
        )

        await self.__ttsTempFileHelper.registerTempFile(fileName)
        self.__isLoading = False

        return True

    async def __processTtsEvent(self, event: TtsEvent) -> str | None:
        message = await self.__googleTtsMessageCleaner.clean(event.message)
        donationPrefix = await self.__ttsCommandBuilder.buildDonationPrefix(event)
        fullMessage: str

        if utils.isValidStr(message) and utils.isValidStr(donationPrefix):
            fullMessage = f'{donationPrefix} + {message}'
        elif utils.isValidStr(message):
            fullMessage = message
        elif utils.isValidStr(donationPrefix):
            fullMessage = donationPrefix
        else:
            return None

        ttsChoice = await self.__randomlyChooseTts()

        request = GoogleTextSynthesizeRequest(
            synthesisInput = GoogleTextSynthesisInput(
                text = fullMessage
            ),
            voice = ttsChoice.selectionParams,
            audioConfig = ttsChoice.audioConfig
        )

        response: GoogleTextSynthesisResponse | None = None
        exception: Exception | None = None

        try:
            response = await self.__googleApiService.textToSpeech(request)
        except Exception as e:
            exception = e

        if response is None or exception is not None:
            self.__timber.log('GoogleTtsManager', f'Failed to utilize Google Text to Speech API for TTS event ({event=}) ({response=}): {exception}', exception, traceback.format_exc())
            return None

        return await self.__googleTtsFileManager.writeBase64CommandToNewFile(
            base64Command = response.audioContent
        )

    async def __randomlyChooseTts(self) -> GoogleTtsChoice:
        audioConfig = GoogleVoiceAudioConfig(
            pitch = None,
            speakingRate = None,
            volumeGainDb = await self.__ttsSettingsRepository.getGoogleVolumeGainDb(),
            sampleRateHertz = None,
            audioEncoding = await self.__ttsSettingsRepository.getGoogleVoiceAudioEncoding()
        )

        selectionParams = await self.__googleTtsVoiceChooser.choose()

        return GoogleTtsChoice(
            audioConfig = audioConfig,
            selectionParams = selectionParams
        )
