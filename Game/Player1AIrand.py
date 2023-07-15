import random

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

    def extract_path(self, start_position, target_x, board):
        board_size = len(board)
        current = start_position
        path = []
        visited = []

        while current[0] != target_x:
            #print("current",current)
            #print("legal_directions",self.get_legal_directions(current))
            found_valid_move = False

            directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
            #print(directions )
            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                #print("neighbor", neighbor)
                if neighbor in visited:
                    path = []
                    continue

                
                if neighbor == start_position or (neighbor[0] >= 0 and neighbor[0] < board_size and neighbor[1] >= 0 and neighbor[1] < board_size):
                    #print("in bounds")
                    if direction == (0, -1):
                        forward_move = ('L',)
                    elif direction == (0, 1):
                        forward_move = ('R',)
                    elif direction == (-1, 0):
                        forward_move = ('U',)
                    elif direction == (1, 0):
                        forward_move = ('D',)

                    #print("self.get_legal_directions(neighbor)", self.get_legal_directions(neighbor))
                    if forward_move in self.get_legal_directions(current, board):
                        path.append(forward_move)
                        #print("appended", forward_move)
                        #print("path", path)
                        #print()
                        visited.append(neighbor)
                        current = neighbor
                        found_valid_move = True
                        break
            #print("found_valid_move", found_valid_move)
            if not found_valid_move:
                # No valid move found, backtrack and continue exploring other paths
                if not path:
                    # No valid path exists, return False
                    return False
                else:
                    # Remove the last move from the path and backtrack
                    last_move = path.pop()
##                    visited.pop()
                    direction = None
                    if last_move == ('L',):
                        direction = (0, -1)
                    elif last_move == ('R',):
                        direction = (0, 1)
                    elif last_move == ('D',):
                        direction = (1, 0)
                    elif last_move == ('U',):
                        direction = (-1, 0)
                    
                    if direction:
                        current = (current[0] - direction[0], current[1] - direction[1])
            #print("current, start_position", current, start_position)

        #print("out of while")    
        return path


    def get_move(self, game):
        p1_position = game.player_positions[game.players[0]]
        path = self.extract_path(p1_position, 0,game.board)
        print(path)
        return path[0]
