''' Saving and loading scores/statistics '''
import os
import math
from dataclasses import dataclass, field
from itertools import chain

try:
    import platformdirs
except ImportError:
    STATSPATH = os.path.expanduser('~/.pyfarkle/scores.dat')
else:
    STATSPATH = os.path.join(platformdirs.user_data_dir('pyfarkle'), 'scores.dat')


@dataclass
class Score:
    ''' One player's score in a game '''
    player: str
    score: int
    bestbank: int


@dataclass
class GameStat:
    ''' Both players scores - One row in the stats file '''
    player1: Score
    player2: Score

    def __str__(self):
        return (f'{self.player1.player};'
                f'{self.player1.score};'
                f'{self.player1.bestbank};'
                f'{self.player2.player};'
                f'{self.player2.score};'
                f'{self.player2.bestbank}')

    @property
    def winner(self) -> Score:
        ''' The winning player '''
        if self.player1.score > self.player2.score:
            return self.player1
        return self.player2

    @property
    def loser(self) -> Score:
        ''' The losing player '''
        if self.player1.score > self.player2.score:
            return self.player2
        return self.player1

    @property
    def hiturnscore(self) -> Score:
        ''' The player with higher best-bank score '''
        if self.player1.bestbank > self.player2.bestbank:
            return self.player1
        return self.player2


@dataclass
class WinRate:
    ''' Win rate statistics '''
    wins: int
    total: int
    percent: float = field(init=False)

    def __post_init__(self):
        try:
            self.percent = self.wins/self.total*100
        except ZeroDivisionError:
            self.percent = math.nan



class GameStats:
    ''' Farkle game statistics. Loaded from file determined by platformdirs. '''
    STATSPATH = STATSPATH

    def __init__(self) -> None:
        ''' Load list of games from file '''
        if not os.path.exists(self.STATSPATH):
            self.games = []
            return

        with open(self.STATSPATH, 'r') as f:
            lines = f.readlines()

        games: list[GameStat] = []
        for line in lines:
            values = line.split(';')
            p1 = Score(values[0],
                       int(values[1]),
                       int(values[2]))
            p2 = Score(values[3],
                       int(values[4]),
                       int(values[5]))
            games.append(GameStat(p1, p2))
        self.games = games
    
    @property
    def high_scores(self) -> list[Score]:
        ''' Sorted list of Scores '''
        winners = [g.winner for g in self.games]
        return sorted(winners, key=lambda g: g.score, reverse=True)

    @property
    def high_turnscores(self) -> list[Score]:
        ''' Sorted list of best-bank scores '''
        highs = [g.hiturnscore for g in self.games]
        return sorted(highs, key=lambda g: g.bestbank, reverse=True)

    @property
    def players(self) -> set[str]:
        ''' Set of all players in stats data '''
        return set(chain(*[(g.player1.player, g.player2.player) for g in self.games]))

    def bestbank(self, player: str) -> int:
        ''' Get best bank by the player '''
        flatgames = chain(*[(g.player1, g.player2) for g in self.games])
        return max(g.bestbank for g in flatgames if g.player == player)

    def bestscore(self, player: str) -> int:
        ''' Get best score by the player '''
        flatgames = chain(*[(g.player1, g.player2) for g in self.games])
        return max(g.score for g in flatgames if g.player == player)

    def winrate(self, player1: str, player2: str) -> WinRate:
        ''' Games player1 won vs player2 '''
        total = 0
        wins = 0
        for game in self.games:
            if (game.player1.player == player1 and game.player2.player == player2):
                total += 1
                wins += game.player1.score > game.player2.score
            elif (game.player1.player == player2 and game.player2.player == player1):
                total += 1
                wins += game.player2.score > game.player1.score
        return WinRate(wins, total)
    
    def winrate_all(self, player1: str) -> WinRate:
        ''' A player's stats over all opponents '''
        total = 0
        wins = 0
        for game in self.games:
            if game.player1.player == player1:
                total += 1
                wins += game.player1.score > game.player2.score
            elif game.player2.player == player1:
                total += 1
                wins += game.player2.score > game.player1.score
        return WinRate(wins, total)
    
    def winrates(self) -> dict[str, dict[str, WinRate]]:
        ''' Get WinRate of all players against all other players as nested dict '''
        players = self.players
        stats: dict[str, dict[str, WinRate]] = {}
        for player1 in players:
            stats[player1] = {}
            for player2 in players:
                if player1 == player2:
                    continue
                stats[player1][player2] = self.winrate(player1, player2)
            stats[player1]['ALL'] = self.winrate_all(player1)
        return stats

    @classmethod
    def savescore(cls,
                  player1: str,
                  p1score: int,
                  p1bestbank: int,
                  player2: str,
                  p2score: int,
                  p2bestbank: int) -> None:
        ''' Save the score to stats file '''
        os.makedirs(os.path.dirname(cls.STATSPATH), exist_ok=True)
        with open(cls.STATSPATH, 'a') as f:
            f.write(str(GameStat(Score(player1, p1score, p1bestbank),
                                 Score(player2, p2score, p2bestbank))) + '\n')

    @classmethod
    def clearstats(cls) -> None:
        ''' Delete the saved statistics file '''
        try:
            os.remove(cls.STATSPATH)
        except FileNotFoundError:
            pass
