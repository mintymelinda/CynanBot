import random
import traceback
from typing import Optional

import CynanBot.misc.utils as utils
from CynanBot.language.languageEntry import LanguageEntry
from CynanBot.language.languagesRepositoryInterface import \
    LanguagesRepositoryInterface
from CynanBot.language.translation.deepLTranslationApi import \
    DeepLTranslationApi
from CynanBot.language.translation.googleTranslationApi import \
    GoogleTranslationApi
from CynanBot.language.translation.translationApi import TranslationApi
from CynanBot.language.translationApiSource import TranslationApiSource
from CynanBot.language.translationHelperInterface import \
    TranslationHelperInterface
from CynanBot.language.translationResponse import TranslationResponse
from CynanBot.timber.timberInterface import TimberInterface


class TranslationHelper(TranslationHelperInterface):

    def __init__(
        self,
        deepLTranslationApi: DeepLTranslationApi,
        googleTranslationApi: GoogleTranslationApi,
        languagesRepository: LanguagesRepositoryInterface,
        timber: TimberInterface,
        maxAttempts: int = 3
    ):
        if not isinstance(deepLTranslationApi, DeepLTranslationApi):
            raise TypeError(f'deepLTranslationApi argument is malformed: \"{deepLTranslationApi}\"')
        elif not isinstance(googleTranslationApi, GoogleTranslationApi):
            raise TypeError(f'googleTranslationApi argument is malformed: \"{googleTranslationApi}\"')
        elif not isinstance(languagesRepository, LanguagesRepositoryInterface):
            raise TypeError(f'languagesRepository argument is malformed: \"{languagesRepository}\"')
        elif not isinstance(timber, TimberInterface):
            raise TypeError(f'timber argument is malformed: \"{timber}\"')
        elif not utils.isValidInt(maxAttempts):
            raise TypeError(f'maxAttempts argument is malformed: \"{maxAttempts}\"')
        elif maxAttempts < 1 or maxAttempts > 10:
            raise ValueError(f'maxAttempts argument is out of bounds: {maxAttempts}')

        self.__deepLTranslationApi: TranslationApi = deepLTranslationApi
        self.__googleTranslationApi: TranslationApi = googleTranslationApi
        self.__languagesRepository: LanguagesRepositoryInterface = languagesRepository
        self.__timber: TimberInterface = timber
        self.__maxAttempts: int = maxAttempts

    async def translate(
        self,
        text: str,
        targetLanguage: Optional[LanguageEntry] = None
    ) -> TranslationResponse:
        if not utils.isValidStr(text):
            raise TypeError(f'text argument is malformed: \"{text}\"')
        elif targetLanguage is not None and not isinstance(targetLanguage, LanguageEntry):
            raise TypeError(f'targetLanguageEntry argument is malformed: \"{targetLanguage}\"')
        elif targetLanguage is not None and not targetLanguage.hasIso6391Code():
            raise ValueError(f'targetLanguage has no ISO 639-1 code: \"{targetLanguage}\"')

        text = utils.cleanStr(text)

        if targetLanguage is None:
            targetLanguage = await self.__languagesRepository.requireLanguageForCommand(
                command = 'en',
                hasIso6391Code = True
            )

        # In order to help keep us from running beyond the free usage tiers for the Google
        # Translate and DeepL translation services, let's randomly choose which translation service
        # to use. At the time of this writing, both services have a 500,000 character monthly limit.
        # So theoretically, this gives us a 1,000,000 character translation capability.

        attempt = 0
        translationApi: Optional[TranslationApi] = None
        translationResponse: Optional[TranslationResponse] = None

        while translationResponse is None or attempt < self.__maxAttempts:
            translationApiSource = random.choice(list(TranslationApiSource))

            if translationApiSource is TranslationApiSource.DEEP_L:
                translationApi = self.__deepLTranslationApi
            elif translationApiSource is TranslationApiSource.GOOGLE_TRANSLATE:
                translationApi = self.__googleTranslationApi
            else:
                raise RuntimeError(f'unknown TranslationApiSource: \"{translationApiSource}\"')

            if not await translationApi.isAvailable():
                continue

            try:
                translationResponse = await translationApi.translate(
                    text = text,
                    targetLanguage = targetLanguage
                )
            except Exception as e:
                self.__timber.log('TranslationHelper', f'Exception occurred when translating ({text=}) ({targetLanguage=}) ({attempt=}) ({translationApiSource=})', e, traceback.format_exc())

            attempt = attempt + 1

        return translationResponse
