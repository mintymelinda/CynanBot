import locale
from typing import List, Optional

import CynanBotCommon.utils as utils
from CynanBotCommon.cuteness.cutenessResult import CutenessResult
from CynanBotCommon.trivia.absTriviaQuestion import AbsTriviaQuestion
from CynanBotCommon.trivia.triviaGameController import TriviaGameController
from CynanBotCommon.trivia.triviaGameControllersRepository import \
    TriviaGameControllersRepository
from CynanBotCommon.trivia.triviaScoreResult import TriviaScoreResult
from CynanBotCommon.trivia.triviaType import TriviaType
from generalSettingsRepository import GeneralSettingsRepository
from users.usersRepository import UsersRepository


class TriviaUtils():

    def __init__(
        self,
        generalSettingsRepository: GeneralSettingsRepository,
        triviaGameControllersRepository: TriviaGameControllersRepository,
        usersRepository: UsersRepository
    ):
        if not isinstance(generalSettingsRepository, GeneralSettingsRepository):
            raise ValueError(f'generalSettingsRepository argument is malformed: \"{generalSettingsRepository}\"')
        elif not isinstance(triviaGameControllersRepository, TriviaGameControllersRepository):
            raise ValueError(f'triviaGameControllersRepository argument is malformed: \"{triviaGameControllersRepository}\"')
        elif not isinstance(usersRepository, UsersRepository):
            raise ValueError(f'usersRepository argument is malformed: \"{usersRepository}\"')

        self.__generalSettingsRepository: GeneralSettingsRepository = generalSettingsRepository
        self.__triviaGameControllersRepository: TriviaGameControllersRepository = triviaGameControllersRepository
        self.__usersRepository: UsersRepository = usersRepository

    def getCorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        isShiny: bool,
        newCuteness: CutenessResult,
        userNameThatRedeemed: str,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidBool(isShiny):
            raise ValueError(f'isShiny argument is malformed: \"{isShiny}\"')
        elif not isinstance(newCuteness, CutenessResult):
            raise ValueError(f'newCuteness argument is malformed: \"{newCuteness}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt: str = None
        if isShiny:
            emotePrompt = f'✨{question.getEmote()}✨'
        else:
            emotePrompt = question.getEmote()

        prefix = f'{emotePrompt} Congratulations @{userNameThatRedeemed}, that\'s correct!'
        infix = f'Your new cuteness is {newCuteness.getCutenessStr()}.'

        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} 🎉 {infix} ✨ The correct answer was: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} 🎉 {infix} ✨ The correct answers were: {correctAnswersStr}'

    def getIncorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        isShiny: bool,
        userNameThatRedeemed: str,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidBool(isShiny):
            raise ValueError(f'isShiny argument is malformed: \"{isShiny}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt: str = None
        if isShiny:
            emotePrompt = f'✨{question.getEmote()}✨'
        else:
            emotePrompt = question.getEmote()

        prefix = f'{emotePrompt} Sorry @{userNameThatRedeemed}, that\'s incorrect. {utils.getRandomSadEmoji()}'
        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} The correct answer is: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} The correct answers are: {correctAnswersStr}'

    def getInvalidAnswerInputPrompt(
        self,
        question: AbsTriviaQuestion,
        isShiny: bool,
        userNameThatRedeemed: str
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidBool(isShiny):
            raise ValueError(f'isShiny argument is malformed: \"{isShiny}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        emotePrompt: str = None
        if isShiny:
            emotePrompt = f'✨{question.getEmote()}✨'
        else:
            emotePrompt = question.getEmote()

        prefix = f'{emotePrompt} Sorry @{userNameThatRedeemed}, that\'s an invalid input. {utils.getRandomSadEmoji()}'
        suffix: str = None

        if question.getTriviaType() is TriviaType.MULTIPLE_CHOICE:
            suffix = 'Please answer using A, B, C, …'
        elif question.getTriviaType() is TriviaType.TRUE_FALSE:
            suffix = 'Please answer using either true or false.'
        else:
            suffix = 'Please check your answer and try again.'

        return f'{prefix} {suffix}'

    def getOutOfTimeAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        isShiny: bool,
        userNameThatRedeemed: str,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidBool(isShiny):
            raise ValueError(f'isShiny argument is malformed: \"{isShiny}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt: str = None
        if isShiny:
            emotePrompt = f'✨{question.getEmote()}✨'
        else:
            emotePrompt = question.getEmote()

        prefix = f'{emotePrompt} Sorry @{userNameThatRedeemed}, you\'re out of time. {utils.getRandomSadEmoji()}'
        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} The correct answer is: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} The correct answers are: {correctAnswersStr}'

    def getTriviaScoreMessage(self, userName: str, triviaResult: TriviaScoreResult) -> str:
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif not isinstance(triviaResult, TriviaScoreResult):
            raise ValueError(f'triviaResult argument is malformed: \"{triviaResult}\"')

        if triviaResult.getTotal() <= 0:
            if triviaResult.getSuperTriviaWins() > 1:
                return f'@{userName} has not played any trivia games 😿 (but has {triviaResult.getSuperTriviaWinsStr()} super trivia wins)'
            elif triviaResult.getSuperTriviaWins() == 1:
                return f'@{userName} has not played any trivia games 😿 (but has {triviaResult.getSuperTriviaWinsStr()} super trivia win)'
            else:
                return f'@{userName} has not played any trivia games 😿'

        gamesStr: str = 'games'
        if triviaResult.getTotal() == 1:
            gamesStr = 'game'

        ratioStr: str = f' ({triviaResult.getWinPercentStr()} wins)'

        streakStr: str = ''
        if triviaResult.getStreak() >= 3:
            streakStr = f', and is on a {triviaResult.getAbsStreakStr()} game winning streak 😸'
        elif triviaResult.getStreak() <= -3:
            streakStr = f', and is on a {triviaResult.getAbsStreakStr()} game losing streak 🙀'

        superTriviaWinsStr: str = ''
        if triviaResult.getSuperTriviaWins() > 1:
            superTriviaWinsStr = f' (and has {triviaResult.getSuperTriviaWinsStr()} super trivia wins)'
        elif triviaResult.getSuperTriviaWins() == 1:
            superTriviaWinsStr = f' (and has {triviaResult.getSuperTriviaWinsStr()} super trivia win)'

        return f'@{userName} has played {triviaResult.getTotalStr()} trivia {gamesStr}, {triviaResult.getTriviaWinsStr()}-{triviaResult.getTriviaLossesStr()} {ratioStr}{streakStr}{superTriviaWinsStr}'.strip()

    def getSuperTriviaCorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        isShiny: bool,
        newCuteness: CutenessResult,
        points: int,
        userName: str,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidBool(isShiny):
            raise ValueError(f'isShiny argument is malformed: \"{isShiny}\"')
        elif not isinstance(newCuteness, CutenessResult):
            raise ValueError(f'newCuteness argument is malformed: \"{newCuteness}\"')
        elif not utils.isValidInt(points):
            raise ValueError(f'points argument is malformed: \"{points}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt: str = None
        if isShiny:
            emotePrompt = f'✨{question.getEmote()}✨'
        else:
            emotePrompt = question.getEmote()

        pointsStr = locale.format_string("%d", points, grouping = True)
        prefix = f'{emotePrompt} CONGRATULATIONS @{userName}, that\'s correct!'
        infix = f'You earned {pointsStr} cuteness, so your new cuteness is {newCuteness.getCutenessStr()}.'

        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} 🎉 {infix} ✨ The correct answer was: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} 🎉 {infix} ✨ The correct answers were: {correctAnswersStr}'

    def getSuperTriviaLaunchpadPrompt(self, remainingQueueSize: int) -> Optional[str]:
        if not utils.isValidInt(remainingQueueSize):
            raise ValueError(f'remainingQueueSize argument is malformed: \"{remainingQueueSize}\"')

        if remainingQueueSize < 1:
            return None
        elif remainingQueueSize == 1:
            return f'One more super trivia game coming up!'
        else:
            remainingQueueSizeStr = locale.format_string("%d", remainingQueueSize, grouping = True)
            return f'{remainingQueueSizeStr} more super trivia games coming up!'

    def getSuperTriviaOutOfTimeAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        isShiny: bool,
        delimiter: str = '; '
    ) -> str:
        if not isinstance(question, AbsTriviaQuestion):
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidBool(isShiny):
            raise ValueError(f'isShiny argument is malformed: \"{isShiny}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt: str = None
        if isShiny:
            emotePrompt = f'✨{question.getEmote()}✨'
        else:
            emotePrompt = question.getEmote()

        prefix = f'{emotePrompt} Sorry everyone, y\'all are out of time… {utils.getRandomSadEmoji()} …'
        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} The correct answer is: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} The correct answers are: {correctAnswersStr}'

    def getSuperTriviaGameQuestionPrompt(
        self,
        triviaQuestion: AbsTriviaQuestion,
        isShiny: bool,
        delaySeconds: int,
        points: int,
        delimiter: str = ' '
    ) -> str:
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise ValueError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not utils.isValidBool(isShiny):
            raise ValueError(f'isShiny argument is malformed: \"{isShiny}\"')
        elif not utils.isValidInt(delaySeconds):
            raise ValueError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif delaySeconds < 1 or delaySeconds >= utils.getIntMaxSafeSize():
            raise ValueError(f'delaySeconds argument is out of bounds: {delaySeconds}')
        elif not utils.isValidInt(points):
            raise ValueError(f'points argument is malformed: \"{points}\"')
        elif points < 1 or points >= utils.getIntMaxSafeSize():
            raise ValueError(f'points argument is out of bounds: {points}')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt: str = None
        if isShiny:
            emotePrompt = f'✨{triviaQuestion.getEmote()}✨'
        else:
            emotePrompt = triviaQuestion.getEmote()

        delaySecondsStr = locale.format_string("%d", delaySeconds, grouping = True)
        pointsStr = locale.format_string("%d", points, grouping = True)

        questionPrompt: str = None
        if triviaQuestion.getTriviaType() is TriviaType.QUESTION_ANSWER and triviaQuestion.hasCategory():
            questionPrompt = f'— category is {triviaQuestion.getCategory()} — {triviaQuestion.getQuestion()}'
        else:
            questionPrompt = f'— {triviaQuestion.getPrompt(delimiter)}'

        return f'{emotePrompt} EVERYONE can play, !superanswer in {delaySecondsStr}s for {pointsStr} points {questionPrompt}'

    def getTriviaGameControllers(
        self,
        gameControllers: Optional[List[TriviaGameController]],
        delimiter: str = ', '
    ) -> str:
        if delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        if not utils.hasItems(gameControllers):
            return f'ⓘ Your channel has no trivia game controllers.'

        gameControllersNames: List[str] = list()
        for gameController in gameControllers:
            gameControllersNames.append(gameController.getUserName())

        gameControllersStr = delimiter.join(gameControllersNames)
        return f'ⓘ Your trivia game controllers — {gameControllersStr}'

    def getTriviaGameQuestionPrompt(
        self,
        triviaQuestion: AbsTriviaQuestion,
        isShiny: bool,
        delaySeconds: int,
        points: int,
        userNameThatRedeemed: str,
        delimiter: str = ' '
    ) -> str:
        if not isinstance(triviaQuestion, AbsTriviaQuestion):
            raise ValueError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not utils.isValidBool(isShiny):
            raise ValueError(f'isShiny argument is malformed: \"{isShiny}\"')
        elif not utils.isValidInt(delaySeconds):
            raise ValueError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif delaySeconds < 1 or delaySeconds >= utils.getIntMaxSafeSize():
            raise ValueError(f'delaySeconds argument is out of bounds: {delaySeconds}')
        elif not utils.isValidInt(points):
            raise ValueError(f'points argument is malformed: \"{points}\"')
        elif points < 1 or points >= utils.getIntMaxSafeSize():
            raise ValueError(f'points argument is out of bounds: {points}')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        emotePrompt: str = None
        if isShiny:
            emotePrompt = f'✨{triviaQuestion.getEmote()}✨'
        else:
            emotePrompt = triviaQuestion.getEmote()

        delaySecondsStr = locale.format_string("%d", delaySeconds, grouping = True)
        pointsStr = locale.format_string("%d", points, grouping = True)

        pointsPlurality: str = None
        if points == 1:
            pointsPlurality = 'point'
        else:
            pointsPlurality = 'points'

        questionPrompt: str = None
        if triviaQuestion.getTriviaType() is TriviaType.QUESTION_ANSWER and triviaQuestion.hasCategory():
            questionPrompt = f'(category is \"{triviaQuestion.getCategory()}\") — {triviaQuestion.getQuestion()}'
        else:
            questionPrompt = f'— {triviaQuestion.getPrompt(delimiter)}'

        return f'{emotePrompt} @{userNameThatRedeemed} !answer in {delaySecondsStr}s for {pointsStr} {pointsPlurality} {questionPrompt}'

    async def isPrivilegedTriviaUser(self, twitchChannel: str, userName: str) -> bool:
        if not utils.isValidStr(twitchChannel):
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        userName = userName.lower()

        user = await self.__usersRepository.getUserAsync(twitchChannel)
        if userName == user.getHandle().lower():
            return True

        gameControllers = await self.__triviaGameControllersRepository.getControllers(user.getHandle())
        for gameController in gameControllers:
            if userName == gameController.getUserName().lower():
                return True

        generalSettings = await self.__generalSettingsRepository.getAllAsync()
        if userName == generalSettings.requireAdministrator().lower():
            return True

        globalGameControllers = generalSettings.getGlobalTriviaGameControllers()
        for globalGameController in globalGameControllers:
            if userName == globalGameController.lower():
                return True

        return False
