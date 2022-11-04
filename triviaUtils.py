import locale

import CynanBotCommon.utils as utils
from CynanBotCommon.cuteness.cutenessResult import CutenessResult
from CynanBotCommon.trivia.absTriviaQuestion import AbsTriviaQuestion
from CynanBotCommon.trivia.triviaScoreResult import TriviaScoreResult
from CynanBotCommon.trivia.triviaType import TriviaType


class TriviaUtils():

    def __init__(self):
        pass

    def getCorrectAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        newCuteness: CutenessResult,
        userNameThatRedeemed: str,
        delimiter: str = '; '
    ) -> str:
        if question is None:
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif newCuteness is None:
            raise ValueError(f'newCuteness argument is malformed: \"{newCuteness}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        prefix = f'{question.getEmote()} Congratulations @{userNameThatRedeemed}, that\'s correct!'
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
        userNameThatRedeemed: str,
        delimiter: str = '; '
    ) -> str:
        if question is None:
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        prefix = f'{question.getEmote()} Sorry @{userNameThatRedeemed}, that\'s incorrect. {utils.getRandomSadEmoji()}'
        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} The correct answer is: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} The correct answers are: {correctAnswersStr}'

    def getInvalidAnswerInputPrompt(
        self,
        question: AbsTriviaQuestion,
        userNameThatRedeemed: str
    ) -> str:
        if question is None:
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')

        prefix = f'{question.getEmote()} Sorry @{userNameThatRedeemed}, that\'s an invalid input. {utils.getRandomSadEmoji()}'
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
        userNameThatRedeemed: str,
        delimiter: str = '; '
    ) -> str:
        if question is None:
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif not utils.isValidStr(userNameThatRedeemed):
            raise ValueError(f'userNameThatRedeemed argument is malformed: \"{userNameThatRedeemed}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        prefix = f'{question.getEmote()} Sorry @{userNameThatRedeemed}, you\'re out of time. {utils.getRandomSadEmoji()}'
        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} The correct answer is: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} The correct answers are: {correctAnswersStr}'

    def getTriviaScoreMessage(self, userName: str, triviaResult: TriviaScoreResult) -> str:
        if not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif triviaResult is None:
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
        newCuteness: CutenessResult,
        points: int,
        userName: str,
        delimiter: str = '; '
    ) -> str:
        if question is None:
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif newCuteness is None:
            raise ValueError(f'newCuteness argument is malformed: \"{newCuteness}\"')
        elif not utils.isValidNum(points):
            raise ValueError(f'points argument is malformed: \"{points}\"')
        elif not utils.isValidStr(userName):
            raise ValueError(f'userName argument is malformed: \"{userName}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        pointsStr = locale.format_string("%d", points, grouping = True)
        prefix = f'{question.getEmote()} CONGRATULATIONS @{userName}, that\'s correct!'
        infix = f'You earned {pointsStr} cuteness, so your new cuteness is {newCuteness.getCutenessStr()}.'

        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} 🎉 {infix} ✨ The correct answer was: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} 🎉 {infix} ✨ The correct answers were: {correctAnswersStr}'

    def getSuperTriviaLaunchpadPrompt(self, remainingQueueSize: int) -> str:
        if not utils.isValidNum(remainingQueueSize):
            raise ValueError(f'remainingQueueSize argument is malformed: \"{remainingQueueSize}\"')

        suffix = ''
        if remainingQueueSize >= 1:
            remainingQueueSizeStr = locale.format_string("%d", remainingQueueSize, grouping = True)
            suffix = f' (with another {remainingQueueSizeStr} after that)'

        return f'Another super trivia game will start shortly!{suffix}'

    def getSuperTriviaOutOfTimeAnswerReveal(
        self,
        question: AbsTriviaQuestion,
        delimiter: str = '; '
    ) -> str:
        if question is None:
            raise ValueError(f'question argument is malformed: \"{question}\"')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        prefix = f'{question.getEmote()} Sorry everyone, y\'all are out of time… {utils.getRandomSadEmoji()} …'
        correctAnswers = question.getCorrectAnswers()

        if len(correctAnswers) == 1:
            return f'{prefix} The correct answer is: {correctAnswers[0]}'
        else:
            correctAnswersStr = delimiter.join(correctAnswers)
            return f'{prefix} The correct answers are: {correctAnswersStr}'

    def getSuperTriviaQuestionPrompt(
        self,
        triviaQuestion: AbsTriviaQuestion,
        delaySeconds: int,
        points: int,
        multiplier: int,
        delimiter: str = ' '
    ) -> str:
        if triviaQuestion is None:
            raise ValueError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not utils.isValidNum(delaySeconds):
            raise ValueError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif delaySeconds < 1:
            raise ValueError(f'delaySeconds argument is out of bounds: {delaySeconds}')
        elif not utils.isValidNum(points):
            raise ValueError(f'points argument is malformed: \"{points}\"')
        elif points < 1:
            raise ValueError(f'points argument is out of bounds: {points}')
        elif not utils.isValidNum(multiplier):
            raise ValueError(f'multiplier argument is malformed: \"{multiplier}\"')
        elif multiplier < 1:
            raise ValueError(f'multiplier argument is out of bounds: {multiplier}')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        triviaEmote = triviaQuestion.getEmote()
        delaySecondsStr = locale.format_string("%d", delaySeconds, grouping = True)
        pointsStr = locale.format_string("%d", points, grouping = True)
        multiplierStr = locale.format_string("%d", multiplier, grouping = True)

        questionPrompt: str = None
        if triviaQuestion.getTriviaType() is TriviaType.QUESTION_ANSWER and triviaQuestion.hasCategory():
            questionPrompt = f'— category is {triviaQuestion.getCategory()} — {triviaQuestion.getQuestion()}'
        else:
            questionPrompt = f'— {triviaQuestion.getPrompt(delimiter)}'

        return f'{triviaEmote} EVERYONE can play, !superanswer in {delaySecondsStr}s for {pointsStr} points ({multiplierStr}x multiplier) {questionPrompt}'

    def getTriviaGameQuestionPrompt(
        self,
        triviaQuestion: AbsTriviaQuestion,
        delaySeconds: int,
        points: int,
        userNameThatRedeemed: str,
        delimiter: str = ' '
    ) -> str:
        if triviaQuestion is None:
            raise ValueError(f'triviaQuestion argument is malformed: \"{triviaQuestion}\"')
        elif not utils.isValidNum(delaySeconds):
            raise ValueError(f'delaySeconds argument is malformed: \"{delaySeconds}\"')
        elif delaySeconds < 1:
            raise ValueError(f'delaySeconds argument is out of bounds: {delaySeconds}')
        elif not utils.isValidNum(points):
            raise ValueError(f'points argument is malformed: \"{points}\"')
        elif points < 1:
            raise ValueError(f'points argument is out of bounds: {points}')
        elif delimiter is None:
            raise ValueError(f'delimiter argument is malformed: \"{delimiter}\"')

        triviaEmote = triviaQuestion.getEmote()
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

        return f'{triviaEmote} @{userNameThatRedeemed} !answer in {delaySecondsStr}s for {pointsStr} {pointsPlurality} {questionPrompt}'
