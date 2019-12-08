#!/usr/bin/python3

# Random-move Gothello player.

import random
import sys

import gthclient

me = sys.argv[1]
opp = gthclient.opponent(me)

client = gthclient.GthClient(me, "localhost", 0)
#client = gthclient.GthClient(me, "barton.cs.pdx.edu", 0)

def letter_range(letter):
    for i in range(5):
        yield chr(ord(letter) + i)

board = {letter + digit
         for letter in letter_range('a')
         for digit in letter_range('1')}

grid = {"white": set(), "black": set()}

def update_position():
    for digit in letter_range('1'):
        for letter in letter_range('a'):
            pos = letter + digit
            print("pos is: \n: ", pos)
            lib1 = False
            lib2 = False
            lib3 = False
            lib4 = False
            if pos in grid["white"]:
                if (letter == 'e'):
                    lib1 = False
                else:
                    lib1 = chr(ord(letter)+1) + digit
                    if lib1 in grid["black"]:
                        lib1 = False
                    else:
                        lib1 = True

                if (digit == '5'):
                    lib2 = False
                else:
                    lib2 = letter + chr(int(digit)+1)
                    if lib2 in grid["black"]:
                        lib2 = False
                    else:
                        lib2 = True

                if (letter == 'a'):
                    lib3 = False
                else:
                    lib3 = chr(ord(letter)-1) + digit
                    if lib3 in grid["black"]:
                        lib3 = False
                    else:
                        lib3 = True


                if (digit == '1'):
                    lib4 = False
                else:
                    lib4 = letter + chr(int(digit)-1)
                    if lib4 in grid["black"]:
                        lib4 = False
                    else:
                        lib4 = True

                result = check_coordinality(lib1, lib2, lib3, lib4)
                # white piece has been captured.
                if result == True:
                    print("for: \n", pos)
                    print("L1 is: \n", lib1)
                    print("L2 is: \n", lib2)
                    print("L3 is: \n", lib3)
                    print("L4 is: \n", lib4)
                    #piece = "*"
                    # remove piece from white set.
                    # add piece to black set. 
                    grid["white"].remove(pos)
                    grid["black"].add(pos)
                    show_position()
                else:
                    print("result was false \n")
                    print("for: \n", pos)
                    print("L1 is: \n", lib1)
                    print("L2 is: \n", lib2)
                    print("L3 is: \n", lib3)
                    print("L4 is: \n", lib4)
                    print("#########################################################################################\n")
                # piece = "O"
            elif pos in grid["black"]:
                if (letter == 'e'):
                    lib1 = False
                else:
                    lib1 = chr(ord(letter)+1) + digit
                    if lib1 in grid["white"]:
                        lib1 = False
                    else:
                        lib1 = True

                if (digit == '5'):
                    lib2 = False
                else:
                    lib2 = letter + chr(int(digit)+1)
                    if lib2 in grid["white"]:
                        lib2 = False
                    else:
                        lib2 = True
 
                if (letter == 'a'):
                    lib3 = False
                else:
                    lib3 = chr(ord(letter)-1) + digit
                    if lib3 in grid["white"]:
                        lib3 = False
                    else:
                        lib3 = True

                    
                if (digit == '1'):
                    lib4 = False
                else:
                    lib4 = letter + chr(int(digit)-1)
                    if lib4 in grid["white"]:
                        lib4 = False
                    else:
                        lib4 = True

                result = check_coordinality(lib1, lib2, lib3, lib4)
                # black piece has been captured.
                if result == True:
                    print("for: \n", pos)
                    print("L1 is: \n", lib1)
                    print("L2 is: \n", lib2)
                    print("L3 is: \n", lib3)
                    print("L4 is: \n", lib4)
                    # piece = "*"
                    # remove piece from black set.
                    # add piece to white set. 
                    grid["black"].remove(pos)
                    grid["white"].add(pos)
                    show_position()

            # piece = "*"
            #else:
                #piece = "."
                #print(piece, end="")
                #print()

# check if a piece is caputred.
def check_coordinality(lib1, lib2, lib3, lib4):
    #if any of the 4 coordinalities have the same color return false.
    if (lib1 == True or lib2==True or lib3==True or lib4==True): 
        return False
    # all 4 coordinalities are caputred piece is caputred, return True.
    elif(lib1==False and lib2==False and lib3==False and lib4==False):
        return True

def show_position():
    update_position()
    for digit in letter_range('1'):
        for letter in letter_range('a'):
            pos = letter + digit
            if pos in grid["white"]:
                piece = "O"
            elif pos in grid["black"]:
                piece = "*"
            else:
                piece = "."
            print(piece, end="")
        print()

side = "black"

while True:
    show_position()
    if side == me:
        move = random.choice(list(board))
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
