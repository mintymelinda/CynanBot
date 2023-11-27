from abc import ABC, abstractmethod
from typing import Optional

from CynanBot.trivia.bannedTriviaQuestion import BannedTriviaQuestion
from CynanBot.trivia.banTriviaQuestionResult import BanTriviaQuestionResult
from CynanBot.trivia.triviaSource import TriviaSource


class BannedTriviaIdsRepositoryInterface(ABC):

    @abstractmethod
    async def ban(
        self,
        triviaId: str,
        userId: str,
        triviaSource: TriviaSource
    ) -> BanTriviaQuestionResult:
        pass

    @abstractmethod
    async def getInfo(
        self,
        triviaId: str,
        triviaSource: TriviaSource
    ) -> Optional[BannedTriviaQuestion]:
        pass

    @abstractmethod
    async def isBanned(self, triviaId: str, triviaSource: TriviaSource) -> bool:
        pass

    @abstractmethod
    async def unban(
        self,
        triviaId: str,
        triviaSource: TriviaSource
    ) -> BanTriviaQuestionResult:
        pass