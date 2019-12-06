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

VIEW = False    # Switch this if we don't want to see game details

# Bart function for piece generation
def letter_range(letter):
    for i in range(5):
        yield chr(ord(letter) + i)


def show_position():
    """
    Function that shows the position to the user through standard output.
    Also creates the states to pass to models for prediction.
    returns two flattened numpy arrays, one of size 50 being a one hot encode
    and the other of size 25 being a flattened version of the output data.
    Note: Built off of Bart's random.
    """
    state = []  # Making a new state
    scoring_state = [] # Custom for counting
    for digit in letter_range('1'):
        for letter in letter_range('a'):
            pos = letter + digit
            if pos in grid["white"]:
                piece = '1'#"O"
                state.append(0)     # The enemy is the loser
                state.append(1)     # The enemy is the loser
                scoring_state.append(1)
            elif pos in grid["black"]:
                piece = '2'#"*"
                state.append(1)     # You gonna be the winner
                state.append(0)     # You gonna be the winner
                scoring_state.append(2)
            else:
                piece = '0'#"."
                state.append(0)     # These are blanks
                state.append(0)     # These are blanks
                scoring_state.append(0)
            
            if VIEW:
                print(piece, end="")
        if VIEW:
            print()
    
    if VIEW:
        print(state)
    return np.asarray(state), np.asarray(scoring_state)        # Give back 2 flattened array of data


def make_predict(restate):
    """
    Function given the 50 element state of 1's and 0's
    uses a neuronetwork prediction to determine a move.
    Then error checks to see if that move is valid to play
    based on the remaining contents of board.
    Later: do a search based on the top 3 predictions (if valid)
    return: string - my_move 
    """

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
        #print(board)
        #print("Valid")
        return my_move  # this move is valid so do it
    else:
        count = 1
        while my_move not in list(board):   # While my move is not valid
            #print("{} is not valid".format(my_move))
            # Get a new prediction:
            index = np.argmax(prediction[0])    
            prediction[0][index] = -10               # Previous prediction not good, try next best valid.
            my_move = moves[np.argmax(prediction[0])]   # Get a move that is valid?
            count += 1
        
        if VIEW:
            print("op-{}: {}".format(count, my_move))
        return my_move  # Next option
        #return random.choice(list(board))   # Legit, do something better than this later


def calc_score(npstate):
    """
    Figure out who won this game. Winner has the most pieces on the board
    at the end of the game.
    return: 1 to add a point for winning, 0 if I lost or draw
    """
    my_tiles = np.where(npstate == 2)[0]    # Where I(BLACK) placed my tiles
    opp_tiles = np.where(npstate == 1)[0]   # Where white placed their tiles
    if VIEW:
        print("my_tiles: {}\nopp_tiles: {}".format(my_tiles, opp_tiles))
    #print(my_tiles[0])

    my_score = len(my_tiles)
    opp_score = len(opp_tiles)
    if VIEW:
        print("my_score: {}\nopp_score: {}".format(my_score, opp_score))

    if my_score > opp_score:
        print("BLACK WINS")
        return 1    # add 1 for every win
    elif my_score < opp_score:
        print("WHITE WINS")
        return 0
    else:
        print("DRAW")
        return 0

# Building off Bart's code
def play_game(side):
    """
    Play the game and make moves against an opponent
    based on states collected.
    """
    while True:
        npstate, score_state = show_position()
        restate = np.reshape(npstate, (-1,50))
        if VIEW:
            print()
        if side == me:
            #move = random.choice(list(board))   # Using random
            move = make_predict(restate)       # Using Neuronet

            if VIEW:
                print("me:", move)
            try:
                client.make_move(move)
                grid[me].add(move)
                board.remove(move)
            except gthclient.MoveError as e:
                if e.cause == e.ILLEGAL:
                    if VIEW:
                        print("me: made illegal move, passing")
                    client.make_move("pass")
        else:
            cont, move = client.get_move()
            if VIEW:
                print("opp:", move)
            if cont and move == "pass":
                if VIEW:
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
    return calc_score(score_state)#npstate)




nn = ma.Collection()
me = sys.argv[1]
#opp = gthclient.opponent(me)

#client = gthclient.GthClient(me, "localhost", 0)
#client = gthclient.GthClient(me, "barton.cs.pdx.edu", 0)
'''
side = "black"

board = {letter + digit
         for letter in letter_range('a')
         for digit in letter_range('1')}

grid = {"white": set(), "black": set()}
'''
# Where the good stuff happens
# Loop through and play x amount of games to determine how good
# the ai approach is.
if __name__ == "__main__":

    wins = 0
    total_games = 100    # play 10 games and see how I do
    i = 0
    while i < total_games: 
        i += 1
        try:
            opp = gthclient.opponent(me)
            client = gthclient.GthClient(me, "barton.cs.pdx.edu", 0)

            side = "black"

            board = {letter + digit
                     for letter in letter_range('a')
                     for digit in letter_range('1')}

            grid = {"white": set(), "black": set()}

            wins += play_game(side)
            client.closeall()
            print("{}.\t{}/{}".format(i, wins, total_games))
            
        except (KeyboardInterrupt, SystemExit):
            raise
        
        except:
            print("ERROR on {}".format(i))
            i = i-1
            pass

