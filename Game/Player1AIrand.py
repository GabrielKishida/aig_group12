from collections import deque

class BfsNode:
        def __init__(self, position, source_direction, previous_node):
            self.position = position
            self.source_direction = source_direction
            self.previous_node = previous_node

class Player1AI:
    player = 'P1'
    enemy = 'P2'

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
    
    def bfs_get_path(self, start_position, player, board):
        path = deque([])
        current_node = self.bfs(start_position, player, board)
        if current_node:
            while current_node.source_direction:
                path.appendleft(current_node.source_direction)
                current_node = current_node.previous_node
        return path


    def get_move(self, game):
        path = self.bfs_get_path(game.player_positions, self.player,game.board)
        legal_moves = self.get_legal_walls(game.player_positions, game.board)
        legal_moves = legal_moves + self.get_legal_directions(game.player_positions[self.player],game.board)
        game_legal_moves = game.get_legal_moves()

        for move in game_legal_moves:
            if move not in legal_moves:
                print("Legal move missing")
                print(move)
        for move in legal_moves:
            if move not in game_legal_moves:
                print("Illegal move considered legal")
                print(move)
        

        return path[0]
