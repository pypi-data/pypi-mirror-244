''' Textual UI for Farkle Game '''
from typing import Sequence, Optional
import time

from rich.text import Text
from textual.app import App, ComposeResult, RenderResult
from textual import events, on
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen, ModalScreen
from textual.widgets import (Button,
                             Digits,
                             Footer,
                             Header,
                             Input,
                             Label,
                             Rule,
                             Select,
                             Static,
                             Switch)

from .game import FarkleGame, AI_NAMES
from .scores import GameStats
from .screens import HelpScreen, StatsScreen


AI_DELAY = .75    # Seconds between AI button-clicking steps
AI_DELAY_SHORT = .05  # No delay needed
ROLL_SPEED = .1  # Time between each die roll coming up


class Die(Static, can_focus=True):
    ''' Single die
    
        Args:
            value: Value to display
    '''
    def __init__(self, value=6, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._value = value

    @property
    def value(self) -> int:
        ''' The current displayed value '''
        return self._value
    
    @value.setter
    def value(self, value: int) -> None:
        ''' Set the current displayed value '''
        self._value = value
        self.refresh()

    def render(self) -> RenderResult:
        ''' Draw the die '''
        text = {
            0: '',
            1: '\n  ●',
            2: '●\n\n    ●',
            3: '●\n  ●\n    ●',
            4: '●   ●\n\n●   ●',
            5: '●   ●\n  ●\n●   ●',
            6: '●   ●\n●   ●\n●   ●'}.get(self._value, '')
        return Text.assemble(text)


class DiceGroup(Static, can_focus=True):
    ''' Group of up to 6 dice '''
    BINDINGS = [
        Binding('1', action='hold(1)', description='Hold Die', key_display='1-6'),
        Binding('2', action='hold(2)', show=False),
        Binding('3', action='hold(3)', show=False),
        Binding('4', action='hold(4)', show=False),
        Binding('5', action='hold(5)', show=False),
        Binding('6', action='hold(6)', show=False),
        Binding('r', action='roll', description="Roll"),
        Binding('b', action='bank', description="Bank")]

    def compose(self) -> ComposeResult:
        with Horizontal(id='dielayout'):
            yield Die(1, id='die1')
            yield Die(2, id='die2')
            yield Die(3, id='die3')
            yield Die(4, id='die4')
            yield Die(5, id='die5')
            yield Die(6, id='die6')

    @property
    def num_visible(self) -> int:
        ''' Get the number of visible dice '''
        visible = [d.styles.display=='block' for d in self.query(Die)]
        return sum(visible)

    @num_visible.setter
    def num_visible(self, n: int) -> None:
        ''' Set the number of visible dice '''
        for i in range(n):
            self.query_one(f'#die{i+1}').styles.display = 'block'
        for i in range(n, 6):
            self.query_one(f'#die{i+1}').styles.display = 'none'
    
    @property
    def values(self):
        ''' Get values of all visible dice '''
        dice = self.query('Die')
        values = [d.value for d in dice if d.styles.display=='block']
        return values

    @values.setter
    def values(self, values: Sequence[int]):
        ''' Set the values of all visible dice '''
        dice = [d for d in self.query(Die) if d.styles.display=='block']
        assert len(dice) == len(values)
        for value, die in zip(values, dice):
            die.value = value

    def animate_roll(self, values: Sequence[int]) -> None:
        ''' Animate the roll '''

        def setval(die: Die, value: int) -> None:
            ''' Set the value of the die '''
            die.value = value

        dice = [d for d in self.query(Die) if d.styles.display=='block']
        for i, (die, value) in enumerate(zip(dice, values)):
            die.value = 0
            self.set_timer((i+1)*ROLL_SPEED, lambda d=die, v=value: setval(d, v), name='animatedice')

    @property
    def held(self) -> list[int]:
        ''' Get indexes of held dice '''
        dice = self.query('Die')
        return [i for i, die in enumerate(dice)
                if die.styles.display=='block' and die.has_class('held')]

    def clear_hold(self) -> None:
        ''' Clear the held dice '''
        dice = self.query('Die')
        for die in dice:
            die.remove_class('held')            


class Score(Static):
    ''' A widget with a name and score label
    
        Args:
            name: Label for the score
            value: Value of the score
    '''
    COMPONENT_CLASSES = {"score--active"}

    def __init__(self, name='Score:', value=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._score = value
        self._title = name

    @property
    def score(self) -> int:
        ''' Currently displayed score '''
        return self._score
    
    @score.setter
    def score(self, value) -> None:
        ''' Set the score to display '''
        self._score = value
        self.query_one('#score', Digits).update(str(self._score))

    def compose(self) -> ComposeResult:
        yield Label(self._title, id='scorelabel')
        yield Digits(str(self._score), id='score')


class ScoreBox(Static):
    ''' Box containing player's scores '''
    BORDER_TITLE = 'Game'
    
    def compose(self) -> ComposeResult:
        with Horizontal(id='scorelayout'):
            yield Score('Human:', 0, id='humanscore')
            yield Score('Computer:', 0, id='computerscore')


class TurnBox(Static):
    ''' Box containing the hold and turn score and roll/bank buttons '''
    BORDER_TITLE = 'Turn'
    def compose(self) -> ComposeResult:
        with Horizontal(id='scorelayout'):
            yield Score('Held:', 0, id='holdscore')
            yield Score('Turn Score:', 0, id='turnscore')
            yield Button('Roll', variant='primary', id='roll')
            yield Button.success('Bank', id='bank')


class FarkleMessage(ModalScreen[int]):
    ''' Show message when Farkled '''
    def compose(self) -> ComposeResult:
        yield Button('Farkle!', variant='error', id='farkleok')
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        ''' Clear the message '''
        self.dismiss(0)


class TripleFarkleMessage(ModalScreen[int]):
    ''' Show message when triple-farkled '''
    def __init__(self, penalty: int = 1000):
        super().__init__()
        self.penalty = penalty

    def compose(self) -> ComposeResult:
        yield Button(f'Triple Farkle! Lose {self.penalty} points!', variant='error', id='triplefarkleok')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        ''' Clear the message '''
        self.dismiss(0)


class WinMessage(ModalScreen[int]):
    ''' Show message when the game is won '''
    def __init__(self, playername: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.playername = playername

    def compose(self) -> ComposeResult:
        yield Button(f'{self.playername} Wins!',
                     variant='error')
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        ''' Clear the message '''
        self.dismiss(0)


class NewGame(Screen[dict]):
    ''' Dialog to set up a new game

        Args:
            setup: Parameters entered last time the dialog was used    
    '''
    BORDER_TITLE = 'Welcome to Farkle!'

    def __init__(self, setup: Optional[dict[str, str]] = None):
        super().__init__()
        self.setup: dict[str, str] = setup if setup else {}

    def compose(self) -> ComposeResult:
        name1 = self.setup.get('name1', '')
        name2 = self.setup.get('name2', '')
        player1 = self.setup.get('player1', 'Human')
        player2 = self.setup.get('player2', 'Super Sally')
        points = self.setup.get('points', 10000)
        triple = self.setup.get('triple_farkle', 1000)
        thresh = True if self.setup.get('openthreshold', 500) == 500 else False
        names = ['Human'] + AI_NAMES

        yield Label('Player 1')
        yield Label('Player 2')
        yield Select(zip(names, names), value=player1, id='player1', allow_blank=False)
        yield Select(zip(names, names), value=player2, id='player2', allow_blank=False)
        yield Input(name1, placeholder='Name', id='name1')
        yield Input(name2, placeholder='Name', id='name2', disabled=True)
        yield Rule()
        yield Label('Points to win:')
        yield Label('Triple Farkle Penalty:')
        yield Select((('500', 500), ('5000', 5000), ('10000', 10000), ('15000', 15000), ('20000', 20000)),
                     value=points,
                     allow_blank=False,
                     prompt='Points to Win', id='pointstowin')
        yield Select((('0', 0), ('500', 500), ('1000', 1000)),
                     value=triple,
                     allow_blank=False,
                     prompt='Triple-Farkle Penalty', id='triplefark')
        with Vertical():
            yield Label('500-point opening threshold:', id='switch')
            yield Switch(value=thresh, name='500-Point Opening Threshold', id='openthresh')
        yield Button('Start', variant='primary', id='startbutton')
        yield Footer()

    def on_select_changed(self, event: Select.Changed) -> None:
        ''' Enable/disable the Name field when changing from human to AI player '''
        if event.select.id == 'player1':
            self.query_one('#name1', Input).disabled = (event.value != 'Human')
        elif event.select.id == 'player2':
            self.query_one('#name2', Input).disabled = (event.value != 'Human')

    def on_button_pressed(self, event: Button.Pressed) -> None:
        ''' Submit the dialog '''
        setup = {'player1': self.query_one('#player1', Select).value,
                 'player2': self.query_one('#player2', Select).value,
                 'name1': self.query_one('#name1', Input).value,
                 'name2': self.query_one('#name2', Input).value,
                 'points': int(str(self.query_one('#pointstowin', Select).value)),
                 'triple_farkle': int(str(self.query_one('#triplefark', Select).value)),
                 'openthreshold': 500 if self.query_one('#openthresh', Switch).value else 0}
        self.dismiss(setup)


class Farkle(App):
    ''' Main Farkle App '''
    CSS_PATH = 'farkle.css'
    SCREENS = {'help': HelpScreen()}
    BINDINGS = [('d', 'toggle_dark', 'Toggle dark mode'),
                ('f1', 'push_screen("help")', 'Help'),
                ('f2', 'show_stats', 'Statistics')]

    def __init__(self):
        super().__init__()
        self.game = None
        self.gamesetup = {}

    def compose(self) -> ComposeResult:
        yield Header()
        yield DiceGroup(id='dice')
        yield TurnBox()
        yield ScoreBox()
        yield Footer()

    def on_mount(self):
        ''' Request a new game when the app starts '''
        self.newgame()

    def setupgame(self, setup: dict[str, int]) -> None:
        ''' Set up a new game '''
        self.gamesetup = setup
        self.game = FarkleGame(**setup)
        self._start_game()

    def newgame(self) -> None:
        ''' Show the new game setup screen '''
        self.push_screen(NewGame(self.gamesetup), self.setupgame)

    def on_key(self, event: events.Key) -> None:
        ''' Key was pressed '''
        if self.screen.id == '_default' and not self.game.player.is_ai:
            if event.key == 'left':
                self.screen.focus_previous()
            elif event.key == 'right':
                self.screen.focus_next()
            elif (event.key in ['space', 'enter'] and
                    self.screen.focused and
                    self.screen.focused.id and
                    self.screen.focused.id.startswith('die')):
                self._hold(int(self.screen.focused.id[-1]))
            elif (event.key == 'space' and
                    self.screen.focused and
                    self.screen.focused.id in ['roll', 'bank']):
                # Allow space to activate buttons
                self.screen.focused.action_press()  # type: ignore

    def on_click(self, event: events.Click) -> None:
        ''' Mouse was clicked '''
        if (self.screen.id == '_default' and
                not self.game.player.is_ai and
                self.screen.focused and
                self.screen.focused.id and
                self.screen.focused.id.startswith('die')):
            self._hold(int(self.screen.focused.id[-1]))

    def _farkle(self, n: int) -> None:
        ''' Farkle screen was cleared '''
        self.query_one('#holdscore', Score).score = 0
        self.query_one('#turnscore', Score).score = 0
        self.screen.set_focus(self.query_one(DiceGroup))
        self.query_one('#bank', Button).disabled = True
        if self.game.current_player == 0:
            self.query_one('#humanscore', Score).score = self.game.player.totalscore
        else:
            self.query_one('#computerscore', Score).score = self.game.player.totalscore
        self._next_player()

    def _roll(self):
        ''' Process Roll Command '''
        if self.game.player.is_ai:
            time.sleep(AI_DELAY)

        dicegroup = self.query_one(DiceGroup)
        if dicegroup.num_visible == 0:
            dicegroup.num_visible = 6

        roll = self.game.player.rollem()
        dicegroup.clear_hold()
        dicegroup.num_visible = self.game.player.inplay
        dicegroup.animate_roll(roll)
        self.set_timer((dicegroup.num_visible+1)*ROLL_SPEED, self._rolldone)

    def _rolldone(self):
        ''' Done with the roll '''
        if self.game.player.is_farkle:
            if (self.game.player.triple_farkle > 0 and
                    self.game.player.farkles_in_a_row == 3):
                self.push_screen(TripleFarkleMessage(self.game.player.triple_farkle), self._farkle)
                self.game.player.farkles_in_a_row = 0
            else:
                self.push_screen(FarkleMessage(), self._farkle)

        else:
            self.query_one('#holdscore').score = 0
            self.query_one('#turnscore').score = self.game.player.turnscore
            self.query_one('#roll').disabled = True
            self.screen.set_focus(self.query_one(DiceGroup))
            self.query_one('#bank').disabled = True

    @on(Button.Pressed, "#roll")
    def roll(self, event: Button.Pressed) -> None:
        ''' Roll when the button was pressed '''
        self._roll()

    def action_roll(self) -> None:
        ''' Roll when the hotkey was pressed '''
        if not self.game.player.is_ai and self.game.player.can_roll:
            self._roll()

    def _hold(self, num: int) -> None:
        ''' Hold the die with index num '''
        self.query_one(f'#die{num}', Die).toggle_class('held')
        held = self.query_one(DiceGroup).held
        holdscore = self.game.player.hold(held)
        self.query_one('#holdscore', Score).score = holdscore
        self.query_one('#bank', Button).disabled = not self.game.player.can_bank
        self.query_one('#roll', Button).disabled = not self.game.player.can_roll

    def action_hold(self, num: int) -> None:
        ''' Hold the die when hotkey was pressed '''
        if not self.game.player.is_ai:
            self._hold(num)

    def _bank(self) -> None:
        ''' Bank the turn '''
        if self.game.player.is_ai:
            time.sleep(AI_DELAY)

        self.game.player.bank()
        self.query_one('#holdscore', Score).score = 0
        self.query_one('#turnscore', Score).score = 0
        if self.game.current_player == 0:
            self.query_one('#humanscore', Score).score = self.game.player.totalscore
        else:
            self.query_one('#computerscore', Score).score = self.game.player.totalscore

        if self.game.player.totalscore >= self.game.winscore:
            self._win(self.game.player)
        else:
            self._next_player()

    def action_bank(self) -> None:
        ''' Bank the turn when hotkey was pressed '''
        if self.game.player.can_bank and not self.game.player.is_ai:
            self._bank()

    @on(Button.Pressed, "#bank")
    def bank(self, event: Button.Pressed) -> None:
        ''' Bank the turn when button was pressed '''
        self._bank()

    def _start_game(self):
        ''' Start a new game '''
        self.query_one(TurnBox).border_title = f"{self.game.player.name}'s Turn"
        self.query_one(DiceGroup).num_visible = 0
        self.query_one('#roll').disabled = False
        self.query_one('#bank').disabled = True
        self.query_one('#humanscore').add_class('scoreactive')
        self.query_one('#computerscore').remove_class('scoreactive')
        self.query_one('#humanscore').score = 0
        self.query_one('#computerscore').score = 0
        self.query_one('#humanscore Label').update(self.game.players[0].name)
        self.query_one('#computerscore Label').update(self.game.players[1].name)
        if self.game.player.is_ai:
            self._aiturn()

    def _next_player(self):
        ''' Go to the next player '''
        self.game.next_player()
        self.query_one(TurnBox).border_title = f"{self.game.player.name}'s Turn"
        self.query_one(DiceGroup).clear_hold()
        self.query_one(DiceGroup).num_visible = 0
        self.query_one('#roll').disabled = False
        self.query_one('#bank').disabled = True
        if self.game.current_player == 0:
            self.query_one('#humanscore').add_class('scoreactive')
            self.query_one('#computerscore').remove_class('scoreactive')
        else:
            self.query_one('#computerscore').add_class('scoreactive')
            self.query_one('#humanscore').remove_class('scoreactive')
        
        if self.game.player.is_ai:
            self._aiturn()
    
    def _win(self, player) -> None:
        ''' Game is won. Show a message. '''
        def done(n: int) -> None:
            self.push_screen(NewGame(self.gamesetup), self.setupgame)

        self.game.wingame()
        self.push_screen(WinMessage(player.name), done)

    def _aiturn(self):
        ''' Process turn by AI player '''
        self.set_timer(AI_DELAY, self._airoll, name='airoll')

    def _airoll(self):
        ''' Process AI player roll '''
        self.query_one('#roll', Button).action_press()
        self.set_timer(AI_DELAY*2, self._ai_getholds, name='aigetholds')

    def _ai_getholds(self):
        ''' Get AI player holds '''
        if not self.game.player.is_farkle and self.game.player.is_ai:
            # Should always be is_ai here, unless human
            # was cheating and hitting the buttons during the AI's turn
            # (which I haven't found a good way to block)...
            holds, bank = self.game.player.ai_holds()
            self.set_timer(AI_DELAY, lambda h=holds, b=bank: self._aihold(h, b), name='aihold')

    def _aihold(self, holds: list[int], bank: bool=False):
        ''' Process AI player holds/animation and either bank or roll again '''
        if len(holds):
            thishold, *holds = holds
            self._hold(thishold+1)
            delay = AI_DELAY if len(holds) else AI_DELAY_SHORT
            self.set_timer(delay, lambda h=holds, b=bank: self._aihold(h, b), name='aihold')
        elif bank:
            self.set_timer(AI_DELAY, self._aibank)
        else:  # roll again
            self.set_timer(AI_DELAY, self._airoll, name='airoll')

    def _aibank(self) -> None:
        ''' AI player decided to bank '''
        self.query_one('#bank', Button).action_press()

    def action_show_stats(self) -> None:
        ''' Show the statistics screen '''
        self.push_screen(StatsScreen())

    def action_clearscores(self) -> None:
        ''' Clear the statistics '''
        GameStats.clearstats()
        self.pop_screen()
        self.push_screen(StatsScreen())
    
    def action_toggle_dark(self) -> None:
        ''' Toggle dark mode '''
        self.dark = not self.dark


def main():
    app = Farkle()
    app.run()


if __name__ == "__main__":
    main()