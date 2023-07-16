from collections import deque
import copy

MINIMAX_MAX = 1000
MINIMAX_WIN_VALUE = MINIMAX_MAX - 1
MINIMAX_LOSS_VALUE = -MINIMAX_MAX + 1
MINIMAX_DEPTH = 3

class BfsNode:
        def __init__(self, position, source_direction, previous_node):
            self.position = position
            self.source_direction = source_direction
            self.previous_node = previous_node

class MinimaxNode:
        def __init__(self, source_move, source_node, value):
            self.source_move = source_move
            self.source_node = source_node
            self.value = value

class Player1AI:
    player = 'P1'
    enemy = 'P2'

    player_distance_coef = 1.0
    enemy_distance_coef = 2.0

    def get_legal_directions(self, from_position, board):
        board_size = len(board)
        moves = []
        current_position = from_position

        # Check if the player can move up
        if current_position[0] > 0 and board[current_position[0]-1][current_position[1]] != "H" and board[current_position[0]-1][current_position[1]] != "HH" and board[current_position[0]-1][current_position[1]] != "HV":
            moves.append(('U',))
        # Check if the player can move down
        if current_position[0] < board_size-1 and board[current_position[0]][current_position[1]] != "H" and board[current_position[0]][current_position[1]] != "HH" and board[current_position[0]][current_position[1]] != "HV":
            moves.append(('D',))
        # Check if the player can move left
        if current_position[1] > 0 and board[current_position[0]][current_position[1]-1] != "V" and board[current_position[0]][current_position[1]-1] != "VV" and board[current_position[0]][current_position[1]-1] != "HV":
            moves.append(('L',))
        # Check if the player can move right
        if current_position[1] < board_size-1 and board[current_position[0]][current_position[1]] != "V" and board[current_position[0]][current_position[1]] != "VV" and board[current_position[0]][current_position[1]] != "HV":
            moves.append(('R',))
        return moves
    
    def update_board_wall(self, move, board):
        wall_type, center_row, center_col = move

        previous = board[center_row][center_col], board[center_row][center_col + 1], board[center_row + 1][center_col]

        if wall_type == 'H':
            
            if board[center_row][center_col] == False:
                board[center_row][center_col] = 'HH'
            elif board[center_row][center_col] == "V":
                board[center_row][center_col] = 'HV'
            elif board[center_row][center_col] == "VV":
                board[center_row][center_col] = 'HV'
                
            if board[center_row][center_col + 1] == False:
                board[center_row][center_col + 1] = 'H'
            elif board[center_row][center_col + 1] == "V":
                board[center_row][center_col + 1] = 'HV'
            elif board[center_row][center_col + 1] == "VV":
                board[center_row][center_col + 1] = 'HV'
                
        elif wall_type == 'V':
            
            if board[center_row][center_col] == False:
                board[center_row][center_col] = 'VV'
            elif board[center_row][center_col] == "H":
                board[center_row][center_col] = 'HV'
            elif board[center_row][center_col] == "HH":
                board[center_row][center_col] = 'HV'
                
            if board[center_row + 1][center_col] == False:
                board[center_row + 1][center_col] = 'V'
            elif board[center_row + 1][center_col] == "H":
                board[center_row + 1][center_col] = 'HV'
            elif board[center_row + 1][center_col] == "HH":
                board[center_row + 1][center_col] = 'HV'

        return previous
    
    def restore_board_wall(self, move, previous, board):
        wall_type, center_row, center_col = move

        board[center_row][center_col], board[center_row][center_col + 1], board[center_row + 1][center_col] = previous

    def get_legal_walls(self, player_positions, board):
        board_size = len(board)
        moves = []
        for i in range(0, board_size - 1):
            for j in range(0, board_size - 1):
                # Check if a wall can be placed horizontally
                if board[i][j] != "H" and board[i][j] != "HH" and board[i][j] != "VV" and board[i][j] != "HV" and board[i][j + 1] != "H" and board[i][j + 1] != "HH" and board[i][j + 1] != "HV":
                    move = ('H', i, j)
                    previous = self.update_board_wall(move, board)
                    path = self.bfs_get_path(player_positions, self.player,board)
                    enemy_path = self.bfs_get_path(player_positions, self.enemy,board)
                    if path and enemy_path:
                        moves.append(move)
                    self.restore_board_wall(move, previous, board)

                if board[i][j] != "V" and board[i][j] != "VV" and board[i][j] != "HH" and board[i][j] != "HV" and board[i + 1][j] != "V" and board[i + 1][j] != "VV" and board[i + 1][j] != "HV":
                    move = ('V', i, j)
                    previous = self.update_board_wall(move, board)
                    path = self.bfs_get_path(player_positions, self.player,board)
                    enemy_path = self.bfs_get_path(player_positions, self.enemy,board)
                    if path and enemy_path:
                        moves.append(move)
                    self.restore_board_wall(move, previous, board)
        return moves

    # Does Breadth First Search and returns final destination node
    def bfs(self, player_positions, player, board):
        target_x = {'P1': 0, 'P2': len(board) - 1}
        start_node = BfsNode(player_positions[player], None, None)
        explored = []
        
        explored.append(player_positions[player])
        to_be_explored = deque([])
        to_be_explored.append(start_node)
        while to_be_explored:
            current_node = to_be_explored.pop()
            if current_node.position[0] == target_x[player]:
                return current_node
            directions = self.get_legal_directions(current_node.position, board)
            for direction in directions:
                neighbor = (0,0)
                if direction == ('L',):
                    neighbor = (current_node.position[0], current_node.position[1] - 1)
                elif direction == ('R',):
                    neighbor = (current_node.position[0], current_node.position[1] + 1)
                elif direction == ('U',):
                    neighbor = (current_node.position[0] - 1, current_node.position[1])
                elif direction == ('D',):
                    neighbor = (current_node.position[0] + 1, current_node.position[1])
                if neighbor not in explored:
                    explored.append(neighbor)
                    to_be_explored.appendleft(BfsNode(neighbor,direction,current_node))
        return False
    
    def bfs_get_path(self, start_positions, player, board):
        path = deque([])
        current_node = self.bfs(start_positions, player, board)
        if current_node:
            while current_node.source_direction:
                path.appendleft(current_node.source_direction)
                current_node = current_node.previous_node
        return path
    
    def get_all_legal_moves(self, player_positions, player, walls, board):
        moves = self.get_legal_directions(player_positions[player], board)
        if walls[player] > 0:
            moves = moves + self.get_legal_walls(player_positions,board)
        return moves

    
    def game_evaluation(self, player_positions, board):
        player_path = self.bfs_get_path(player_positions, self.player, board)
        enemy_path = self.bfs_get_path(player_positions, self.enemy, board)
        if len(player_path) == 0:
            return MINIMAX_WIN_VALUE
        return self.enemy_distance_coef*len(enemy_path) - self.player_distance_coef*len(player_path)
    
    def simulate_move(self, player_positions, current_player, walls, board, move, source_node):
        current_position = player_positions[current_player]
        if move[0] == 'U':
            player_positions[current_player] = (current_position[0] - 1, current_position[1])
        elif move[0] == 'D':
            player_positions[current_player] = (current_position[0] + 1, current_position[1])
        elif move[0] == 'L':
            player_positions[current_player] = (current_position[0], current_position[1] - 1)
        elif move[0] == 'R':
            player_positions[current_player] = (current_position[0], current_position[1] + 1)
        else:
            walls[current_player] = walls[current_player] - 1
            self.update_board_wall(move,board)

        move_value = self.game_evaluation(player_positions, board)

        return MinimaxNode(move, source_node, move_value)

    
    def minimax(self, player_positions, walls, board, is_player_turn, current_depth, max_depth, current_node):
        if current_depth == max_depth:
            return current_node
    
        if current_node:
            if current_node.value == MINIMAX_WIN_VALUE:
                return current_node
        
        if is_player_turn:
            legal_moves = self.get_all_legal_moves(player_positions, self.player, walls, board)
            max_value = - MINIMAX_MAX
            best_node = None
            for legal_move in legal_moves:
                walls_copy = walls.copy()
                board_copy = copy.deepcopy(board)
                positions_copy = player_positions.copy()
                child_node = self.simulate_move(positions_copy, self.player, walls_copy, board_copy, legal_move, current_node)
                minimaxed_node = self.minimax(positions_copy, walls_copy, board_copy, False, current_depth + 1, max_depth, child_node)
                if minimaxed_node.value == MINIMAX_WIN_VALUE:
                    return minimaxed_node
                if minimaxed_node.value > max_value:
                    max_value = minimaxed_node.value
                    best_node = minimaxed_node
            return best_node

        else:
            legal_moves = self.get_all_legal_moves(player_positions, self.enemy, walls, board)
            min_value = MINIMAX_MAX
            worst_node = None
            for legal_move in legal_moves:
                walls_copy = walls.copy()
                board_copy = copy.deepcopy(board)
                positions_copy = player_positions.copy()
                child_node = self.simulate_move(positions_copy, self.enemy, walls_copy, board_copy, legal_move, current_node)
                minimaxed_node = self.minimax(positions_copy, walls_copy, board_copy, True, current_depth + 1, max_depth, child_node)
                if minimaxed_node.value < min_value:
                    min_value = minimaxed_node.value
                    worst_node = minimaxed_node
            return worst_node



    def get_move(self, game):
        minimax_node = self.minimax(game.player_positions.copy(), game.walls.copy(), copy.deepcopy(game.board), True, 0, MINIMAX_DEPTH, None)
        moves = deque([])
        while minimax_node:
            moves.appendleft(minimax_node.source_move)
            minimax_node = minimax_node.source_node
        return moves[0]
