import random
import copy

# Typical BINGO card layout
CARD_LENGTH = 5  # 5x5 square card
COLUMN_RANGE = 15  # 15 numbers per column to choose from


class BingoCard:

    def __init__(self):

        bingo_cell = [0, False]

        self.bingo_card = [[bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                           [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                           [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                           [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell],
                           [bingo_cell, bingo_cell, bingo_cell, bingo_cell, bingo_cell]]

        # TODO: Better way to init card
        self.bingo_card2 = []

        for i in range(0, CARD_LENGTH):
            self.bingo_card2.append(bingo_cell)

        for j in range(0, CARD_LENGTH):
            self.bingo_card2.append(self.bingo_card2[0])

        under_b = range(1, COLUMN_RANGE + 1)
        under_i = range(COLUMN_RANGE + 1, COLUMN_RANGE * 2 + 1)
        under_n = range(COLUMN_RANGE * 2 + 1, COLUMN_RANGE * 3 + 1)
        under_g = range(COLUMN_RANGE * 3 + 1, COLUMN_RANGE * 4 + 1)
        under_o = range(COLUMN_RANGE * 4 + 1, COLUMN_RANGE * CARD_LENGTH + 1)

        self.under_all = range(1, COLUMN_RANGE * CARD_LENGTH + 1)

        random_b = random.sample(under_b, CARD_LENGTH)
        random_i = random.sample(under_i, CARD_LENGTH)
        random_n = random.sample(under_n, CARD_LENGTH)
        random_g = random.sample(under_g, CARD_LENGTH)
        random_o = random.sample(under_o, CARD_LENGTH)

        # Create random bingo card:
        for i in range(0, CARD_LENGTH):
            for j in range(0, CARD_LENGTH):

                if i == 0:
                    self.bingo_card[j][0] = [random_b[j], False]
                if i == 1:
                    self.bingo_card[j][1] = [random_i[j], False]
                if i == 2:
                    self.bingo_card[j][2] = [random_n[j], False]
                if i == 3:
                    self.bingo_card[j][3] = [random_g[j], False]
                if i == 4:
                    self.bingo_card[j][4] = [random_o[j], False]

        # TODO: is the middle cell FREE?
        # bingo_card[2][2] = [0, True]

        # print_bingo_card(bingo_card)
        self.marked_bingo_card = copy.deepcopy(self.bingo_card)

