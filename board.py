import random

class Board:
    def __init__(self, rows=9, columns=9):
        self.rows = rows
        self.columns = columns

        self.game_board = [['0' for _ in range(columns)] for _ in range(rows)]

        self.h_walls = [[False for _ in range(columns)] for _ in range(rows-1)] #False = no wall exists
        self.v_walls = [[False for _ in range(columns-1)] for _ in range(rows)] #False = no wall exists

        self.current_turn = random.randint(0, 1)

    def set_board_state(self, board, h_walls, v_walls, turn):
        self.game_board = board
        self.h_walls = h_walls
        self.v_walls = v_walls
        self.current_turn = turn

    def get_board(self):
        return self.game_board

    def get_h_walls(self):
        return self.h_walls

    def get_v_walls(self):
        return self.v_walls

    def get_current_turn(self):
        return self.current_turn

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
        if orientation == 'h':
            if not self.can_place_horizontal_wall(row, column):
                return False
            self.h_walls[row][column] = True
            self.h_walls[row][column + 1] = True

        elif orientation == 'v':
            if not self.can_place_vertical_wall(row, column):
                return False
            self.v_walls[row][column] = True
            self.v_walls[row + 1][column] = True

        return True

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

    def is_inside_board(self, position):
        row, column = position
        return 0 <= row < self.rows and 0 <= column < self.columns




