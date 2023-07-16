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
        while current_node.source_direction:
            path.appendleft(current_node.source_direction)
            current_node = current_node.previous_node
        return path


    def get_move(self, game):
        path = self.bfs_get_path(game.player_positions, self.player,game.board)
        enemy_path = self.bfs_get_path(game.player_positions, self.enemy,game.board)
        print("enemy_path", enemy_path)
        print("player_path", path)

        return path[0]
