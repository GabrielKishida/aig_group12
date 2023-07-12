import pygame
from pygame.locals import *
import random
import time
import heapq
import copy

board_size = 4
num_walls = 3

# Initialize Pygame and set up the game window
pygame.init()
WIDTH = HEIGHT = 600
FRAME_SIZE = 40
WINDOW_WIDTH = WIDTH + FRAME_SIZE*2 + 400
WINDOW_HEIGHT = HEIGHT + FRAME_SIZE*2
BOARD_COLOR = (150, 75, 0)  # Brown color for the board
FRAME_COLOR = (255, 255, 255)  # White color for the frame
LOG_COLOR = (255, 0, 0)  # Red color for Player 1's moves
LOG2_COLOR = (0, 0, 255)  # Blue color for Player 2's moves
BOTH_COLOR = (128, 0, 128)  # Purple
WALLS_COLOR = (0, 0, 0)  # White color for the frame

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Quoridor Game")

from Player1AIrand import *
from Player2AIrand import *




class Quoridor:
    def __init__(self, board_size):
        self.board_size = board_size
        self.board = [[False for _ in range(board_size)] for _ in range(board_size)]
        self.players = ['P1', 'P2']
        self.player_positions = {'P1': (board_size - 1, board_size // 2), 'P2': (0, board_size // 2  if board_size % 2 == 1 else board_size // 2 -1)}
        self.walls = {'P1': num_walls, 'P2': num_walls}
        self.ply = random.randint(0,1)
        self.player1_ai = Player1AI()  # Create an instance of Player1's AI
        self.player2_ai = Player2AI()  # Create an instance of Player2's AI
        self.move_log = []  # Move log to store the moves
        self.previous_board = None
        self.previous_player_positions = {'P1': None, 'P2': None}  # Initialize the previous_player_positions attribute
        self.game_over = False  # Add a game_over attribute to track the end of the game



    def get_legal_moves(self):
        moves = []
        current_position = self.player_positions[self.players[self.ply]]
        if self.walls[self.players[self.ply]] > 0:
            for i in range(0, self.board_size - 1):
                for j in range(0, self.board_size - 1):

                    # Check if a wall can be placed horizontally
                        if self.board[i][j] != "H" and self.board[i][j] != "HH" and self.board[i][j] != "VV" and self.board[i][j] != "HV" and self.board[i][j + 1] != "H" and self.board[i][j + 1] != "HH" and self.board[i][j + 1] != "HV":
                            move = ('H', i, j)
                            #simulate placing a wall to compute path existance
                            previous = self.update_board_wall(move)
                            #print("\ntemporaryH")
                            #self.print_board()
                            reachable1 = self.reachable(self.player_positions['P1'],(0,0))
                            reachable2 = self.reachable(self.player_positions['P2'],(board_size-1,0))
                            if reachable1 and reachable2:
                                moves.append(move)
                                #print("reachable", move)
                            #else:
                                #print("not reachable", move)
                            self.restore_board_wall(move, previous)

                    # Check if a wall can be placed vertically
                        if self.board[i][j] != "V" and self.board[i][j] != "VV" and self.board[i][j] != "HH" and self.board[i][j] != "HV" and self.board[i + 1][j] != "V" and self.board[i + 1][j] != "VV" and self.board[i + 1][j] != "HV":
                            move = ('V', i, j)
                            #simulate placing a wall to compute path existance
                            previous = self.update_board_wall(move)
                            #print("\ntemporaryV")
                            #self.print_board()
                            reachable1 = self.reachable(self.player_positions['P1'],(0,0))
                            reachable2 = self.reachable(self.player_positions['P2'],(board_size-1,0))
                            if reachable1 and reachable2:
                                moves.append(move)
                                #print("reachable", move)
                            #else:
                                #print("not reachable", move)
                            self.restore_board_wall(move, previous)

        # Check if the player can move up
        if current_position[0] > 0 and self.board[current_position[0]-1][current_position[1]] != "H" and self.board[current_position[0]-1][current_position[1]] != "HH" and self.board[current_position[0]-1][current_position[1]] != "HV":
            moves.append(('U',))
        # Check if the player can move down
        if current_position[0] < self.board_size-1 and self.board[current_position[0]][current_position[1]] != "H" and self.board[current_position[0]][current_position[1]] != "HH" and self.board[current_position[0]][current_position[1]] != "HV":
            moves.append(('D',))
        # Check if the player can move left
        if current_position[1] > 0 and self.board[current_position[0]][current_position[1]-1] != "V" and self.board[current_position[0]][current_position[1]-1] != "VV" and self.board[current_position[0]][current_position[1]-1] != "HV":
            moves.append(('L',))
        # Check if the player can move right
        if current_position[1] < self.board_size-1 and self.board[current_position[0]][current_position[1]] != "V" and self.board[current_position[0]][current_position[1]] != "VV" and self.board[current_position[0]][current_position[1]] != "HV":
            moves.append(('R',))
        return moves

    def get_legal_directions(self, from_position):
        moves = []
        current_position = from_position

        # Check if the player can move up
        if current_position[0] > 0 and self.board[current_position[0]-1][current_position[1]] != "H" and self.board[current_position[0]-1][current_position[1]] != "HH" and self.board[current_position[0]-1][current_position[1]] != "HV":
            moves.append(('U',))
        # Check if the player can move down
        if current_position[0] < self.board_size-1 and self.board[current_position[0]][current_position[1]] != "H" and self.board[current_position[0]][current_position[1]] != "HH" and self.board[current_position[0]][current_position[1]] != "HV":
            moves.append(('D',))
        # Check if the player can move left
        if current_position[1] > 0 and self.board[current_position[0]][current_position[1]-1] != "V" and self.board[current_position[0]][current_position[1]-1] != "VV" and self.board[current_position[0]][current_position[1]-1] != "HV":
            moves.append(('L',))
        # Check if the player can move right
        if current_position[1] < self.board_size-1 and self.board[current_position[0]][current_position[1]] != "V" and self.board[current_position[0]][current_position[1]] != "VV" and self.board[current_position[0]][current_position[1]] != "HV":
            moves.append(('R',))
        return moves

    def reachable(self, start_position, target_position):
        path = []
        for i in range(100):
            path = self.extract_path(start_position, target_position)
            if path != [] and path != False:
                #print("path is ok", path)
                return True
        return False

    def extract_path(self, start_position, target_position):
        current = start_position
        path = []
        visited = []

        while current[0] != target_position[0]:
            #print("current",current)
            #print("legal_directions",self.get_legal_directions(current))
            found_valid_move = False

            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            random.shuffle(directions)
            #print(directions )
            for direction in directions:
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                #print("neighbor", neighbor)
                if neighbor in visited:
                    #print("neighbor already visited", neighbor)
                    continue

                
                if neighbor == start_position or (neighbor[0] >= 0 and neighbor[0] < self.board_size and neighbor[1] >= 0 and neighbor[1] < self.board_size):
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
                    if forward_move in self.get_legal_directions(current):
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

    def move_player(self, move):
        current_player = self.players[self.ply]
        current_position = self.player_positions[current_player]
        self.previous_player_positions[current_player] = current_position  # Store the previous player position
        if move[0] == 'U':
            self.player_positions[current_player] = (current_position[0] - 1, current_position[1])
        elif move[0] == 'D':
            self.player_positions[current_player] = (current_position[0] + 1, current_position[1])
        elif move[0] == 'L':
            self.player_positions[current_player] = (current_position[0], current_position[1] - 1)
        elif move[0] == 'R':
            self.player_positions[current_player] = (current_position[0], current_position[1] + 1)
        self.move_log.append((current_player, move))

        # Check if the current player has reached the other end of the board
        if (current_player == 'P1' and self.player_positions[current_player][0] == 0) or \
                (current_player == 'P2' and self.player_positions[current_player][0] == self.board_size - 1):
            self.game_over = True
            print(self.player_positions, self.player_positions[current_player][0] == 0, self.player_positions[current_player][0] == self.board_size - 1)
            print(f"Player {current_player} wins!")
            
        self.ply = (self.ply + 1) % 2
        self.previous_board = [row[:] for row in self.board]  # Save the current board state

    def update_board_wall(self, move):
        wall_type, center_row, center_col = move

        previous = self.board[center_row][center_col], self.board[center_row][center_col + 1], self.board[center_row + 1][center_col]

        if wall_type == 'H':
            
            if self.board[center_row][center_col] == False:
                self.board[center_row][center_col] = 'HH'
            elif self.board[center_row][center_col] == "V":
                self.board[center_row][center_col] = 'HV'
            elif self.board[center_row][center_col] == "VV":
                self.board[center_row][center_col] = 'HV'
                
            if self.board[center_row][center_col + 1] == False:
                self.board[center_row][center_col + 1] = 'H'
            elif self.board[center_row][center_col + 1] == "V":
                self.board[center_row][center_col + 1] = 'HV'
            elif self.board[center_row][center_col + 1] == "VV":
                self.board[center_row][center_col + 1] = 'HV'
                
        elif wall_type == 'V':
            
            if self.board[center_row][center_col] == False:
                self.board[center_row][center_col] = 'VV'
            elif self.board[center_row][center_col] == "H":
                self.board[center_row][center_col] = 'HV'
            elif self.board[center_row][center_col] == "HH":
                self.board[center_row][center_col] = 'HV'
                
            if self.board[center_row + 1][center_col] == False:
                self.board[center_row + 1][center_col] = 'V'
            elif self.board[center_row + 1][center_col] == "H":
                self.board[center_row + 1][center_col] = 'HV'
            elif self.board[center_row + 1][center_col] == "HH":
                self.board[center_row + 1][center_col] = 'HV'

        return previous


    def restore_board_wall(self, move, previous):
        wall_type, center_row, center_col = move

        self.board[center_row][center_col], self.board[center_row][center_col + 1], self.board[center_row + 1][center_col] = previous

                

    def place_wall(self, move):

        self.update_board_wall(move)
                
        current_player = self.players[self.ply]
        self.previous_player_positions[current_player] = self.player_positions[current_player]  # Store the previous player position
        self.walls[current_player] -= 1
        self.move_log.append((current_player, move))
        self.ply = (self.ply + 1) % 2
        self.previous_board = [row[:] for row in self.board]  # Save the current board state

    def undo_move(self):
        # Restore the player positions to the previous state
        previous_positions = self.previous_player_positions
        self.player_positions['P1'] = previous_positions['P1']
        self.player_positions['P2'] = previous_positions['P2']
        self.previous_player_positions = {'P1': None, 'P2': None}  # Reset the previous player positions

        
        # Restore the board to the previous state
        self.board = [row[:] for row in self.previous_board]
        self.previous_board = None

        # Switch the turn back to the previous player
        self.ply = (self.ply - 1) % 2

        # Redraw the board to reflect the restored state
        self.draw_board()

        
    def draw_board(self):
        window.fill(FRAME_COLOR)
        pygame.draw.rect(window, BOARD_COLOR, (FRAME_SIZE, FRAME_SIZE, WIDTH, HEIGHT))

        square_size = WIDTH // self.board_size
        wall_thickness = 5

        # Draw the grid lines
        for i in range(1, self.board_size):
            pygame.draw.line(window, FRAME_COLOR, (i * square_size + FRAME_SIZE, FRAME_SIZE),
                             (i * square_size + FRAME_SIZE, HEIGHT + FRAME_SIZE), 2)
            pygame.draw.line(window, FRAME_COLOR, (FRAME_SIZE, i * square_size + FRAME_SIZE),
                             (WIDTH + FRAME_SIZE, i * square_size + FRAME_SIZE), 2)

        # Draw the player positions
        for player, position in self.player_positions.items():
            if position is not None:  # Check if position is not None
                player_color = LOG_COLOR if player == 'P1' else LOG2_COLOR
                if self.player_positions['P1'] == self.player_positions['P2']:
                    player_color = BOTH_COLOR
                pygame.draw.circle(window, player_color,
                               (position[1] * square_size + square_size // 2 + FRAME_SIZE,
                                position[0] * square_size + square_size // 2 + FRAME_SIZE), square_size // 4)

        # Draw the walls
        for i in range(self.board_size):
            for j in range(self.board_size):
                if self.board[i][j] == 'H' or self.board[i][j] == 'HH':
                    pygame.draw.line(window, WALLS_COLOR, ((j) * square_size + FRAME_SIZE, (i+1) * square_size + FRAME_SIZE),
                                     (((j) + 1) * square_size + FRAME_SIZE, (i+1) * square_size + FRAME_SIZE), wall_thickness)
                elif self.board[i][j] == 'V' or self.board[i][j] == 'VV':
                    pygame.draw.line(window, WALLS_COLOR, ((j+1) * square_size + FRAME_SIZE, (i) * square_size + FRAME_SIZE),
                                     ((j+1) * square_size + FRAME_SIZE, (i + 1) * square_size + FRAME_SIZE), wall_thickness)
                elif self.board[i][j] == 'HV':
                    pygame.draw.line(window, WALLS_COLOR, (j * square_size + FRAME_SIZE, (i+1) * square_size + FRAME_SIZE),
                                     ((j + 1) * square_size + FRAME_SIZE, (i+1) * square_size + FRAME_SIZE), wall_thickness)
                    pygame.draw.line(window, WALLS_COLOR, ((j+1) * square_size + FRAME_SIZE, i * square_size + FRAME_SIZE),
                                     ((j+1) * square_size + FRAME_SIZE, (i + 1) * square_size + FRAME_SIZE), wall_thickness)
        # Display the coordinates
        font = pygame.font.Font(None, 24)
        for i in range(self.board_size):
            # Display the numbers 1-9 for columns
            text = font.render(str(i + 1), True, WALLS_COLOR)
            window.blit(text, (50 + (i + 0.5) * square_size - text.get_width() // 2, 20))

            # Display the letters A-I for rows
            text = font.render(chr(ord('A') + i), True, WALLS_COLOR)
            window.blit(text, (20, 50 + (i + 0.5) * square_size - text.get_height() // 2))

    def print_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                print( self.board[i][j] , end="\t")
            print()


    def draw_log(self):
        log_font = pygame.font.Font(None, 32)
        player1_moves = [entry for entry in self.move_log if entry[0] == 'P1']
        player2_moves = [entry for entry in self.move_log if entry[0] == 'P2']

        for i, move in enumerate(player1_moves):
            text = log_font.render(str(move[0])+" "+str(move[1]), True, LOG_COLOR)
            window.blit(text, (WIDTH + 100, 50 + i * 40))

        for i, move in enumerate(player2_moves):
            text = log_font.render(str(move[0])+" "+str(move[1]), True, LOG2_COLOR)
            window.blit(text, (WIDTH + 300, 50 + i * 40))

game = Quoridor(board_size)

running = True
clock = pygame.time.Clock()

current_move = None  # Track the current move
stop_game = False

while running:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if current_move is None:
                    if game.ply == 0:
                        current_move = game.player1_ai.get_move(game)
                    else:
                        current_move = game.player2_ai.get_move(game)
                    illegal = False
                    #print(current_move, "NOT IN", game.get_legal_moves(), current_move not in game.get_legal_moves())
                    if current_move not in game.get_legal_moves():
                        illegal = True
                        print("ILLEGAL MOVE DETECTED", game.ply)
##            elif event.key == pygame.K_LEFT:
##                game.undo_move()
##                current_move = None  # Reset current_move to None

    if current_move is not None:
        if current_move[0] in ['U', 'D', 'L', 'R']:
            game.move_player(current_move)
        else:
            game.place_wall(current_move)
        print(current_move)
        game.print_board()

        
        # Check if the game is over
        if stop_game == True:
            running = False

        
        if game.game_over:
            stop_game = True

        if illegal == True:
            print("ENDING", game.ply)
            if game.ply == 1:   #ply has changed in the meantime, so these are inverted
                game.move_log.append(("P1", "ILLEGAL"))
            else:
                game.move_log.append(("P2", "ILLEGAL"))            
            stop_game = True
            

        current_move = None
   
            

    game.draw_board()
    game.draw_log()
    pygame.display.update()

pygame.quit()
