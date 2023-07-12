import random

class Player1AI:
    def get_move(self, game):
        legal_moves = game.get_legal_moves()
        print("P1",legal_moves)
        #return(('D',))
        return random.choice(legal_moves)
