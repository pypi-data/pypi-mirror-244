''' Farkle Game '''

from typing import Sequence
import random
from collections import Counter
from itertools import combinations

from . import strategy
from .scores import GameStats


AI_NAMES = ['Super Sally', 'Happy Harry', 'Maniacal Matt']


class Player(object):
    ''' Farkle Player

        Args:
            name: Player's name
            threshold: Opening game threshold
            triple_farkle: Penalty for farkling 3 times in a row
    '''
    is_ai = False

    def __init__(self, name: str, threshold: int = 500, triple_farkle: int = 1000):
        self.name = name
        self.totalscore = 0
        self.threshold = threshold
        self.turnscore = 0
        self.inplay = 6
        self.rollcount = 0
        self.held: Sequence[int] = []
        self.roll: Sequence[int] = []
        self.farkles_in_a_row = 0
        self.triple_farkle = triple_farkle
        self.bestbank = 0

    def newturn(self) -> None:
        ''' Start a new turn '''
        self.turnscore = 0
        self.inplay = 6
        self.rollcount = 0
        self.held = []

    def rollem(self) -> list[int]:
        ''' Roll the dice '''
        assert self.can_roll
        self.inplay = self.inplay - len(self.held)
        if self.inplay == 0:
            self.inplay = 6
        self.turnscore += self.holdscore
        self.roll = [random.randint(1, 6) for i in range(self.inplay)]
        self.rollcount += 1
        if self.is_farkle:
            self.farkles_in_a_row += 1
            if self.farkles_in_a_row == 3:
                self.totalscore -= self.triple_farkle
        return self.roll

    def hold(self, indexes: Sequence[int]) -> int:
        ''' Set which dice to hold and return score of current hold '''
        self.held = indexes
        return self.holdscore

    @property
    def is_farkle(self) -> bool:
        ''' True if the roll was a farkle - no scoring options '''
        c = Counter(self.roll)
        if 1 in self.roll or 5 in self.roll:
            return False
        if c.most_common(1)[0][1] > 2:
            return False  # 3+ of a kind
        if len(c) == 6:
            return False  # 1-6 Straight
        if len(c) == 3 and all(n[1]==2 for n in c.most_common(6)):
            return False  # 3-pairs
        return True

    @property
    def can_roll(self) -> bool:
        ''' Can the player roll? '''
        return (self.holdscore > 0 or
                self.rollcount == 0)

    @property
    def can_bank(self) -> bool:
        ''' Can the player bank the turn? '''
        holdscore = self.holdscore
        return holdscore > 0 and holdscore + self.turnscore >= self.threshold

    def bank(self) -> None:
        ''' Bank the turn '''
        assert self.can_bank
        self.bestbank = max(self.bestbank, self.holdscore+self.turnscore)
        self.totalscore += self.holdscore + self.turnscore
        self.threshold = 0
        self.farkles_in_a_row = 0
        self.newturn()

    @property
    def holdscore(self) -> int:
        ''' Get the score for the currently held dice '''
        roll = [self.roll[k] for k in self.held]
        c = Counter(roll)

        if len(c) == 6:
            return 1500  # Straight
        elif len(c) == 3 and set(c.values()) == {2}:
            return 750   # 3-pairs

        # Count up 3+ of a kind, 1's and 5's
        score = 0
        for val, count in c.most_common(n=len(roll)):
            add = 0
            if count > 2 and val == 1:
                add = 1000 * (count-2)
            elif count > 2:
                add = val * 100 * (count-2)
            elif val == 1:
                add = 100 * count
            elif val == 5:
                add = 50 * count
            if add > 0:   # Remove scored dice
                roll = [r for r in roll if r != val]
                score += add
        if len(roll) > 0:
            return 0
        return score


class PlayerAI(Player):
    ''' Computer/AI player. Same as human but different process for holding dice.
        This player banks whenever 2 or fewer die remain to roll, or if this turn
        released the opening threshold.
    '''
    is_ai = True

    def ai_holds(self) -> tuple[list[int], bool]:
        ''' Decide which dice to hold and whether to bank
        
            Returns:
                holds: indices of dice to hold
                bank: whether to bank after holding the dice
        '''
        combos: list[list[int]] = []
        for i in range(len(self.roll)):
            combos.extend(combinations(range(len(self.roll)), i+1))  # type: ignore
        maxscore = -1
        seldice: list[int] = []
        for combo in combos:
            self.held = combo
            points = self.holdscore
            if points > maxscore:
                maxscore = points
                seldice = combo

        n = len(self.roll) - len(seldice)
        bank = (maxscore + self.turnscore >= self.threshold and
                ((n > 0 and n <= 2) or             # Bank when 1 or 2 die left
                 (n > 0 and self.threshold > 1)))  # Or if we can hit opening threshold
        self.held = []        
        return seldice, bank
    

