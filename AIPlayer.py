import math
from collections import deque
import heapq
import random
import copy

PAWN_MOVE_CODE = 0
WALL_MOVE_CODE = 1

class AIPlayer:
    """
    AI Player for Quoridor with three difficulty levels:
    - Easy: Random moves with basic validation
    - Medium: Greedy algorithm with simple heuristics (depth=1)
    - Hard: Full minimax with alpha-beta pruning (depth=3)
    """
    
    def __init__(self, board=None, player_id=1, objective=0, difficulty='medium'):
        """
        Initialize AIPlayer with all necessary attributes.
        
        Args:
            board: Board object containing game state
            player_id: ID of this player (1 or 2)
            objective: Row/column the player needs to reach
            difficulty: 'easy', 'medium', or 'hard'
        """
        self.board = board
        self.id = player_id
        self.objective = objective
        self.pos = None  # Will be set by board initialization
        self.available_walls = 10  # Standard Quoridor rule
        
        # Set parameters based on difficulty
        if difficulty.lower() == 'easy':
            self.search_depth = 0  # No search, random moves
            self.wall_bonus_weight = 0
            self.difficulty = 'easy'
        elif difficulty.lower() == 'medium':
            self.search_depth = 1  # Greedy one-step lookahead
            self.wall_bonus_weight = 0.5
            self.difficulty = 'medium'
        else:  # hard
            self.search_depth = 3  # Deep search
            self.wall_bonus_weight = 1.5
            self.difficulty = 'hard'

    def apply_move(self, board, move):
        """Apply a move to the board using Board class methods"""
        if move[0] == PAWN_MOVE_CODE:
            # Move pawn to new position using board's update method
            new_position = tuple(move[1])
            # Get the correct player from the board copy to ensure independence
            if board.get_current_turn() == 1:
                board.get_player1().set_position(new_position)
            else:
                board.get_player2().set_position(new_position)
        elif move[0] == WALL_MOVE_CODE:
            # Place wall using board's place_wall method
            orientation = move[2]  # 'h' or 'v'
            row, col = move[1]
            # print("inside place wall")
            board.place_wall(orientation, row, col)
        
        # Switch turn to other player
        next_turn = 2 if board.get_current_turn() == 1 else 1
        board.set_current_turn(next_turn)

    def get_valid_moves(self, board):
        """Generate all valid moves for the current player using Board's methods"""
        current_player = board.get_current_player()
        opponent = board.get_player2() if board.get_current_player() == board.get_player1() else board.get_player1()
        
        moves = []
        
        # Get pawn moves from board's get_valid_moves method
        pawn_moves = board.get_valid_moves(current_player.get_position(), opponent.get_position())
        for move_pos in pawn_moves:
            moves.append((PAWN_MOVE_CODE, move_pos))
        
        # Get wall moves if player has walls remaining
        if current_player.get_number_of_walls() > 0:
            rows, cols = board.rows, board.columns
            # Check horizontal wall placements
            for row in range(rows - 1):
                for col in range(cols - 1):
                    if board.can_place_horizontal_wall(row, col):
                        moves.append((WALL_MOVE_CODE, (row, col), 'h'))
            
            # Check vertical wall placements
            for row in range(rows - 1):
                for col in range(cols - 1):
                    if board.can_place_vertical_wall(row, col):
                        moves.append((WALL_MOVE_CODE, (row, col), 'v'))
        # print(f"Valid moves for player {current_player.get_name()}: {moves}")
        return moves

    def heuristic(self, board):
        """Heuristic function using A* for both players"""
        def manhattan_distance(y1, x1, y2):
            return abs(y1 - y2)  # Only vertical movement matters for goal row

        def a_star_path(start_pos, target_row, opponent_pos):
            visited = set()
            y, x = start_pos
            heap = [(manhattan_distance(y, x, target_row), 0, y, x)]  # (f, g, y, x)

            while heap:
                f, g, cy, cx = heapq.heappop(heap)
                if cy == target_row:
                    return g
                if (cy, cx) in visited:
                    continue
                visited.add((cy, cx))

                # Check all four directions (single step)
                for ny, nx in [(cy-1, cx), (cy+1, cx), (cy, cx-1), (cy, cx+1)]:
                    if (ny, nx) not in visited and board.is_inside_board((ny, nx)):
                        if not board.is_wall_between((cy, cx), (ny, nx)) and (ny, nx) != opponent_pos:
                            h = manhattan_distance(ny, nx, target_row)
                            heapq.heappush(heap, (g + 1 + h, g + 1, ny, nx))

            return math.inf  # No path found

        player1 = board.get_player1()
        player2 = board.get_player2()
        
        p1_path = a_star_path(player1.get_position(), 0, player2.get_position())
        p2_path = a_star_path(player2.get_position(), 8, player1.get_position())

        # Check for terminal states
        if p1_path == 0:
            return -math.inf
        if p2_path == 0:
            return math.inf

        # Heuristic = path difference + wall advantage
        path_diff = (p1_path - p2_path) * 4
        current_player_walls = board.get_current_player().get_number_of_walls()
        wall_bonus = current_player_walls * self.wall_bonus_weight
        
        return path_diff + wall_bonus

    def alpha_beta(self, board, depth, alpha, beta):
        """Minimax with alpha-beta pruning"""
        player1 = board.get_player1()
        player2 = board.get_player2()
        print("alpha beta depth: ", depth)
        # Check terminal states
        if player1.get_position()[0] == 0:  # Player 1 reached goal
            return -float('inf')
        if player2.get_position()[0] == 8:  # Player 2 reached goal
            return float('inf')

        # Base case: reached depth limit
        if depth == 0:
            return self.heuristic(board)

        valid_moves = self.get_valid_moves(board)

        # Move ordering: prioritize winning moves
        def move_priority(move):
            if move[0] == PAWN_MOVE_CODE:
                target_pos = move[1]
                current = board.get_current_player()
                goal_row = 8 if board.get_current_player() == player2 else 0
                if target_pos[0] == goal_row:
                    return 0  # Winning move
            return 1

        valid_moves.sort(key=move_priority)
        print(f"Valid moves: {valid_moves}")
        if board.get_current_turn() == 2:  # Maximizing player
            max_eval = -float('inf')
            for move in valid_moves:
                # Create a copy of the board state
                board_copy = copy.deepcopy(board)
                self.apply_move(board_copy, move)
                eval_score = self.alpha_beta(board_copy, depth - 1, alpha, beta)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_eval
        else:  # Minimizing player
            min_eval = float('inf')
            for move in valid_moves:
                # Create a copy of the board state
                board_copy = copy.deepcopy(board)
                self.apply_move(board_copy, move)
                eval_score = self.alpha_beta(board_copy, depth - 1, alpha, beta)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_eval

    def ai_move(self):
        """Execute AI move based on difficulty level"""
        board_copy = copy.deepcopy(self.board)
        valid_moves = self.get_valid_moves(board_copy)

        if not valid_moves:
            return  # No valid moves available
        print(f"ai player {self.board.get_current_turn()}")
        # Check for immediate win
        current_player = self.board.get_current_player()
        opponent = self.board.get_player2() if current_player == self.board.get_player1() else self.board.get_player1()
        goal_row = 8 if current_player == self.board.get_player2() else 0
        opponent_goal_row = 0 if current_player == self.board.get_player2() else 8
        
        fast_win_move = next((m for m in valid_moves 
                              if m[0] == PAWN_MOVE_CODE and m[1][0] == goal_row), 
                             None)

        if fast_win_move:
            self.apply_move(self.board, fast_win_move)
            return

        # Easy difficulty: Random valid move
        if self.difficulty == 'easy':
            # Prefer pawn moves over wall moves (65% chance)
            pawn_moves = [m for m in valid_moves if m[0] == PAWN_MOVE_CODE]
            wall_moves = [m for m in valid_moves if m[0] == WALL_MOVE_CODE]
            
            if pawn_moves and (not wall_moves or random.random() < 0.65):
                best_move = random.choice(pawn_moves)
            elif wall_moves:
                best_move = random.choice(wall_moves)
            else:
                best_move = random.choice(valid_moves)
        
            self.apply_move(self.board, best_move)
        # Medium difficulty: Greedy
        elif self.difficulty == "medium":
            best_move = None
            best_score = -float('inf')

            for move in valid_moves:
                board_sim = copy.deepcopy(self.board)
                self.apply_move(board_sim, move)

                # Compute shortest paths using A* or BFS
                def shortest_path(pos, target_row):
                    visited = set()
                    queue = deque([(pos, 0)])
                    while queue:
                        (y, x), dist = queue.popleft()
                        if (y, x) in visited:
                            continue
                        visited.add((y, x))
                        if y == target_row:
                            return dist
                        for ny, nx in [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]:
                            if board_sim.is_inside_board((ny, nx)) and not board_sim.is_wall_between((y, x), (ny, nx)):
                                queue.append(((ny, nx), dist+1))
                    return float('inf')

                my_path = shortest_path(board_sim.get_current_player().get_position(), goal_row)
                sim_opponent = board_sim.get_player2() if board_sim.get_current_turn() == 1 else board_sim.get_player1()
                opp_path = shortest_path(sim_opponent.get_position(), opponent_goal_row)

                # Score: maximize opponent path minus my path
                score = opp_path - my_path
                if score > best_score:
                    best_score = score
                    best_move = move

            if best_move:
                self.apply_move(self.board, best_move)
            print(best_move  , best_score)
            
        # Hard difficulty: Use minimax
        else:
            best_move = None
            best_value = -float('inf')
            
            for move in valid_moves:
                board_copy = copy.deepcopy(self.board)
                self.apply_move(board_copy, move)
                value = self.alpha_beta(board_copy, self.search_depth, 
                                       -float('inf'), float('inf'))

                if value > best_value:
                    best_value = value
                    best_move = move

            if best_move:
                self.apply_move(self.board, best_move)

            print(best_move)


# Factory function for creating AI players
def create_ai_player(board=None, player_id=1, objective=0, difficulty='medium'):
    return AIPlayer(board=board, player_id=player_id, objective=objective, difficulty=difficulty)