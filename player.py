from board import Board


class Player:

    def __init__(self, name = "", position = "", symbol = ""):
        self.name = name
        self.position = position
        self.symbol = symbol
        self.number_of_walls = 10

    def get_number_of_walls(self):
        return self.number_of_walls

    def get_position(self):
        return self.position

    def get_symbol(self):
        return self.symbol

    def get_name(self):
        return self.name

    def set_number_of_walls(self, new_number_of_walls):
        self.number_of_walls = new_number_of_walls

    def set_position(self, position):
        self.position = position





