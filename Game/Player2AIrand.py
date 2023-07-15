import random

class Player2AI:
    def get_move(self, game):
        legal_moves = game.get_legal_moves()
        #print("P2",legal_moves)
        return random.choice(legal_moves)
