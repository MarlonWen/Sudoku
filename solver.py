import time
import random
import copy

def is_valid(board, row, col, num):
    '''
    Check if move is valid
    '''
    # Check if number appears more than twice in column
    for i in range(1, 10):
        if board[row][(col + i) % 9] == num:
            return False
        
    # Check if number appears more than twice in row
    for i in range(1, 10):
        if board[(row + i) % 9][col] == num:
            return False
        
    # Check if number appears more than twice in 3x3 grids
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True
        

def solution(board, num_count):
    '''
    Returns solved board
    '''
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == 0:
                for num in num_count:
                    # Check if move is valid, if so, play the move
                    if is_valid(board, row, col, num):
                        board[row][col] = num
                        if solution(board, num_count):
                            return board
                        # Backtrack / undo last move
                        board[row][col] = 0
                return None
    # Base case
    return board

def is_solvable(board, num_count):
    '''
    Returns True if solution exists False otherwise
    '''
    empty = find_empty(board)
    # Base case
    if empty == None:
        return True

    row, col = empty

    # Check if move is valid, if so, play the move
    for num in num_count:
        if is_valid(board, row, col, num):
            board[row][col] = num
            if is_solvable(board, num_count):
                return True
            # Backtrack / undo last move
            board[row][col] = 0
    return False
    

def find_empty(board):
    '''
    Finds the next empty cell
    '''
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == 0:
                return row, col
    return None

def find_num_count(board):
    '''
    Finds the number of occurences of each number 1-9
    '''
    # Initialize dictionary
    num_count = dict()
    for i in range(1, 10):
        num_count[i] = 0
    
    # Iterate over each cell
    for row in range(len(board)):
        for col in range(len(board)):
            number = board[row][col] 
            if number != 0:
                num_count[number] += 1
    
    return num_count

def create_puzzle(difficulty):
    board = [[0 for _ in range(9)] for _ in range(9)]
    board = solution(board, random.sample(range(1, 10), 9))  
    board = remove_numbers(board, difficulty)
    return board

def remove_numbers(board, count):
    for i in range(count):
        ranRow = random.randint(0,8)
        ranCol = random.randint(0,8)
        while board[ranRow][ranCol] == 0:
            ranRow = random.randint(0,8)
            ranCol = random.randint(0,8)
        temp = board[ranRow][ranCol]
        board[ranRow][ranCol] = 0
        num_count = find_num_count(board)
        num_count = sorted(range(1, 10), key=lambda num: num_count[num])
        if not is_solvable:
            board[ranRow][ranCol] = temp
            continue
    return board



# Test
'''
board = [[0, 0, 0, 0, 6, 0, 3, 0, 0], 
         [0, 0, 0, 5, 0, 0, 0, 2, 0], 
         [1, 0, 6, 0, 0, 0, 0, 7, 0], 
         [3, 7, 0, 0, 0, 2, 0, 0, 0], 
         [4, 0, 0, 0, 0, 3, 0, 0, 0], 
         [0, 0, 0, 9, 5, 8, 0, 0, 0], 
         [0, 9, 0, 0, 0, 0, 0, 0, 0], 
         [0, 8, 0, 0, 2, 0, 0, 0, 5],
         [0, 0, 3, 0, 0, 0, 9, 0, 8]]

start_time = time.time()
# List in ascending order of number of occurences
num_count = find_num_count(board)
num_count = sorted(range(1, 10), key=lambda num: num_count[num])
print(solution(board, num_count))
end_time = time.time()
print(end_time - start_time)
'''