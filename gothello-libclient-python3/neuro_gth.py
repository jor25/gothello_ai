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
#import capture as cp
#import multi_catch as muc

VIEW = False    # Switch this if we don't want to see game details

# Bart function for piece generation
def letter_range(letter):
    for i in range(5):
        yield chr(ord(letter) + i)

def update_grid(rem_from, add_to, piece):
    """
    Takes in three strings, a player to remove a piece from(black,white),
    a player to add a piece to(white,black), and a piece values(a5).
    """
    # Call the capture function to verify 
    grid[rem_from].remove(piece)
    grid[add_to].add(piece)
    print(grid)


def show_position():
    """
    Shows the position to the user through standard output.
    Also creates the states to pass to models for predictions and scoring.
    Returns: two flattened numpy arrays, one of size 50 being a one hot encode
             and the other of size 25 being a flattened version of the output data.
    Note: Built off of Bart's random player.
    Note: The table output in this has been made upsidedown from previous
          implementation. Manually flipped the table in later functions.
    """
    # Adding in capture function
    #cp.update_position(grid)
    #muc.am_i_free(grid, "black", "white")
    #print(grid)
    state = []                              # Making a new state for model
    scoring_state = []                      # Custom state for counting score
    for digit in letter_range('1'):
        for letter in letter_range('a'):
            pos = letter + digit
            if pos in grid["white"]:
                piece = '1' #"O"        # loser player (WHITE)
                state.append(0)         # The enemy is the loser
                state.append(1)         # The enemy is the loser
                scoring_state.append(1)

            elif pos in grid["black"]:
                piece = '2' #"*"        # Winning player (BLACK)
                state.append(1)         # You gonna be the winner
                state.append(0)         # You gonna be the winner
                scoring_state.append(2)

            else:
                piece = '0' #"."        # Blank
                state.append(0)         # These are blanks
                state.append(0)         # These are blanks
                scoring_state.append(0)
            
            if VIEW:
                print(piece, end="")    # Show the board
        if VIEW:
            print()
    
    if VIEW:
        print(state)            # Show state of 50 elements
        print(scoring_state)    # Show scoring state

    return np.asarray(state), np.asarray(scoring_state)     # Give back 2 flattened array of data


def make_predict(restate):
    """
    Function given the 50 element state of 1's and 0's (onehot)
    uses a neural network prediction to determine a move.
    Then error checks to see if that move is valid to play
    based on the remaining contents of board.
    Later: do a search based on the top 3 predictions (if valid)
    return: string - my_move ie 'a5'
    """

    # The categorical labels of the board. (Technically it should be 5 on top)
    # but, in this case, we're using this version of the table.
    moves = ['a1','b1','c1','d1','e1',
            'a2','b2','c2','d2','e2',
            'a3','b3','c3','d3','e3',
            'a4','b4','c4','d4','e4',
            'a5','b5','c5','d5','e5']
    
    '''
    moves = ['a5','b5','c5','d5','e5',
            'a4','b4','c4','d4','e4',
            'a3','b3','c3','d3','e3',
            'a2','b2','c2','d2','e2',
            'a1','b1','c1','d1','e1']
    '''
    prediction = nn.model.predict(restate)      # Use model to predict move from given state
    my_move = moves[np.argmax(prediction[0])]   # Select move with corresponding index, ie my_move = a5

    if my_move in list(board):
        return my_move                          # This move is valid so DO IT

    else:
        count = 1                                       # Error check how many predictions were wrong
        while my_move not in list(board):               # While my move is not valid
            # Get a new prediction:
            index = np.argmax(prediction[0])            # Previous prediction no good, try next best valid.
            prediction[0][index] = -10                  # Negate bad prediction
            my_move = moves[np.argmax(prediction[0])]   # Get a move that is valid?
            count += 1                                  # Error checking How many times it's invalid
        
        if VIEW:
            print("alt-{}: {}".format(count, my_move))   # Display how many alteratives
        
        return my_move  # Next best/valid option


