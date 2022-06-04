import random
import copy

# Typical BINGO card layout
CARD_LENGTH = 5  # 5x5 square card
COLUMN_RANGE = 15  # 15 numbers per column to choose from


class BingoCard:

    def __init__(self, free_cell):

        bingo_cell = [0, False]

        self.bingo_card = [[bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                           [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                           [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                           [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                           [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell]]

        column_ranges = [[], [], [], [], []]
        column_random = [[], [], [], [], []]

        for i in range(0, CARD_LENGTH):
            column_ranges[i] = range(COLUMN_RANGE*i + 1, COLUMN_RANGE*(i+1) + 1)
            column_random[i] = random.sample(column_ranges[i], CARD_LENGTH)

        self.under_all = range(1, COLUMN_RANGE * CARD_LENGTH + 1)

        # Create random bingo card:
        for i in range(0, CARD_LENGTH):
            for j in range(0, CARD_LENGTH):
                self.bingo_card[j][i] = [column_random[i][j], False]

        # Is the middle cell FREE?
        if free_cell:
            self.bingo_card[2][2] = [0, True]

        self.marked_bingo_card = copy.deepcopy(self.bingo_card)

    # ------------------------------------------------------------------------

    def print_bingo_card(self, card):

        print('------------------------')
        print('|B | |I | |N | |G | |O |')
        print('------------------------')

        for i in range(0, CARD_LENGTH):

            if i > 0:
                print('\n------------------------')
            for j in range(0, CARD_LENGTH):
                print('|{:2}|'.format(card[i][j][True]), end=" ")

        print('\n------------------------\n\n')
