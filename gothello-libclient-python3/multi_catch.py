# File to check for multi piece capture
# In progress - found out Bart's show position function doesn't capture

import numpy as np

# Function will be called 4 times for each element,
# x and y will be the coordinate direction to check, they will
# increment or decriment by 1 each call.
'''
right = x+1, y
up = x, y+1
left = x-1, y
down = x, y-1
'''
def check_libs(piece, my_side, enemy_side, x, y, np_board, grid):
    '''
    Takes a piece, my side, opp side (black or white), direction (ENWS) in x and y coordinates, 
    numpy 2d array of board, dictionary grid of black and white pieces.
    '''
    #print("IN CHECK LIB {}, x={}, y={}".format(piece, x, y))
    # I've hit some outter wall or an enemy
    # x = letter, y = number
    if x > 4 or x < 0 or y > 4 or y < 0 or np_board[y][x] in grid[enemy_side]:
        return False, "BLOCKED"    # This current coordinate is not free.

    elif np_board[y][x] in grid[my_side]:   # It's a friendly
        return True, np_board[y][x]         # Return a piece because more checking needed

    else:   # It's blank and I'm safe
        return True, "BLANK"#None



# Then check if all liberties have been taken.
# If so, I've been captured
def am_i_free(grid, my_side, enemy_side):
    connected = set()  # Set of connected pieces
    captured = set()  # Set of captured pieces
    allies = ["","","",""]
    libs = [False, False, False, False]

    # I know it's a static array, gonna convert this to a 2d array
    moves = ['a1','b1','c1','d1','e1',
            'a2','b2','c2','d2','e2',
            'a3','b3','c3','d3','e3',
            'a4','b4','c4','d4','e4',
            'a5','b5','c5','d5','e5']
    
    np_moves = np.asarray(moves)    # Convert to numpy
    np_board = np.reshape(np_moves, (5, 5)) # Make the board 2d
    print(np_board)

    for piece in grid[my_side]:
        index = np.where(np_board == piece)  # Should get my y and x indexes (only 1 coord pair)
        let = index[1][0]   # Column
        dig = index[0][0]   # Row
        print("piece: {}, dig: {}, let: {}".format(piece, dig, let))
        
        libs[0], allies[0] = check_libs(piece, my_side, enemy_side, let+1, dig, np_board, grid)  # Right
        #print(allies)
        libs[1], allies[1] = check_libs(piece, my_side, enemy_side, let, dig+1, np_board, grid)  # Up
        #print(allies)
        libs[2], allies[2] = check_libs(piece, my_side, enemy_side, let-1, dig, np_board, grid)  # Left
        #print(allies)
        libs[3], allies[3] = check_libs(piece, my_side, enemy_side, let, dig-1, np_board, grid)  # Down
        #print(allies)
        print("le: {}, ln: {}, lw: {}, ls: {}, allies: {}".format(libs[0], libs[1], libs[2], libs[3], allies))

        print("grid[{}]: {}".format(my_side, grid[my_side]))
        print("Connected {}: {}".format(my_side, connected))
        print("Captured by {}: {}".format(enemy_side, captured))
        for ally in allies: # Loop through each side and see if I add them to set
            #print("in for loop len: {}".format(len(allies)))
            if ally != "BLANK" and ally != "BLOCKED" and ally not in connected:
                connected.add(ally) # Add all non None allies
                print(connected)

        #print("out of loop")
        # This checks for a single piece - all false means I've been captured by the other side...
        if not libs[0] and not libs[1] and not lib[2] and not libs[3]: # No sides free
            # Call capture function
            print("CAPTURE {}\n\n".format(piece))
            captured.add(piece)
            print("{}".format(captured))
            connected.discard(piece)    # Removes piece if it exists here, if not, then nothing
            print("{}".format(connected))
            #pass

        #update_grid(my_side, enemy_side, piece, grid) # Enemy captured a piece


def update_grid(rem_from, add_to, piece, grid):
    """
    Takes in three strings, a player to remove a piece from(black,white),
    a player to add a piece to(white,black), and a piece values(a5).
    """
    # Call the capture function to verify 
    grid[rem_from].remove(piece)
    grid[add_to].add(piece)
    print(grid)
