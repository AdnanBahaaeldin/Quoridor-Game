import random


class Board:

    def __init__(self, game_state=None, player1=None, player2=None, rows=9, columns=9, ):
        self.rows = rows
        self.columns = columns

        self.game_board = [['0' for _ in range(columns)] for _ in range(rows)]

        self.h_walls = [[False for _ in range(columns)] for _ in range(rows - 1)]  # False = no wall exists
        self.v_walls = [[False for _ in range(columns - 1)] for _ in range(rows)]  # False = no wall exists

        self.player2 = player2
        self.player1 = player1

        self.current_turn = random.choice([1, 2])

        self.game_state = game_state

    def get_game_board(self):
        return self.game_board

    def get_h_walls(self):
        return self.h_walls

    def get_v_walls(self):
        return self.v_walls

    def get_player1(self):
        return self.player1

    def get_player2(self):
        return self.player2

    def get_player2_pos(self):
        return self.player2.get_position()

    def get_player1_pos(self):
        return self.player1.get_position()

    def get_current_turn(self):
        return self.current_turn

    def set_h_walls(self, h_walls):
        self.h_walls = h_walls

    def set_v_walls(self, v_walls):
        self.v_walls = v_walls

    def set_player1(self, player1):
        self.player1 = player1

    def set_player2(self, player2):
        self.player2 = player2

    def set_current_turn(self, turn):
        self.current_turn = turn

    #####################MAIN LOGIC#####################

    ############Wall placement logic###########

    def is_wall_between(self, old_position, new_position):
        old_row, old_column = old_position
        new_row, new_column = new_position

        # Moving up
        if new_row == old_row - 1:
            return self.h_walls[new_row][old_column]

        # Moving down
        if new_row == old_row + 1:
            return self.h_walls[old_row][old_column]

        # Moving left
        if new_column == old_column - 1:
            return self.v_walls[old_row][new_column]

        # Moving right
        if new_column == old_column + 1:
            return self.v_walls[old_row][old_column]

        return False

    def can_place_horizontal_wall(self, row, column):
        if not self.is_inside_board((row, column)):
            return False

        if self.h_walls[row][column] or self.h_walls[row][column + 1]:
            return False

        if self.v_walls[row][column + 1]:
            return False

        return True

    def can_place_vertical_wall(self, row, column):
        if not self.is_inside_board((row, column)):
            return False

        if self.v_walls[row][column] or self.v_walls[row + 1][column]:
            return False

        if self.h_walls[row + 1][column]:
            return False

        return True

    def place_wall(self, orientation, row, column):

        if self.get_current_turn() == 1:
            if self.player1.get_number_of_walls() <= 0:
                return False, "No remaining walls for player 1"
            else:
                self.player1.set_number_of_walls(self.player1.get_number_of_walls() - 1)
        elif self.get_current_turn() == 2:
            if self.player2.get_number_of_walls() <= 0:
                return False, "No remaining walls for player 2."
            else:
                self.player2.set_number_of_walls(self.player2.get_number_of_walls() - 1)

        if orientation == 'h':
            if not self.can_place_horizontal_wall(row, column):
                return False, "Can't place wall in this position"
            self.h_walls[row][column] = True
            self.h_walls[row][column + 1] = True

        elif orientation == 'v':
            if not self.can_place_vertical_wall(row, column):
                return False, "Can't place wall in this position"
            self.v_walls[row][column] = True
            self.v_walls[row + 1][column] = True
        self.update_turn()
        self.game_state.save_state(self)
        return True

    ##################################################
    ############Movement logic###########

    def get_valid_moves(self, player_pos, opponent_pos):
        valid_moves = []

        directions = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1)
        }

        for distance_row, distance_column in directions.values():
            adjacent = (player_pos[0] + distance_row, player_pos[1] + distance_column)

            if not self.is_inside_board(adjacent):
                continue

            if self.is_wall_between(player_pos, adjacent):
                continue

            if adjacent != opponent_pos:
                valid_moves.append(adjacent)
                continue

            jump = (adjacent[0] + distance_row, adjacent[1] + distance_column)

            if self.is_inside_board(jump) and not self.is_wall_between(adjacent, jump):
                valid_moves.append(jump)
            else:
                if distance_row != 0:  # moving up/down → diagonals left/right
                    diagonals = [(adjacent[0], adjacent[1] - 1), (adjacent[0], adjacent[1] + 1)]
                else:  # moving left/right → diagonals up/down
                    diagonals = [(adjacent[0] - 1, adjacent[1]), (adjacent[0] + 1, adjacent[1])]

                for diagonal in diagonals:
                    if (self.is_inside_board(diagonal)
                            and not self.is_wall_between(adjacent, diagonal)):
                        valid_moves.append(diagonal)

        return valid_moves

    ##################################################
    ############Helper functions###########

    def update_turn(self):
        if self.current_turn == 1:
            self.current_turn = 2
        else:
            self.current_turn = 1

    def get_current_player(self):
        if self.current_turn == 1:
            return self.player1
        else:
            return self.player2

    def is_inside_board(self, position):
        row, column = position
        return 0 <= row < self.rows and 0 <= column < self.columns

    def update_player_position(self, player, new_player_pos):
        if player.get_symbol() == self.player1.get_symbol():
            self.player1.set_position(new_player_pos)
        else:
            self.player2.set_position(new_player_pos)

        self.update_turn()
        return self.game_state.save_state(self)

    def set_game_state(self, game_state):
        self.game_state = game_state




