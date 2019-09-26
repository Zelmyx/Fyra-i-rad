import pygame
import numpy as np


class GameBackEnd:
    """This class handles the game backend."""

    def __init__(self, row_count, column_count, max_count):
        self.row_count = row_count
        self.column_count = column_count
        self.max_count = max_count
        self.board = np.zeros((self.row_count, self.column_count), 
                                dtype=int)
        self.colswitch = self.create_column_switch()

    def create_column_switch(self):
        """Flip the columns for easier diagonal checking."""

        n = len(self.board[0])
        list1 = [i for i in range(0, n)]
        list2 = [i for i in range(n - 1, -1, -1)]
        colswitch = {l1: l2 for l1, l2 in zip(list1, list2)}

        return colswitch

    def check_move(self, col):
        """Check if column is full."""

        for i in range(len(self.board) - 1, -1, -1):
            if self.board[i][col] == 0:
                return i

        return "Full"

    def check_for_win(self, row, col, player):
        """Check if max_count is reached.""" 

        count = 0
        for i in range(0, len(self.board[0])):
            # Check vertical
            if self.board[row][i] == player:
                count += 1
            else:
                count = 0
            
            if count == self.max_count:
                return True

        count = 0
        for i in range(0, len(self.board)):
            # Check horisontal
            if self.board[:, col][i] == player:
                count += 1
            else:
                count = 0
            
            if count == self.max_count:
                return True
        
        count = 0
        totoffset = col - row
        for i in np.diagonal(self.board, offset=totoffset):
            # Check diagonal
            if i == player:
                count += 1
            else:
                count = 0

            if count == self.max_count:
                return True

        count = 0
        mirrorboard = np.fliplr(self.board)
        col = self.colswitch[col]
        totoffset = col - row
        for i in np.diagonal(mirrorboard, offset=totoffset):
            # Check other diagonal
            if i == player:
                count += 1
            else:
                count = 0

            if count == self.max_count:
                return True
        
    def game_tie(self):
        """Check if the board is full."""

        shape = self.board.shape
        if np.count_nonzero(self.board) == (shape[0] * shape[1]):
            # The board is full
            player = 0
            return True
        else:
            return False

        

class GameUserInterface(GameBackEnd):
    """This class handels the frontend (pygame) aspects of the game."""

    def __init__(self, row_count, column_count, 
                    max_count, box_length, y_offset):
        super().__init__(row_count, column_count, max_count)
        self.box_length = box_length
        self.display_height = self.row_count * self.box_length
        self.display_width = self.column_count * self.box_length
        self.y_offset = y_offset
        pygame.init()
        pygame.display.set_caption("Connect {self.max_count}")
        clock = pygame.time.Clock()
        clock.tick(30)
        self.black = (0, 0, 0)
        self.game_display = pygame.display.set_mode((self.display_width, 
                                                    self.display_height
                                                    + self.y_offset))
        self.game_display.fill(self.black)

    def draw_board(self):
        """Draw the board."""

        for c in range(self.column_count):
            for r in range(self.row_count):
                bild = pygame.image.load("etc/board_square.png")
                # Scale the game board
                bild = pygame.transform.scale(bild, (self.box_length, 
                                                        self.box_length))
                self.game_display.blit(bild, (c * self.box_length, 
                                        r * self.box_length 
                                        + self.y_offset))

    def display_message(self, text, color, text_size, coordinates):
        """Show a message on the display."""

        if text_size == "large":
            text_size = 100
        elif text_size == "normal":
            text_size = 60
            
        text_style = pygame.font.Font("etc/Roboto-Regular.ttf", text_size)
        text_surface, text_rect = self.text_objects(text, text_style, color)
        text_rect.center = coordinates
        self.game_display.blit(text_surface, text_rect)
        pygame.display.update()

    def text_objects(self, text, font, color):
        """Make a surface to draw the text onto."""

        text_surface = font.render(text, True, color)
        return text_surface, text_surface.get_rect()
    
    def delete_text(self, color, coord, coord_):
        """Delete selected text by drawing a square over it."""

        pygame.draw.rect(self.game_display, color, ((coord), (coord_)))
        pygame.display.update()

    def display_coin(self, player, row, column):
        """Draws the moves to the screen."""

        coin_1_img = pygame.image.load("etc/yellow.png")
        coin_2_img = pygame.image.load("etc/red.png")
        # Scale images to fit the game board
        coin_1_img = pygame.transform.scale(coin_1_img, (self.box_length, 
                                            self.box_length))
        coin_2_img = pygame.transform.scale(coin_2_img, (self.box_length, 
                                            self.box_length))
        
        if player == 1:
            coin_img = coin_1_img
        elif player == 2:
            coin_img = coin_2_img

        self.game_display.blit(coin_img, ((column * self.box_length), 
                                ((row * self.box_length) + self.y_offset)))