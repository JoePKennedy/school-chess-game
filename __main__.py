import pygame
from pygame.locals import *
import random

pygame.init()
# Starts up pygame

display_width = 1600
display_height = 900
screen = pygame.display.set_mode((display_width, display_height))
# Allows screen resolution to be changed, and sets the resolution

Black = 0, 0, 0
Grey = 120, 120, 120
light_tile = 255, 205, 160
dark_tile = 210, 140, 70
light_highlight = 40, 200, 150
dark_highlight = 25, 130, 65
# Just some colours

game_running = True
# Will be set false to end game

clock = pygame.time.Clock()
clock.tick(60)

font = pygame.font.Font(None, 32)


class Options:
    def __init__(self, string, width):
        self.string = string
        # The word to be written
        self.width = width
        # Percentage into the screen
        x = display_width * width
        # Where to place it on the screen
        self.x = x
    # Initialising variables, making x accessible outside of the class

    def draw(self):
        text = font.render(self.string, True, (0, 0, 0))
        screen.blit(text, (self.x - text.get_width(), display_height * 0.75))
    # Draws the button


class Menu(Options):
    def __init__(self):
        Options.__init__(self, string="", width=0)
        self.running = True

    current_selection = 0
    """
    Selection options
    0 = Create A Deck; 1 = Play, 2 = Open Packs
    """
    def run_menu(self):
        key_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            # Every time something happens
            if event.type == QUIT:
                self.running = False
                return False
                # If that something is they want to quit, end the game
        if key_pressed[K_LEFT]:
            if self.current_selection != 0:
                self.current_selection -= 1
                print(self.current_selection)
                # Increments option by 1
        if key_pressed[K_RIGHT]:
            if self.current_selection != 1:
                self.current_selection += 1
                print(self.current_selection)
        if key_pressed[K_RETURN]:
            if self.current_selection is 0:
                self.running = False
                return "board"


        screen.fill(Grey)
        # Make the screen grey

        play_button = Options("Play", 0.33)
        custom_button = Options("Custom Game", 0.66)
        play_button.draw()
        custom_button.draw()

        # Initialising the buttons then drawing them

        if self.current_selection is 0:
            pygame.draw.circle(screen, Black, (int(round(play_button.x - 55)), int(round(display_height * 0.75 + 10))), 5, 5)
        if self.current_selection is 1:
            pygame.draw.circle(screen, Black, (int(round(custom_button.x - 160)), int(round(display_height * 0.75 + 10))), 5, 5)

        # Moving a dot to show the selected

        pygame.display.flip()

class Tile:

    def __init__(self, colour, row, column):
        self.colour = colour
        self.row = row
        self.column = column

    def draw_tile(self):
        if self.colour is "light":\
            pygame.draw.rect(screen, light_tile, ((self.row * 110), (self.column * 110), 110, 110))
        elif self.colour is "dark":
            pygame.draw.rect(screen, dark_tile, ((self.row * 110), (self.column * 110), 110, 110))
        if self.colour is "h-light":\
            pygame.draw.rect(screen, light_highlight, ((self.row * 110), (self.column * 110), 110, 110))
        elif self.colour is "h-dark":
            pygame.draw.rect(screen, dark_highlight, ((self.row * 110), (self.column * 110), 110, 110))


class Board(Tile):
    def __init__(self):
        Tile.__init__(self, colour="", row=-1, column=-1)
        self.running = True

    def make_board(self):
        board = []
        colour_change = 0
        for i in range(8):
            board_y = []
            colour_change = 1 - colour_change
            for i in range(8):
                board_y.append(colour_change)
                colour_change = 1 - colour_change
            board.append(board_y)
        return board

    def draw_board(self, board):
        screen.fill(Grey)
        tile_pos = -1
        for row in board:
            column_number = -1
            tile_pos += 1
            for tile in row:
                column_number += 1
                if tile == 0:
                    new_tile = Tile("light", tile_pos, column_number)
                    new_tile.draw_tile()
                elif tile == 1:
                    new_tile = Tile("dark", tile_pos, column_number)
                    new_tile.draw_tile()
        for event in pygame.event.get():
            # Every time something happens
            if event.type == QUIT:
                self.running = False
                return False

        pygame.display.flip()

    def highlight_tiles(self, board, row, column):
        if board[row][column] is 0:
            highlighted_tile = Tile("h-light", row, column)
            highlighted_tile.draw_tile()
        elif board[row][column] is 1:
            highlighted_tile = Tile("h-dark", row, column)
            highlighted_tile.draw_tile()

"""
What I want to do:
    When a piece is clicked on, highlight the valid squares it can move to
What's needed:
    Piece position
    Current state of the board (Where things literally are)
    *Variating Factors (Check, En Passant, Castling)
    How the piece can move
Where to get these:
    Piece class
    play board list
    a scary place
    individual piece class
Ignoring variation, it can be done at each level instead of one grouped function
    Click on Piece
    Function that takes movement as parameters?
"""
class Piece:
    def __init__(self, colour, pos_x, pos_y):
        self.colour = colour
        self.pos_x = pos_x
        self.pos_y = pos_y

    def piece_taken(self):
        del self

    def piece_moved(self, new_pos_x, new_pos_y):
        self.pos_x = new_pos_x
        self.pos_y = new_pos_y


class Pawn(Piece):
    def __init__(self):
        Piece.__init__(self, colour=self.colour, pos_x=self.pos_x, pos_y=self.pos_y)
        self.has_moved = False


def create_board(inital_board):
    counter = -1
    for rows in inital_board:
        counter += 1
        y_counter = -1
        for items in rows:
            y_counter += 1
            inital_board[counter][y_counter] = None
    new_board = inital_board
    return new_board

board_setup = Board
board_template = board_setup.make_board(board_setup)
play_board = create_board(board_template)
main_menu = Menu()
menu_running = True
board_running = False
while game_running:
    key_pressed = pygame.key.get_pressed()
    if menu_running is True:
        main_loop = main_menu.run_menu()
        if main_loop is False:
            menu_running = False
            game_running = False
            break
        elif main_loop is "board":
            menu_running = False
            board_running = True
    elif board_running is True:
        main_loop = board_setup.draw_board(board_setup, board_template)
        if key_pressed[K_BACKQUOTE]:
            board_setup.highlight_tiles(board_setup, board_template, 0, 0)
            print(board_template)
        if main_loop is False:
            menu_running = False
            game_running = False
            break


"""
test = Board
new_board = test.make_board(test)
menu_running = True
while game_running:
    main_loop = test.draw_board(test, new_board)
    if main_loop is False:
        break
"""
print("See ya")
pygame.quit()
