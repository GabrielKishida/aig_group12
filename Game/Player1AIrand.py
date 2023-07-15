from collections import deque

class BfsNode:
        def __init__(self, position, source_direction, previous_node):
            self.position = position
            self.source_direction = source_direction
            self.previous_node = previous_node

class Player1AI:

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
    def bfs(self, start_position, target_x, board):
        start_node = BfsNode(start_position, None, None)
        explored = []
        
        explored.append(start_position)
        to_be_explored = deque([])
        to_be_explored.append(start_node)
        while to_be_explored:
            current_node = to_be_explored.pop()
            if current_node.position[0] == target_x:
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
    
    def bfs_get_path(self, start_position, target_x, board):
        path = deque([])
        current_node = self.bfs(start_position, target_x, board)
        while current_node.source_direction:
            path.appendleft(current_node.source_direction)
            current_node = current_node.previous_node
        return path


    def get_move(self, game):
        p1_position = game.player_positions[game.players[0]]
        path = self.bfs_get_path(p1_position, 0,game.board)
        print(path)
        return path[0]
