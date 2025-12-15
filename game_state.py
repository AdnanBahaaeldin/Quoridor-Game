from copy import deepcopy
import json

from board import Board
from player import Player


class GameState:
   def __init__(self):
       self.is_game_over = False
       self.board = None
       self.undo_stack = []
       self.redo_stack = []

   def save_state(self, board):
       snapshot = {
           "player1": {
               "name": board.player1.name,
               "position": board.player1.position,
               "symbol": board.player1.symbol,
               "number_of_walls": board.player1.get_number_of_walls(),
           },
           "player2": {
               "name": board.player2.name,
               "position": board.player2.position,
               "symbol": board.player2.symbol,
               "number_of_walls": board.player2.get_number_of_walls(),
           },
           "h_walls": deepcopy(board.h_walls),
           "v_walls": deepcopy(board.v_walls),
           "turn": board.get_current_turn(),
       }

       self.undo_stack.append(snapshot)
       self.redo_stack.clear()
       if board.player1.position[0] == 0 or board.player2.position[0] == board.rows - 1:
           self.is_game_over = True

       return self.is_game_over


   def undo_move(self):
      if len(self.undo_stack) <= 1:
          return
      self.redo_stack.append(self.undo_stack.pop())
      board = self.extract_board_from_snapshot(self.undo_stack[-1])
      self.board = board
      # self.board.undo_redo_move(board)
      return self.board


   def redo_move(self):
       if not self.redo_stack:
           return
       self.undo_stack.append(self.redo_stack.pop())
       board = self.extract_board_from_snapshot(self.redo_stack[-1])
       self.board = board
       # self.board.undo_redo_move(board)
       return self.board


   def save_game(self, board):
       snapshot = {
        "player1": {
            "name": board.player1.name,
            "position": board.player1.position,
            "symbol": board.player1.symbol,
            "number_of_walls": board.player1.get_number_of_walls(),
            },
       "player2": {
            "name": board.player2.name,
            "position": board.player2.position,
            "symbol": board.player2.symbol,
            "number_of_walls": board.player2.get_number_of_walls(),
            },
           "h_walls": deepcopy(board.h_walls),
           "v_walls": deepcopy(board.v_walls),
           "turn": board.get_current_turn(),
       }

       with open("save_game.json", "w") as f:
           json.dump(snapshot, f)


   def load_game(self):
       try:
           with open("save_game.json", "r") as f:
               snapshot = json.load(f)

           board = self.extract_board_from_snapshot(snapshot)

           self.board = board

           # self.board.load_game(board)

           return self.board

       except FileNotFoundError:
            print ("Load file not found.")
            return None

   def new_game(self, rows, columns, player1_name, player2_name):
       player1 = Player(player1_name, (rows-1, columns // 2), 1)
       player2 = Player(player2_name, (0, columns // 2), 2)
       self.board = Board(self, player1, player2, rows, columns)
       self.save_state(self.board)
       return self.board


   def extract_board_from_snapshot(self, snapshot):
       board = Board()
       player1 = Player(
           name=snapshot["player1"]["name"],
           position=tuple(snapshot["player1"]["position"]),  # convert list back to tuple
           symbol=snapshot["player1"]["symbol"],
       )
       player1.set_number_of_walls(snapshot["player1"]["number_of_walls"])

       player2 = Player(
           name=snapshot["player2"]["name"],
           position=tuple(snapshot["player2"]["position"]),  # convert list back to tuple
           symbol=snapshot["player2"]["symbol"],
       )
       player2.set_number_of_walls(snapshot["player2"]["number_of_walls"])

       board.set_player1(player1)
       board.set_player2(player2)
       board.set_h_walls(snapshot["h_walls"])
       board.set_v_walls(snapshot["v_walls"])
       board.set_current_turn(snapshot["turn"])
       board.set_game_state(self)

       return board