def calc_score(npstate):
    """
    Calculate who won this game given the scoring state of 25 elements.
    Winner has the most pieces on the board at the end of the game.
    returns: Three integers, basically one hot for win, loss, draw. 
             used to add a point for winning (1,0,0), losing(0,1,0), or draw(0,0,1)
    """
    my_tiles = np.where(npstate == 2)[0]    # Where I(BLACK) placed my tiles
    opp_tiles = np.where(npstate == 1)[0]   # Where white placed their tiles

    if VIEW:                                # Show my tiles and my opponent's tiles
        print("my_tiles: {}\nopp_tiles: {}".format(my_tiles, opp_tiles))

    my_score = len(my_tiles)                # My points = number of (2) tiles
    opp_score = len(opp_tiles)              # Enemy points = number of (1) tiles

    if VIEW:
        print("my_score: {}\nopp_score: {}".format(my_score, opp_score))

    if my_score > opp_score:
        print("BLACK WINS")     # Black won, give back 1,0,0
        return 1, 0, 0
    elif my_score < opp_score:
        print("WHITE WINS")     # White won, give back 0,1,0
        return 0, 1, 0
    else:
        print("DRAW")           # Draw, give back 0,0,1
        return 0, 0, 1


# Building off Bart's code
def play_game(side):
    """
    Given a side, black or white, play the game and make moves against an opponent
    based on states collected.
    """
    while True:
        npstate, score_state = show_position()      # Collect game states and scoring state
        restate = np.reshape(npstate, (-1,50))      # Convert game state to the right size
        if VIEW:
            print()
        if side == me:
            """ SELECT AI PLAYER HERE: """
            #move = random.choice(list(board))      # Using random  - set a flag to choose player later...
            move = make_predict(restate)            # Using Neuronet

            if VIEW:
                print("me:", move)                                  # Print my move
            try:
                client.make_move(move)                              # Then attempt to place the pieces
                grid[me].add(move)                                  # Place on the grid
                board.remove(move)                                  # Remove from board of available spots
            except gthclient.MoveError as e:
                if e.cause == e.ILLEGAL:
                    if VIEW:
                        print("me: made illegal move, passing")     # Made an illegal move
                    client.make_move("pass")                        # No move made - so pass
        else:
            cont, move = client.get_move()              # If it's opponent's turn - get their move
            if VIEW:
                print("opp:", move)
            if cont and move == "pass":
                if VIEW:
                    print("me: pass to end game")
                client.make_move("pass")                # Game end condition
                break
            else:
                if not cont:
                    break                               # Game end condition
                board.remove(move)                      # Remove available board move
                grid[opp].add(move)                     # Place on grid

        side = gthclient.opponent(side)                 # Who's side is it?

    # Get the score for winner here:
    return calc_score(score_state)




nn = ma.Collection()    # Global collection object
me = sys.argv[1]        # My side "black" or "white"


# Where the good stuff happens
# Loop through and play x amount of games to determine how good
# the ai approach is.
if __name__ == "__main__":
    """
    Main function is where all the good stuff happens,
    play x amount of games against bart's computer opponent to see
    how well each approach does. New players can be used via the move variable
    in the play_game function.
    """

    wins = 0                # Keep track of my wins
    losses = 0              # Keep track of my losses
    draws = 0               # Keep track of draws
    total_games = 100        # Play x games and see how I do
    i = 0                   # Just a counter

    while i < total_games:  # Loop for specified amount of games
        i += 1
        try:
            opp = gthclient.opponent(me)                                # Set opponent
            client = gthclient.GthClient(me, "barton.cs.pdx.edu", 0)    # Connect to server (Bart's)
            #client = gthclient.GthClient(me, "localhost", 0)

            side = "black"

            # Set up available board spots
            board = {letter + digit
                     for letter in letter_range('a')
                     for digit in letter_range('1')}

            # Set the grid
            grid = {"white": set(), "black": set()}

            win, loss, draw= play_game(side)        # Check if I won, loss, or tied a game
            wins += win                             # Increment wins
            losses += loss                          # Increment losses
            draws += draw                           # increment draws

            client.closeall()                       # Disconnect from server

            # Print individual game statistics
            print("Game #{} \twins: {}\t\tlosses: {}\tdraws: {}\twin perc: {}\n".format(
                    i, wins, losses, draws, round(float(wins/i), 2) ))
            
        except (KeyboardInterrupt, SystemExit):     # Lets me get out if i "ctrl-c"
            raise
        
        except:
            #print("ERROR on {}".format(i))      # If error in game, run the same game again.
            i = i-1
            pass

