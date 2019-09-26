import sys
import pygame
import numpy as np
from backend import GameBackEnd, GameUserInterface


row_count = 6
column_count = 7
max_count = 4       # 4 for Connect Four, 5 for Connect Five etc.
box_length = 100    # How big every "square" is (px)
y_offset = 140      # Black area on top (px)

display_width = column_count * box_length
display_heigth = row_count * box_length

yellow = (255, 255, 0)
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

key_dict = {
    49: 0,  # Button 1 --> Column 0
    50: 1,  # Button 2 --> Column 1
    51: 2,  # Button 3 --> Column 2
    52: 3,  # Button 4 --> Column 3
    53: 4,  # Button 5 --> Column 4
    54: 5,  # Button 6 --> Column 5
    55: 6,  # Button 7 --> Column 6
}


def main():
    """Main game function. 
    Handles all game logic.
    """
    Game_BE = GameBackEnd(row_count, column_count, max_count)
    Game_UI = GameUserInterface(row_count, column_count, 
                                max_count, box_length, 
                                y_offset)
    board = Game_BE.board
    Game_UI.draw_board()
    game_over = False
    turn = 0

    # Main loop
    while not game_over:
        if turn % 2 == 0:
            player = 1
            color = yellow
        else:
            player = 2
            color = red

        # Display current player
        Game_UI.delete_text(black, (0, 0), (display_width, y_offset))
        Game_UI.display_message(f"Player {player}'s turn!", color, "large",
                                ((display_width / 2), (y_offset / 2)))

        # Looping over every event (button press)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key in key_dict:
                column = key_dict[event.key]

                if Game_BE.check_move(column) == "Full":
                    # Column is full
                    pass
                else:
                    # Drop and draw piece to the screen
                    row = Game_BE.check_move(column)
                    board[row][column] = player
                    Game_UI.display_coin(player, row, column)

                    # Check for win
                    if Game_BE.check_for_win(row, column, player):
                        Game_UI.delete_text(black, (0, 0), 
                                        (display_width, y_offset))
                        Game_UI.display_message(f"Player {player} won!", 
                                            color, "normal", 
                                            ((display_width / 2), 40))
                        game_over = True

                    # Check for tie
                    elif Game_BE.game_tie():
                        Game_UI.delete_text(black, (0, 0), 
                                            (display_width, y_offset))
                        Game_UI.display_message("That's a tie!", white, 
                                                "normal", 
                                                ((display_width / 2), 40))
                        game_over = True

                    turn += 1
                    break

    while game_over:
        Game_UI.display_message("Play again? Yes/No", white, "normal", 
                                ((display_width / 2), 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key in (121, 110):
                # Ask for another game (121 = (Y)es, 110 = (N)o)
                if event.key == 121:    # Play again
                    game_over = False
                    main()
                else:   # Quit
                    pygame.quit()
                    sys.exit()


main()