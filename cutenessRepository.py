import locale

from backingDatabase import BackingDatabase
from userIdsRepository import UserIdsRepository


class CutenessRepository():

    def __init__(
        self,
        backingDatabase: BackingDatabase,
        leaderboardSize: int,
        localLeaderboardSize: int,
        userIdsRepository: UserIdsRepository
    ):
        if backingDatabase == None:
            raise ValueError(f'backingDatabase argument is malformed: \"{backingDatabase}\"')
        elif leaderboardSize == None:
            raise ValueError(f'leaderboardSize argument is malformed: \"{leaderboardSize}\"')
        elif leaderboardSize < 1 or leaderboardSize > 10:
            raise ValueError(f'leaderboardSize argument is out of bounds: \"{leaderboardSize}\"')
        elif localLeaderboardSize == None:
            raise ValueError(f'localLeaderboardSize argument is malformed: \"{localLeaderboardSize}\"')
        elif localLeaderboardSize < 1 or localLeaderboardSize > 6:
            raise ValueError(f'localLeaderboardSize argument is out of bounds: \"{localLeaderboardSize}\"')
        elif userIdsRepository == None:
            raise ValueError(f'userIdsRepository argument is malformed: \"{userIdsRepository}\"')

        self.__backingDatabase = backingDatabase
        self.__leaderboardSize = leaderboardSize
        self.__localLeaderboardSize = localLeaderboardSize
        self.__userIdsRepository = userIdsRepository

        connection = backingDatabase.getConnection()
        connection.execute(
            '''
                CREATE TABLE IF NOT EXISTS cuteness (
                    cuteness INTEGER NOT NULL DEFAULT 0,
                    twitchChannel TEXT NOT NULL COLLATE NOCASE,
                    userId TEXT NOT NULL COLLATE NOCASE,
                    PRIMARY KEY (twitchChannel, userId)
                )
            '''
        )
        connection.commit()

    def fetchCuteness(self, twitchChannel: str, userName: str):
        if twitchChannel == None or len(twitchChannel) == 0 or twitchChannel.isspace():
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif userName == None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        userId = self.__userIdsRepository.fetchUserId(userName = userName)

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute(
            '''
                SELECT cuteness FROM cuteness
                WHERE twitchChannel = ? AND userId = ?
            ''',
            ( twitchChannel, userId )
        )
        row = cursor.fetchone()

        cuteness = None
        if row != None:
            cuteness = row[0]

        cursor.close()
        return cuteness

    def fetchCutenessAndLocalLeaderboard(
        self,
        twitchChannel: str,
        userId: str,
        userName: str
    ):
        if twitchChannel == None or len(twitchChannel) == 0 or twitchChannel.isspace():
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif userId == None or len(userId) == 0 or userId.isspace() or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userName == None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__userIdsRepository.setUser(userId = userId, userName = userName)

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute(
            '''
                SELECT cuteness FROM cuteness
                WHERE twitchChannel = ? AND userId = ?
            ''',
            ( twitchChannel, userId )
        )
        row = cursor.fetchone()

        if row == None:
            cursor.close()
            return ( 0, None )

        cuteness = row[0]

        cursor.execute(
            '''
                SELECT cuteness, userId FROM cuteness
                WHERE twitchChannel = ? AND cuteness IS NOT NULL AND cuteness >= 1 AND userId != ?
                ORDER BY ABS(? - ABS(cuteness)) ASC
                LIMIT ?
            ''',
            ( twitchChannel, userId, cuteness, self.__localLeaderboardSize )
        )

        rows = cursor.fetchmany(size = self.__localLeaderboardSize)

        if len(rows) == 0:
            cursor.close()
            return ( cuteness, None )

        sortedRows = sorted(rows, key = lambda row: row[0], reverse = True)
        localLeaderboard = list()

        for row in sortedRows:
            # The try-except here is an unfortunate band-aid around an old, since been fixed, bug
            # that would cause us to not always have a person's username persisted in the database
            # alongside their user ID. So for any users that cause this exception to be raised,
            # we'll just ignore them.
            # If we were to ever start from scratch with a brand new database, this try-except
            # would be completely extranneous.
            try:
                userName = self.__userIdsRepository.fetchUserName(row[1])
                cuteStr = locale.format_string("%d", row[0], grouping = True)
                localLeaderboard.append(f'{userName} ({cuteStr})')
            except RuntimeError:
                print(f'Encountered a user ID that has no username: \"{row[1]}\"')

        cursor.close()
        return ( cuteness, localLeaderboard )

    def fetchCutenessIncrementedBy(
        self,
        incrementAmount: int,
        twitchChannel: str,
        userId: str,
        userName: str
    ):
        if incrementAmount == None:
            raise ValueError(f'incrementAmount argument is malformed: \"{incrementAmount}\"')
        elif twitchChannel == None or len(twitchChannel) == 0 or twitchChannel.isspace():
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')
        elif userId == None or len(userId) == 0 or userId.isspace() or userId == '0':
            raise ValueError(f'userId argument is malformed: \"{userId}\"')
        elif userName == None or len(userName) == 0 or userName.isspace():
            raise ValueError(f'userName argument is malformed: \"{userName}\"')

        self.__userIdsRepository.setUser(userId = userId, userName = userName)

        connection = self.__backingDatabase.getConnection()
        cursor = connection.cursor()
        cursor.execute(
            '''
                SELECT cuteness FROM cuteness
                WHERE twitchChannel = ? AND userId = ?
            ''',
            ( twitchChannel, userId )
        )
        row = cursor.fetchone()

        cuteness = 0
        if row != None:
            cuteness = row[0]

        cuteness = cuteness + incrementAmount

        if cuteness < 0:
            cuteness = 0

        cursor.execute(
            '''
                INSERT INTO cuteness (cuteness, twitchChannel, userId)
                VALUES (?, ?, ?)
                ON CONFLICT (twitchChannel, userId) DO UPDATE SET cuteness = excluded.cuteness
            ''',
            ( cuteness, twitchChannel, userId )
        )

        connection.commit()
        cursor.close()
        return cuteness

    def fetchLeaderboard(self, twitchChannel: str):
        if twitchChannel == None or len(twitchChannel) == 0 or twitchChannel.isspace():
            raise ValueError(f'twitchChannel argument is malformed: \"{twitchChannel}\"')

        twitchChannelUserId = self.__userIdsRepository.fetchUserId(userName = twitchChannel)

        cursor = self.__backingDatabase.getConnection().cursor()
        cursor.execute(
            '''
                SELECT cuteness, userId FROM cuteness
                WHERE twitchChannel = ? AND cuteness IS NOT NULL AND cuteness >= 1 AND userId != ?
                ORDER BY cuteness DESC
                LIMIT ?
            ''',
            ( twitchChannel, twitchChannelUserId, self.__leaderboardSize )
        )

        rows = cursor.fetchmany(size = self.__leaderboardSize)
        leaderboard = list()

        if len(rows) == 0:
            cursor.close()
            return leaderboard

        rank = 1

        for row in rows:
            userName = self.__userIdsRepository.fetchUserName(row[1])
            rankStr = locale.format_string("#%d", rank, grouping = True)
            cuteStr = locale.format_string("%d", row[0], grouping = True)
            leaderboard.append(f'{rankStr} {userName} ({cuteStr})')
            rank = rank + 1

        cursor.close()
        return leaderboard