class Player2(PlayerAI):
    ''' This player banks if they have more than 750 points regardless of die remaining '''
    minturn = 750

    def ai_holds(self):
        ''' Decide which dice to hold and whether to bank
        
            Returns:
                holds: indices of dice to hold
                bank: whether to bank after holding the dice
        '''
        combos = []
        for i in range(len(self.roll)):
            combos.extend(combinations(list(range(len(self.roll))), i+1))

        maxscore = -1
        bestcombo = None
        for combo in combos:
            self.held = combo
            points = self.holdscore
            if points > 0 and points > maxscore:
                maxscore = points
                bestcombo = combo
        n = len(self.roll) - len(bestcombo)
        bank = (maxscore + self.turnscore >= self.threshold and n != 0 and maxscore+self.turnscore > self.minturn)
        self.held = []
        return bestcombo, bank
       

class Player3(PlayerAI):
    ''' This player is based on the optimal strategy published by Maniacal Matt at
        http://www.mattbusche.org/blog/article/zilch/
        
        Using the table matching the farkle rules used here.
        http://www.mattbusche.org/projects/farkle/strategy.php?set1=100,200,1000,2000,3000,4000&set2=0,0,200,400,600,800&set3=0,0,300,600,900,1200&set4=0,0,400,800,1200,1600&set5=50,100,500,1000,1500,2000&set6=0,0,600,1200,1800,2400&straight=1500&threepair=750&flexpairs=false&twotriplet=0&nothing=0&penalty=0&minbank=0
    '''
    def ai_holds(self):
        ''' Decide which dice to hold and whether to bank
        
            Returns:
                holds: indices of dice to hold
                bank: whether to bank after holding the dice
        '''
        strategy_table, bankmin = strategy.get_strategy(
            self.triple_farkle, self.farkles_in_a_row)

        combos = []
        for i in range(len(self.roll)):
            combos.extend(combinations(list(range(len(self.roll))), i+1))
        best = 0
        bestn = None
        bestcombo = None
        bank = None
        for combo in combos:
            self.held = combo
            t = self.holdscore
            if t > 0:
                n = len(self.roll) - len(combo)
                n = 6 if n == 0 else n
                w = strategy_table[(t+self.turnscore)//50][6-n]
                if w and w > best:
                    bestcombo = combo
                    best = w
                    bestn = n
                    bank = (t + self.turnscore >= self.threshold) and (t+self.turnscore >= bankmin[6-n])
                elif w == best and n > bestn:
                    bestcombo = combo
                    bestn = n
                    bank = (t + self.turnscore >= self.threshold) and (t+self.turnscore >= bankmin[6-n])
        self.held = []
        return bestcombo, bank


class FarkleGame:
    ''' Farkle game state 
    
        Args:
            human: Name of human player
            ainame: Name of computer/AI player
            points: Winning score
            triple_farkle: Penalty for farkling three times in a row
            openthreshold: Opening threshold for banking a turn
    '''
    def __init__(self,
                 player1='Human',
                 player2=AI_NAMES[0],
                 name1='Name',
                 name2='',
                 points=10000,
                 triple_farkle=1000,
                 openthreshold=500):
        
        self.players = []
        for name, player in zip((name1, name2), (player1, player2)):
            if player == 'Human':
                self.players.append(Player(
                    name, 
                    triple_farkle=triple_farkle,
                    threshold=openthreshold))
            elif player == AI_NAMES[0]:
                self.players.append(PlayerAI(
                    player, 
                    triple_farkle=triple_farkle,
                    threshold=openthreshold))                
            elif player == AI_NAMES[1]:
                self.players.append(Player2(
                    player, 
                    triple_farkle=triple_farkle,
                    threshold=openthreshold))                
            elif player == AI_NAMES[2]:
                self.players.append(Player3(
                    player, 
                    triple_farkle=triple_farkle,
                    threshold=openthreshold))                

        self.current_player = 0
        self.winscore = points

    def next_player(self):
        ''' Start the next player's turn '''
        self.current_player = (self.current_player+1) % len(self.players)
        self.player.newturn()

    @property
    def player(self):
        ''' Get the current player '''
        return self.players[self.current_player]

    @property
    def both_ai(self):
        ''' Both players are AI '''
        return self.players[0].is_ai and self.players[1].is_ai

    def wingame(self):
        ''' Game was won, update stats '''
        loser = self.players[self.current_player-1]
        GameStats.savescore(self.player.name, self.player.totalscore, self.player.bestbank,
                            loser.name, loser.totalscore, loser.bestbank)
