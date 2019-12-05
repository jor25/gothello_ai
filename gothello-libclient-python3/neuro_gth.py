# Jordan Le
# Training a neural network to play gothello.
# Aim is to learn from previous winners of the game.
# Need to build data pipeline for training as well.

import numpy as np
from operator import add
from keras.optimizers import Adam
from keras.models import Sequential
from keras.layers.core import Dense, Dropout
import random
import sys
import gthclient
import model_arch as ma

'''
class Collection():
    def __init__(self):
        self.learning_rate = 0.001
        self.model = self.network()
        #self.model = self.network("model_files/nn_01.hdf5")


    def network(self, weights=None):
        model = Sequential()
        model.add(Dense(output_dim=75, activation='relu', input_dim=25))        # max 144
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=75, activation='relu'))
        model.add(Dropout(0.15))
        model.add(Dense(output_dim=75, activation='relu'))
        model.add(Dropout(0.15))

        model.add(Dense(output_dim=25, activation='softmax'))
        opt = Adam(self.learning_rate)
        model.compile(loss='mse', metrics=['accuracy'], optimizer=opt)

        if weights:
            model.load_weights(weights)
            print("model loaded")
        return model
'''


def letter_range(letter):
    for i in range(5):
        yield chr(ord(letter) + i)


def show_position():
    state = []  # Making a new state
    for digit in letter_range('1'):
        for letter in letter_range('a'):
            pos = letter + digit
            if pos in grid["white"]:
                piece = '1'#"O"
                state.append(1)     # The enemy is the loser
            elif pos in grid["black"]:
                piece = '2'#"*"
                state.append(2)     # You gonna be the winner
            else:
                piece = '0'#"."
                state.append(0)     # These are blanks
            print(piece, end="")
        #print("HELLO")
        print()
    
    print(state)
    return np.asarray(state)        # Give back flattened array of data

def give_state(move):
    # 0 = '.'   - Blank
    # 2 = '*'   - Winner
    # 1 = '0'   - Loser
    # Move = a4
    board_2d = np.zeros((5,5), dtype=int) 

    if move[0] == 'a':
        x = 0
    elif move[0] == 'b':
        x = 1
    elif move[0] == 'c':
        x = 2
    elif move[0] == 'd':
        x = 3
    elif move[0] == 'e':
        x = 4
    
    y = int(move[1]) - 1

    print("{y},{x}")


def make_predict(restate):

    moves = ['a5','b5','c5','d5','e5',
            'a4','b4','c4','d4','e4',
            'a3','b3','c3','d3','e3',
            'a2','b2','c2','d2','e2',
            'a1','b1','c1','d1','e1']

    prediction = nn.model.predict(restate)
    my_move = moves[np.argmax(prediction[0])]   # a5
    #print("prediction:\n{}\nmove: {}".format(prediction, my_move))

    # Get a new prediction:
    #index = np.argmax(prediction[0])
    #prediction[0][index] = -1

    if my_move in list(board):
        #print("Valid")
        return my_move  # this move is valid so do it
    else:
        
        while my_move not in list(board):   # While my move is not valid
            #print("{} is not valid".format(my_move))
            # Get a new prediction:
            index = np.argmax(prediction[0])    
            prediction[0][index] = -1               # Previous prediction not good, try next best valid.
            my_move = moves[np.argmax(prediction[0])]   # Get a move that is valid?
        

        return my_move  # Next option
        #return random.choice(list(board))   # Legit, do something better than this later


def calc_score(npstate):
    my_tiles = np.where(npstate == 2)[0]    # Where I(BLACK) placed my tiles
    opp_tiles = np.where(npstate == 1)[0]   # Where white placed their tiles
    print("my_tiles: {}\nopp_tiles: {}".format(my_tiles, opp_tiles))
    #print(my_tiles[0])

    my_score = len(my_tiles)
    opp_score = len(opp_tiles)
    print("my_score: {}\nopp_score: {}".format(my_score, opp_score))

    if my_score > opp_score:
        print("BLACK WINS")
    elif my_score < opp_score:
        print("WHITE WINS")
    else:
        print("DRAW")


nn = ma.Collection()
me = sys.argv[1]
opp = gthclient.opponent(me)

#client = gthclient.GthClient(me, "localhost", 0)
client = gthclient.GthClient(me, "barton.cs.pdx.edu", 0)
side = "black"

board = {letter + digit
         for letter in letter_range('a')
         for digit in letter_range('1')}

grid = {"white": set(), "black": set()}

if __name__ == "__main__":
    print(board)
    while True:
        npstate = show_position()
        restate = np.reshape(npstate, (-1,25))
        print()
        if side == me:
            #move = random.choice(list(board))
            #prediction = nn.model.predict(restate)
            move = make_predict(restate)
            print("me:", move)
            try:
                client.make_move(move)
                grid[me].add(move)
                board.remove(move)
            except gthclient.MoveError as e:
                if e.cause == e.ILLEGAL:
                    print("me: made illegal move, passing")
                    client.make_move("pass")
        else:
            cont, move = client.get_move()
            print("opp:", move)
            if cont and move == "pass":
                print("me: pass to end game")
                client.make_move("pass")
                break
            else:
                if not cont:
                    break
                board.remove(move)
                grid[opp].add(move)

        side = gthclient.opponent(side)

    # Get the score for winner here:
    calc_score(npstate)

'''
if __name__ == "__main__":
    nn = Collection()
    nn.model.predict(state)
'''



