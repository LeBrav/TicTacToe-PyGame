import numpy as np
import random
import pygame

#PYGAMEINIT#############################################################
pygame.init()
gameDisplay = pygame.display.set_mode((512,512))

image_board = pygame.image.load('./board.png')
cross = pygame.image.load('./cross.png')
circle = pygame.image.load('./round.png')
gameDisplay.blit(image_board, (0,0))
###############################################################

#CONSTANTS#########################################################

SIZE_SQUARE = 170

###############################################################

#DEFINICIONS-FUNCIONS#####################################################
def create_board():
    return np.zeros((3,3))

def is_valid_location(row, col, board):
    return board[row][col] == 0

def edit_board(row, col, board, turn, gameDisplay):
    if Turn == 0:
        board[row][col] = 1
        gameDisplay.blit(cross, (col*SIZE_SQUARE,row*SIZE_SQUARE))
    else:
        board[row][col] = 2
        gameDisplay.blit(circle, (col*SIZE_SQUARE,row*SIZE_SQUARE))

def ask_position():
    if Turn == 0:
        row = int(input('Insert row (from 0 to 2)'))
        col = int(input('Insert column (from 0 to 2)'))
        while is_valid_location(row, col, board) == False:
            print('Not a valid location')
            row = int(input('Insert row (from 0 to 2)'))
            col = int(input('Insert column (from 0 to 2)'))
    else:
        row= random.randint(0, 2)
        col= random.randint(0, 2)
        while is_valid_location(row, col, board) == False:
            row= random.randint(0, 2)
            col= random.randint(0, 2)
        
    
    return row, col

def get_lines(board, row, col):
    diagonal1 = board.diagonal(0)
    diaognal2 = np.fliplr(board).diagonal(0)
    total_col = board[:,col]
    total_row = board[row]
    return [diagonal1, diaognal2,total_col, total_row]
    

def minimax(board, row, col):
    
    for x in range(3):
        for y in range(3):
            if board[x][y] == 0:
                board_test = np.copy(board)
                #si guanyes lesgo
                board_test[x][y] = 2
                list_matrix = get_lines(board_test, x, y)
                game_over, winner = is_game_over(board_test, list_matrix)
                print(game_over)
                if game_over is True:
                    
                    return x, y
    
    
    heuristic_board = np.zeros((3,3))
    
    for x in range(3):
        for y in range(3):
            if board[x][y] == 0:
                board_test2 = np.copy(board)
                #evita que guanyin
                board_test2[x][y] = 1
                list_matrix = get_lines(board_test2, x, y)
                game_over, winner = is_game_over(board_test2, list_matrix)
                if game_over is True:
                    return x, y
                
                #sino heuristica
                if np.count_nonzero(list_matrix[0] == 1) == 0 or np.count_nonzero(list_matrix[1] == 1) == 0 or np.count_nonzero(list_matrix[2] == 1) == 0 or np.count_nonzero(list_matrix[3] == 1) == 0:
                    heuristic_board[x][y] = 5
                if np.count_nonzero(list_matrix[0] == 1) == 0 and np.count_nonzero(list_matrix[1] == 1) == 0 or np.count_nonzero(list_matrix[2] == 1) == 0 or np.count_nonzero(list_matrix[3] == 1) == 0:
                    heuristic_board[x][y] = 10
                if np.count_nonzero(list_matrix[0] == 1) == 0 and np.count_nonzero(list_matrix[1] == 1) == 0 and np.count_nonzero(list_matrix[2] == 1) == 0 or np.count_nonzero(list_matrix[3] == 1) == 0:
                    heuristic_board[x][y] = 15
                if np.count_nonzero(list_matrix[0] == 1) == 0 and np.count_nonzero(list_matrix[1] == 1) == 0 and np.count_nonzero(list_matrix[2] == 1) == 0 and np.count_nonzero(list_matrix[3] == 1) == 0:
                    heuristic_board[x][y] = 20
                    
    maxValue = np.amax(heuristic_board)
    
    while True:
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        if heuristic_board[x][y] == maxValue and board[x][y] == 0:
            return x, y


def random_pick(board, row, col):
    row= random.randint(0, 2)
    col= random.randint(0, 2)
    while is_valid_location(row, col, board) == False:
        row= random.randint(0, 2)
        col= random.randint(0, 2)
    return row, col

def is_game_over(board, list_matrix):
    game_over = False
    winner = 2  #circle = 0, cross = 1, empate = 2
    empate = False
    if np.all((list_matrix[0] == 1)):
        game_over = True
        winner = 1
    elif np.all((list_matrix[1] == 1)):
        game_over = True
        winner = 1
    elif np.all((list_matrix[2] == 1)):
        game_over = True
        winner = 1
    elif np.all((list_matrix[3] == 1)):
        game_over = True
        winner = 1
    elif np.all((list_matrix[0] == 2)):
        game_over = True
        winner = 0
    elif np.all((list_matrix[1] == 2)):
        game_over = True
        winner = 0
    elif np.all((list_matrix[2] == 2)):
        game_over = True
        winner = 0
    elif np.all((list_matrix[3] == 2)):
        game_over = True
        winner = 0
    elif np.all((board != 0)):
        game_over = True
        
    return game_over, winner
################################################################################


#MAIN############################################################################
board = create_board()

game_over = False
Turn = random.randint(0, 1)
play = False
row = 0
col = 0

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
            
        if Turn == 0:
            if event.type == pygame.MOUSEBUTTONUP:
               x, y = pygame.mouse.get_pos()
               row = int(y/SIZE_SQUARE)
               col = int(x/SIZE_SQUARE)
               if is_valid_location(row, col, board):
                   play = True
        else:           
            row, col = minimax(board, row, col)
            #row, col = random_pick(board, row, col)
            play = True
                
        if play:
            edit_board(row, col, board, Turn, gameDisplay)
            list_matrix = get_lines(board, row, col)
            game_over, winner = is_game_over(board, list_matrix)
            play = False
            Turn +=1
            Turn = Turn %2
            print(board)
    
    
    pygame.display.update()

if winner == 2:
    print('Empate')
else:
    if winner == 0:
        print('El PC wins bro')
    else:
        print('Tu guanyes tete')
    
pygame.quit()
print('THE END')
######################################################################################