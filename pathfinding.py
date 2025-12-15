"""
Pathfinding and validation for Quoridor game.
Makes sure walls don't trap players and validates all moves.
"""

from collections import deque

def has_valid_path(board, player_pos, goal_row):
    """
    Check if player can reach their goal row using BFS pathfinding.
    
    Args:
        board: Board object containing game state
        player_pos: Tuple (row, col) of player's current position
        goal_row: Target row the player needs to reach (0 for player 1, board.rows-1 for player 2)
    
    Returns:
        True if a valid path exists, False otherwise
    """
    # Validate inputs
    if not board.is_inside_board(player_pos):
        return False
    
    if goal_row < 0 or goal_row >= board.rows:
        return False
    
    visited = set()
    queue = deque([player_pos])
    visited.add(player_pos)

    # Four orthogonal directions: up, down, left, right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue:
        current_row, current_col = queue.popleft()

        # Check if we reached the goal row
        if current_row == goal_row:
            return True

        # Explore all adjacent positions
        for d_row, d_col in directions:
            next_pos = (current_row + d_row, current_col + d_col)
            
            # Check if next position is valid, unvisited, and not blocked by a wall
            if (board.is_inside_board(next_pos) and 
                next_pos not in visited and
                not board.is_wall_between((current_row, current_col), next_pos)):
                
                visited.add(next_pos)
                queue.append(next_pos)

    return False


def validate_wall_placement(board, orientation, row, column, player1_pos, player2_pos):
    """
    Check if wall placement is legal and doesn't block any player's path to their goal.
    
    Args:
        board: Board object containing game state
        orientation: 'h' for horizontal or 'v' for vertical wall
        row: Row coordinate for wall placement
        column: Column coordinate for wall placement
        player1_pos: Tuple (row, col) of player 1's position
        player2_pos: Tuple (row, col) of player 2's position
    
    Returns:
        True if wall placement is valid, False otherwise
    """
    # Validate orientation
    if orientation not in ['h', 'v']:
        return False
    
    # Validate coordinates are within board bounds
    if not board.is_inside_board((row, column)):
        return False
    
    # For horizontal walls, check if we can access column + 1
    if orientation == 'h':
        if column + 1 >= board.columns:
            return False
        if row >= len(board.h_walls):
            return False
        if not board.can_place_horizontal_wall(row, column):
            return False
    # For vertical walls, check if we can access row + 1
    elif orientation == 'v':
        if row + 1 >= board.rows:
            return False
        if column >= len(board.v_walls[0]):
            return False
        if not board.can_place_vertical_wall(row, column):
            return False

    # Validate player positions
    if not board.is_inside_board(player1_pos) or not board.is_inside_board(player2_pos):
        return False

    # Try placing the wall temporarily
    if orientation == 'h':
        board.h_walls[row][column] = True
        board.h_walls[row][column + 1] = True
    else:  # orientation == 'v'
        board.v_walls[row][column] = True
        board.v_walls[row + 1][column] = True

    # Check if both players can still reach their goals
    # Player 1 needs to reach row 0 (top), Player 2 needs to reach row board.rows-1 (bottom)
    player1_can_reach = has_valid_path(board, player1_pos, 0)
    player2_can_reach = has_valid_path(board, player2_pos, board.rows - 1)

    # Remove the temporary wall
    if orientation == 'h':
        board.h_walls[row][column] = False
        board.h_walls[row][column + 1] = False
    else:  # orientation == 'v'
        board.v_walls[row][column] = False
        board.v_walls[row + 1][column] = False

    # Wall is valid only if both players can still reach their goals
    return player1_can_reach and player2_can_reach


def place_wall_with_validation(board, orientation, row, column, player1_pos, player2_pos):
    """
    Place a wall after validating it won't block any player's path.
    
    Args:
        board: Board object containing game state
        orientation: 'h' for horizontal or 'v' for vertical wall
        row: Row coordinate for wall placement
        column: Column coordinate for wall placement
        player1_pos: Tuple (row, col) of player 1's position
        player2_pos: Tuple (row, col) of player 2's position
    
    Returns:
        True if wall was successfully placed, False if invalid
    """
    # Validate wall placement first
    if not validate_wall_placement(board, orientation, row, column, player1_pos, player2_pos):
        return False

    # Place the wall permanently
    if orientation == 'h':
        board.h_walls[row][column] = True
        board.h_walls[row][column + 1] = True
    elif orientation == 'v':
        board.v_walls[row][column] = True
        board.v_walls[row + 1][column] = True
    else:
        return False

    return True


def is_valid_move(board, player_pos, target_pos, opponent_pos):
    """
    Check if a pawn move is legal according to Quoridor rules.
    
    Args:
        board: Board object containing game state
        player_pos: Tuple (row, col) of player's current position
        target_pos: Tuple (row, col) of intended move destination
        opponent_pos: Tuple (row, col) of opponent's position
    
    Returns:
        True if move is valid, False otherwise
    """
    # Validate inputs
    if not board.is_inside_board(player_pos):
        return False
    
    if not board.is_inside_board(target_pos):
        return False
    
    if not board.is_inside_board(opponent_pos):
        return False
    
    # Get all valid moves and check if target is among them
    valid_moves = board.get_valid_moves(player_pos, opponent_pos)
    return target_pos in valid_moves


def get_all_valid_moves_for_ui(board, player_pos, opponent_pos):
    """
    Get all legal moves for UI highlighting purposes.
    
    Args:
        board: Board object containing game state
        player_pos: Tuple (row, col) of player's current position
        opponent_pos: Tuple (row, col) of opponent's position
    
    Returns:
        List of valid move positions as tuples [(row, col), ...]
        Returns empty list if inputs are invalid
    """
    # Validate inputs
    if not board.is_inside_board(player_pos):
        return []
    
    if not board.is_inside_board(opponent_pos):
        return []
    
    # Get and return all valid moves from the board
    return board.get_valid_moves(player_pos, opponent_pos)