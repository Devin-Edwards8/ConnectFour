import numpy as np

PLAYER1 = 1
PLAYER2 = 2

def create_board():
    board = np.zeros((6,7))
    return board

def column_full(selection, board):
    return board[0][selection] != 0

def place_chip(selection, board, player):
    for x in range(5,-1,-1):
        if board[x][selection] == 0:
            board[x][selection] = player
            break

def check_status(board, p):
    for i in range(7):
        for j in range(5,2,-1):
            if board[j][i] == p and board[j-1][i] == p and board[j-2][i] == p and board[j-3][i] == p:
                print("\nPlayer " + str(p) + " wins!\n")
                print(board)
                return True

    for j in range(5,-1,-1):
        for i in range(4):
            if board[j][i] == p and board[j][i+1] == p and board[j][i+2] == p and board[j][i+3] == p:
                print("\nPlayer " + str(p) + " wins!\n")
                print(board)
                return True

    for i in range(4):
        for j in range(5,2,-1):
            if board[j][i] == p and board[j-1][i+1] == p and board[j-2][i+2] == p and board[j-3][i+3] == p:
                print("\nPlayer " + str(p) + " wins!\n")
                print(board)
                return True

    for i in range(6, 2, -1):
        for j in range(5,2,-1):
            if board[j][i] == p and board[j-1][i-1] == p and board[j-2][i-2] == p and board[j-3][i-3] == p:
                print("\nPlayer " + str(p) + " wins!\n")
                print(board)
                return True


board = create_board()
game_over = False
turn = 0
while not game_over:
    print(board)
    if turn == 0:
        while True:
            selection = input("Player 1 Make your Selection (1-7):")
            try:
                selection = int(selection)
            except:
                print("Please enter a number. \n")
                continue
            if selection < 1 or selection > 7:
                print("Please enter a number between 1 and 7.\n")
                continue
            break

        if column_full(selection - 1, board):
            print("please select a different column")
            turn += 1
        else:
            place_chip(selection - 1, board, PLAYER1)
    else:
        selection = int(input("Player 2 Make your Selection (1-7):"))
        if column_full(selection - 1, board):
            print("please select a different column")
            turn+=1
        else:
            place_chip(selection - 1, board, PLAYER2)

    game_over = check_status(board, PLAYER1)
    if not game_over:
        game_over = check_status(board, PLAYER2)
    if game_over:
        play_again = input("\nWould you like to play again? (y/n) : ")
        if play_again == "y":
            board = np.zeros((6,7))
            game_over = False

    turn += 1
    turn = turn % 2
