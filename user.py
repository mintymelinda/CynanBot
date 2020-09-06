import os
from urllib.parse import urlparse

class User:
    def __init__(
        self,
        isAnalogueEnabled: bool,
        isEsWordOfTheDayEnabled: bool,
        isFrWordOfTheDayEnabled: bool,
        isJaWordOfTheDayEnabled: bool,
        isPicOfTheDayEnabled: bool,
        isZhWordOfTheDayEnabled: bool,
        discord: str,
        handle: str,
        picOfTheDayFile: str,
        picOfTheDayRewardId: str,
        speedrunProfile: str,
        twitter: str,
        timeZone
    ):
        if handle == None or len(handle) == 0 or handle.isspace():
            raise ValueError(f'handle argument is malformed: \"{handle}\"')
        elif isPicOfTheDayEnabled and (picOfTheDayFile == None or len(picOfTheDayFile) == 0 or picOfTheDayFile.isspace()):
            raise ValueError(f'picOfTheDayFile argument is malformed: \"{picOfTheDayFile}\"')

        self.__isAnalogueEnabled = isAnalogueEnabled
        self.__isEsWordOfTheDayEnabled = isEsWordOfTheDayEnabled
        self.__isFrWordOfTheDayEnabled = isFrWordOfTheDayEnabled
        self.__isJaWordOfTheDayEnabled = isJaWordOfTheDayEnabled
        self.__isPicOfTheDayEnabled = isPicOfTheDayEnabled
        self.__isZhWordOfTheDayEnabled = isZhWordOfTheDayEnabled
        self.__discord = discord
        self.__handle = handle
        self.__picOfTheDayFile = picOfTheDayFile
        self.__picOfTheDayRewardId = picOfTheDayRewardId
        self.__speedrunProfile = speedrunProfile
        self.__twitter = twitter
        self.__timeZone = timeZone

    def fetchPicOfTheDay(self):
        if not self.__isPicOfTheDayEnabled:
            raise RuntimeError(f'POTD is disabled for {self.__handle}')
        elif not os.path.exists(self.__picOfTheDayFile):
            raise FileNotFoundError(f'POTD file not found: \"{self.__picOfTheDayFile}\"')

        with open(self.__picOfTheDayFile, 'r') as file:
            potdText = file.read().replace('\n', '').strip()

        if potdText == None or len(potdText) == 0 or potdText.isspace():
            raise ValueError(f'POTD text is malformed: \"{potdText}\"')

        potdParsed = urlparse(potdText)
        potdUrl = potdParsed.geturl()

        if potdUrl == None or len(potdUrl) == 0 or potdUrl.isspace():
            raise ValueError(f'POTD URL is malformed: \"{potdUrl}\"')

        return potdUrl

    def getDiscord(self):
        return self.__discord

    def getHandle(self):
        return self.__handle

    def getPicOfTheDayRewardId(self):
        return self.__picOfTheDayRewardId

    def getSpeedrunProfile(self):
        return self.__speedrunProfile

    def getTimeZone(self):
        return self.__timeZone

    def getTwitter(self):
        return self.__twitter

    def isAnalogueEnabled(self):
        return self.__isAnalogueEnabled

    def isEsWordOfTheDayEnabled(self):
        return self.__isEsWordOfTheDayEnabled

    def isFrWordOfTheDayEnabled(self):
        return self.__isFrWordOfTheDayEnabled

    def isJaWordOfTheDayEnabled(self):
        return self.__isJaWordOfTheDayEnabled

    def isPicOfTheDayEnabled(self):
        return self.__isPicOfTheDayEnabled

    def isZhWordOfTheDayEnabled(self):
        return self.__isZhWordOfTheDayEnabled
