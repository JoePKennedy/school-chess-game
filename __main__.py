import pygame
from pygame.locals import *

black_pawn = pygame.image.load('assets/black_pawn.png')
black_bishop = pygame.image.load('assets/black_bishop.png')
black_rook = pygame.image.load('assets/black_rook.png')
black_knight = pygame.image.load('assets/black_knight.png')
black_king = pygame.image.load('assets/black_king.png')
black_queen = pygame.image.load('assets/black_queen.png')
white_pawn = pygame.image.load('assets/white_pawn.png')
white_bishop = pygame.image.load('assets/white_bishop.png')
white_rook = pygame.image.load('assets/white_rook.png')
white_knight = pygame.image.load('assets/white_knight.png')
white_king = pygame.image.load('assets/white_king.png')
white_queen = pygame.image.load('assets/white_queen.png')

pieces = {"p":black_pawn,
          "b":black_bishop,
          "r":black_rook,
          "n":black_knight,
          "k":black_king,
          "q":black_queen,
          "P":white_pawn,
          "B":white_bishop,
          "R":white_rook,
          "N":white_knight,
          "K":white_king,
          "Q":white_queen
        }

pygame.init()
# Starts up pygame

display_width = 800
display_height = 800
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

    current_selection = 0
    # 0: Play game, 1: Customise Board

    def run_menu(self):
        for event in pygame.event.get():
            # Every time something happens
            if event.type == QUIT:
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
                return "board"

        screen.fill(Grey)
        # Make the screen grey

        play_button = Options("Play", 0.33)
        custom_button = Options("Custom Game", 0.66)
        play_button.draw()
        custom_button.draw()

        # Initialising the buttons then drawing them

        if self.current_selection is 0:
            pygame.draw.circle(screen, Black, (int(round(play_button.x - 55)),
                                               int(round(display_height * 0.75 + 10))), 5, 5)
        if self.current_selection is 1:
            pygame.draw.circle(screen, Black, (int(round(custom_button.x - 160)),
                                               int(round(display_height * 0.75 + 10))), 5, 5)

        # Moving a dot to show the selected

        pygame.display.flip()


class Board:
    def __init__(self, premade_list):
        self.premade_list = premade_list

    @staticmethod
    def draw_board():
        screen.fill(Grey)
        colour_flip = 0
        size = 100
        rect_pos_y = -size
        for rows in range(8):
            colour_flip = 1 - colour_flip
            rect_pos_x = size - size
            rect_pos_y += size
            for tiles in range(8):
                if colour_flip is 1:
                    pygame.draw.rect(screen, light_tile, (rect_pos_x, rect_pos_y, size, size))
                if colour_flip is 0:
                    pygame.draw.rect(screen, dark_tile, (rect_pos_x, rect_pos_y, size, size))
                rect_pos_x += 100
                colour_flip = 1 - colour_flip
        pygame.display.flip()

    def run_board(self):
        self.draw_board()
        for event in pygame.event.get():
            # Every time something happens
            if event.type == QUIT:
                return False

    def make_list(self):
        piece_list = []
        pieces = open("pieces.txt", "r")
        for rows in pieces.readlines():
            piece_list_rows = []
            for item in rows:
                piece_list_rows.append(item)
            piece_list.append(piece_list_rows)
        self.premade_list = piece_list


class Piece:
    def __init__(self, colour, pos, letter):
        self.colour = colour
        self.pos = pos
        self.sprite = None
        self.letter = letter

    def piece_colour(self):
        if self.letter.isupper() is True:
            self.colour = "Black"
        else:
            self.colour = "White"

    def set_piece(self):
        if self.letter is "p":
            self.sprite = white_pawn
        if self.letter is "r":
            self.sprite = white_rook
        if self.letter is "n":
            self.sprite = white_knight
        if self.letter is "b":
            self.sprite = white_bishop
        if self.letter is "q":
            self.sprite = white_queen
        if self.letter is "k":
            self.sprite = white_king
        if self.letter is "P":
            self.sprite = black_pawn
        if self.letter is "R":
            self.sprite = black_rook
        if self.letter is "N":
            self.sprite = black_knight
        if self.letter is "B":
            self.sprite = black_bishop
        if self.letter is "Q":
            self.sprite = black_queen
        if self.letter is "K":
            self.sprite = black_king

    def display_piece(self):
        screen.blit(self.sprite, self.pos)
        pygame.display.flip()

main_menu = Menu()
main_board = Board(None)
menu_running = True
board_running = False
arb_piece = Piece("white", (-14, -14))
while game_running:
    key_pressed = pygame.key.get_pressed()
    if menu_running is True:
        main_loop = main_menu.run_menu()
        if key_pressed[K_BACKQUOTE]:
            arb_piece.display_piece()
        if main_loop is False:
            menu_running = False
            game_running = False
            break
        elif main_loop is "board":
            menu_running = False
            board_running = True
    elif board_running is True:
        main_loop = main_board.run_board()
        if key_pressed[K_BACKQUOTE]:
            arb_piece.display_piece()
        if main_loop is False:
            board_running = False
            game_running = False


print("See ya")
pygame.quit()