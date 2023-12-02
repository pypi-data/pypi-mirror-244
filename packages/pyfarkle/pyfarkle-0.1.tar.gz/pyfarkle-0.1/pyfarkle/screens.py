''' Screens for Farkle App '''
from textual.screen import Screen
from textual.app import ComposeResult
from textual.widgets import MarkdownViewer, Footer

from .scores import GameStats

AI_NAMES = ['Super Sally', 'Happy Harry', 'Maniacal Matt']


HELP_MD = '''
# Farkle

## How to play

- Roll 6 dice
- Set aside combinations which have scoring value (see below)
- Either bank the points set aside, or roll the remaining dice
    * Banking the points adds the score to the player's total and ends the player's turn
    * If player rolls remaining dice, but obtains no scoring combinations,
       they have *Farkled* and lose all points from the current turn.
- If all 6 dice score, then the player continues by rolling
  all 6 dice again, building up the score for the turn.
- After either banking or Farkling, the turn is over and the next player rolls.
- The winner is the first player to reach 10,000 points

Options:
- 500-point opening threshold: The player must bank at least 500 points on their first bank.
- Points-to-win: Change the number of points required to win the game
- Triple-Farkle: Lose 1000 points for Farkling three times in a row


## Scoring Combinations

- 1: 100 points
- 5: 50 points
- 3-of-a-kind of 1's: 1000 points
- 3-of-a-kind: 100 times face value
- 4-of-a-kind: 2 times the 3-of-a-kind value
- 5-of-a-kind: 3 times the 3-of-a-kind value
- 6-of-a-kind: 4 times the 3-of-a-kind value
- 3 pairs: 750 points
- Straight of 6: 1000 points


## Computer Player Profiles

### Super Sally

This player takes all points possible from a roll and banks whenever 2 or fewer die remain to roll, or if this turn exceeded the opening threshold.

### Happy Harry

This player takes all points possible from a roll and banks if they have more than 750 points regardless of die remaining or turn score.

### Maniacal Matt

This player uses the strategy described in a blog post by Maniacal Matt.
The strategy maximizes the average expected score per turn.
http://www.mattbusche.org/blog/article/zilch/.
'''


class HelpScreen(Screen):
    ''' Show game help '''
    BINDINGS = [("escape", "app.pop_screen", "Close")]
    def compose(self) -> ComposeResult:
        yield MarkdownViewer(HELP_MD)##, show_table_of_contents=False)
        yield Footer()



TEMPLATE_HDR = '''
## {player}

| Opponent | Wins | Games | Percent |
|----------|------|-------|---------|
'''
TEMPLATE_ROW = '''| {opponent} | {wins} | {total} | {percent:.1f} % |\n'''
TOP_5_TEMPLATE = '''
| Player | Score |
|--------|-------|
'''
TOP5_ROW = '| {player} | {score} |\n'


class StatsScreen(Screen):
    ''' Show game statistics '''
    BINDINGS = [("escape", "app.pop_screen", "Close"),
                ('exclamation_mark', 'clearscores', 'Clear Stats')]  # Let this one bubble to App

    def compose(self) -> ComposeResult:
        stats = GameStats()

        md = '# Statistics\n'  # Human players only
        for player, opponents in stats.winrates().items():
            if player not in AI_NAMES:
                md += TEMPLATE_HDR.format(player=player)
                for opponent, vals in opponents.items():
                    md += TEMPLATE_ROW.format(opponent=opponent,
                                              total=vals.total,
                                              wins=vals.wins,
                                              percent=vals.percent)
                bestturn = stats.bestbank(player)
                bestscore = stats.bestscore(player)
                md += f'\n- Highest Score: {bestscore}\n'
                md += f'\n- Highest Turn Banked: {bestturn}\n'

        md += '\n\n' + '# Top 5 Scoring Games\n'
        md += TOP_5_TEMPLATE
        for score in stats.high_scores[:5]:
            md += TOP5_ROW.format(player=score.player,
                                  score=score.score)

        md += '\n\n' + '# Top 5 Turns Banked\n'
        md += TOP_5_TEMPLATE
        for score in stats.high_turnscores[:5]:
            md += TOP5_ROW.format(player=score.player,
                                  score=score.bestbank)

        md += '# Computer Players'
        for player, opponents in stats.winrates().items():
            if player in AI_NAMES:
                md += TEMPLATE_HDR.format(player=player)
                for opponent, vals in opponents.items():
                    md += TEMPLATE_ROW.format(opponent=opponent,
                                              total=vals.total,
                                              wins=vals.wins,
                                              percent=vals.percent)
                bestturn = stats.bestbank(player)
                bestscore = stats.bestscore(player)
                md += f'\n- Highest Score: {bestscore}\n'
                md += f'\n- Highest Turn Banked: {bestturn}\n'

        md += '\n\n---\n\n'
        md += f'Scores saved to {GameStats.STATSPATH}\n'

        yield MarkdownViewer(md)
        yield Footer()
