import pygame as pg 
from icecream import ic 

from .case import Case
from .pin import Pin


from utils.var import KEYS, PIN, MOVE, CASE, APPLY, WIDTH, STARTX, STARTY, OUT_SIZE, SPACING, HIGHLIGHT
from utils.function import gridify, draw_grid, color_cell, draw_cell_circle

class Grid:
    def __init__(self, rows: int, cols: int):
        self.__rows = rows
        self.__cols = cols
        self.__grid = [[Case((i, j)) for j in range(cols)] for i in range(rows)]
        self.__turn = 0

        self.__phase = PIN
        self.__players = None
        self.__pindex = None
        self.__selected_pin = None
        self.__move = "revive"
        self.__case_selected = None
       

    def __getitem__(self, index: tuple[int]) -> Case:
        """Get the case at the specified index."""
        if not (0 <= index[0] < self.__rows and 0 <= index[1] < self.__cols):
            raise IndexError("Index out of range")
        return self.__grid[index[0]][index[1]]
        
    def set_players(self, players):
        """Set the players of the game."""
        self.__players = players
        self.__pindex = 0
        self.__selected_pin = 0

    def __repr__(self):
        ... 

    def advance_turn(self):
        """Advance the turn of the game."""
        self.__turn += 1

    def get_turn(self) -> int:
        """Get the current turn."""
        return self.__turn

    def putPin():
        ...
        
    def random_case() -> Case:
        """Get a random case from the grid that doesnt contain any pin in it."""
        ...

    def get_neighbor_case(self, case, direction) -> Case:
        """
        Get the neighboring case in the specified direction.
        The direction is represented as an integer:
        0 - up, 1 - right, 2 - down, 3 - left.
        """

        ...

    def is_over(self) -> bool:
        return False
        """Check if the game is over. 
        The game is over if one of the players has all pins out of the grid."""
        for players in self.__players:
            lost = True
            for pin in players.pins:
                if pin.is_alive():
                    lost = False
                    break
            if lost:
                return True
        for line in self.__grid:
            for case in line:
                if case.is_empty():
                    return False
        
    def display_end(self, screen):
        ...

    def interprate(self, k, pos) -> tuple[int, int]:
        

        if self.__phase == PIN: 
            if k == pg.K_SPACE:
                self.__selected_pin = (self.__selected_pin + 1) % len(self.__players[self.__pindex].pins)
                
            elif k == pg.K_RETURN:
                self.__phase = MOVE

        elif self.__phase == MOVE:
            if k == pg.K_a:
                self.__move = "revive"
                self.__phase = CASE
            elif k == pg.K_s:
                self.__move = "move"
                self.__phase = CASE
            elif k == pg.K_d:
                self.__move = "invade"
                self.__phase = CASE
        
        elif self.__phase == CASE:
            # get the position of the mouse click
            x, y = gridify(pos[0], pos[1])
            self.__case_selected = self.__grid[x][y]
            self.__phase = APPLY
           
        
        elif self.__phase == APPLY: 
            player = self.__players[self.__pindex]
            res = self.apply_move(player.pins[self.__selected_pin],
                    self.__move, self.__case_selected,
                    player)
            self.initialize()
            self.advance_turn()
            self.__pindex = 1 - self.__pindex
            if res == False:
                return (1, 0) if self.__pindex == 0 else (0, 1)
        
        return (0, 0)
    
    def validate(self, x, y, move, pin_selected, name):
        if self.__players is None: return True 
        if move == "revive":
            if self.__grid[x][y].is_empty() and not self.__players[name].pins[pin_selected].is_alive():
                return True
            else: return False
        elif move == "move":
            for ox, oy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if not (0 < x + ox < self.__rows and 0 < y + oy < self.__cols):
                    continue
                if self.__grid[x + ox][y + oy].get_pin() is self.__players[name].pins[pin_selected]:
                    return True
            return False
        elif move == "invade":
            for ox, oy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if not (0 < x + ox < self.__rows and 0 < y + oy < self.__cols):
                    continue
                if self.__grid[x + ox][y + oy].case_side == name:
                    return True
            return False


    def initialize(self):
        """Initialize the game for the next turn."""
        self.__phase = PIN
        self.__case_selected = None
        self.__move = "revive"
        self.__selected_pin = 0

    def phase(self) -> int:
        return self.__phase

    def delta_move(self, key, pos) -> tuple[int, int]:
        ab = (0, 0)
        for k in KEYS.keys():
            if key[k]:
                if KEYS[k] == 0:
                    KEYS[k] = 1
                    ab = self.interprate(k, pos)
            else: 
                KEYS[k] = 0
        return ab[0], ab[1]

    def apply_move(self, pin: Pin, move: str, 
                   case: Case, player) -> bool:
        """
        Apply the move to the grid.
        the plauyer number is either 0 or 1.
        The move is a tuple of the form (pin, move, x, y).
        The pin is the pin number of the player, 
            the move is whether to move the pin or not ["revive", "move", "invade"],
        x, y are the coordinates of the case to move to or to invade.

        steps: 
        check if the move is valid
        apply it
        update the grid 
        """
        if move == "revive":
            self.revive(pin, case, player)

        elif move == "move":
            self.move(pin, case, player)

        elif move == "invade":
            self.invade(case, player)
        else:
            raise ValueError("Invalid move")

    def current_player_index(self) -> int:
        return self.__pindex

    def pin_selected(self) -> int:
        return self.__selected_pin

    def revive(self, pin: Pin, case: Case, player) -> bool:
    
        if pin.is_alive():
            return False
        # revive the pin at the position (x, y)
        if case.is_empty():
            case.case_side = player.name
            case.set_pin(pin)
            pin.revive()
            return True
        else:
            return False
        
    def move(self, pin: Pin, case: Case, player) -> bool:
            # if pin is not alive, return False

            if not pin.is_alive(): 
                return False
            # move the pin to the position (x, y)
            if not case.is_empty():
                return False
            # move the pin in a neighboring case to this case
            x, y = case.pos
            for (ox, oy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if not (0 < x + ox < self.__rows and 0 < y + oy < self.__cols):
                    continue
                self.__grid[x + ox][y + oy]
                if self.__grid[x + ox][y + oy].get_pin() is pin:
                    # remove the pin from the old case
                    self.__grid[x + ox][y + oy].remove_pin()
                    # put the pin in the new case
                    case.set_pin(pin)
                    case.case_side = player.name
                    return True
            return False

    def invade(self, case: Case, player):
        """
        test if that case have a neighbor case with the player side -> otherwise return False
        check if the case is not protected -> otherwise return False
        check if the case contains a pin in it -> if so, kill the pin, end your turn
        check if the case is already colorified -> if so, remove colorification, protected
        otherwise: colorify it with your color, and protect it
        """

        """
        Attempt to invade a case following the game rules

        Args:
            case: The target case to invade
            player: The player attempting the invasion
            
        Returns:
            bool: True if invasion was successful, False otherwise
        """
        # Check if case has a neighbor with player's side
        x, y = case.pos
        neighbor = False
        for (ox, oy) in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if not (0 < x + ox < self.__rows and 0 < y + oy < self.__cols):
                continue
           
            if self.__grid[x + ox][y + oy].case_side == player.name:
                neighbor = True
                break
        
        if not neighbor:
            ic("no neighbor color, invasion failed")
            return False 

        # Check if case is protected
        if case.protected(self.__turn):
            ic("case is protected, invasion failed")
            return False

        # Handle case with pin
        pin = case.get_pin()
        if pin is not None and pin not in player.pins:
            pin.kill()
            case.eliminate()
            ic("eliminated a pin, invasion succeded")
            return True

        # Handle already colored case
        if case.case_side == 1 - player.name:
            case.case_side = None 
            case.protect(self.__turn)
            ic("removed a color, invasion succeded")
            return True

        # Default invasion - color and protect
        case.case_side = player.name
        case.protect(self.__turn)
        ic("coloriying case, invasion succeded")
        return True

    def analyse(self):
        r_area_size = b_area_size = r_pins = b_pins = 0
        for line in self.__grid: 
            for case in line: 
                if case.case_side == 0:
                    r_area_size += 1
                    if case.get_pin() is not None:
                        r_pins += 1
                elif case.case_side == 1:
                    b_area_size += 1
                    if case.get_pin() is not None:
                        b_pins += 1
        return r_area_size, b_area_size, r_pins, b_pins

    def get_me(self):
        return self.__grid 

    def display(self, screen):
        """
        Display the grid on the screen.
        The grid is displayed as a 2D array of cases.
        Each case is represented by a rectangle with its color.
        """
        for i in range(self.__rows):
            for j in range(self.__cols):
                # self.__grid[i][j].display(screen)
                case = self.__grid[i][j]
                if case.case_side is not None:
                    color_cell(screen, i, j, self.__players[case.case_side].color)
                if not case.is_empty():
                    pin = case.get_pin()
                    if pin is self.__players[self.__pindex].pins[self.__selected_pin]:
                        color_cell(screen, i, j, HIGHLIGHT(self.__phase))
                    draw_cell_circle(screen, i, j)

        draw_grid(screen)

    def draw_pin(self, screen):
        """
        Draw the pin on the screen.''
        The pin is represented by a circle with its ''
        """
        self.__draw_pin_list(screen, self.__players[0])
        self.__draw_pin_list(screen, self.__players[1])

    def __draw_pin_list(self, screen, player):
        """
        Draw the pin list on the screen.
        The pin list is represented by a rectangle with its color.
        """
        if player.name == 0: start = STARTX 
        else: start = WIDTH - STARTX - OUT_SIZE
        for i, pin in enumerate(player.pins):
            if not pin.is_alive():
                if player.name == self.__pindex and i == self.__selected_pin:
                    color = HIGHLIGHT(self.__phase)
                else: color = player.color
                pg.draw.rect(screen, color, (start, i*(OUT_SIZE + SPACING) + STARTY, OUT_SIZE, OUT_SIZE))
                pg.draw.circle(screen, (0, 0, 0),  (start + OUT_SIZE//2, i*(OUT_SIZE + SPACING) + STARTY + OUT_SIZE//2), OUT_SIZE//4 - 2)