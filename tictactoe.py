"""
Tic Tac Toe Player
"""
import copy
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_X = sum(row.count('X') for row in board)
    count_O = sum(row.count('O') for row in board)
    
    # In the initial state, X goes first
    if count_X == count_O:
        return 'X'
    else:
        return 'O'


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == '':
                possible_actions.add((i, j))
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action

    # Ensure the action is valid
    if board[i][j] != None:
        raise ValueError("Invalid action. Cell is already occupied.")
    
    # Create a deep copy of the board to avoid modifying the original
    new_board = copy.deepcopy(board)
    
    # Determine whose turn it is and make the move
    current_player = player(board)
    new_board[i][j] = current_player
    
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):    
        # Check rows
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] is not None:
            return board[i][0]
    
        # Check columns
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] is not None:
            return board[0][i]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None:
        return board[0][0]
    
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None:
        return board[0][2]
    
    return None
    


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # Check if there is a winner
    if winner(board):
        return True
    
    # Check if all cells are filled (tie)
    if all(board[i][j] != None for i in range(3) for j in range(3)):
       return True

    # If neither a winner nor a tie, the game is still in progress
    return False
    


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    winner_result = winner(board)

    if winner_result == 'X':
        return 1
    elif winner_result == 'O':
        return -1
    else:
        return 0
    
def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    def is_terminal(board): # to check if someone has won. 
        return winner(board) is not None or all(all(cell is not None for cell in row) for row in board)

    def max_value(board):
        if is_terminal(board):
            return evaluate(board)

        v = float('-inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = 'X'  # Simulate making a move
                    min_result = min_value(board)
                    board[i][j] = None  # Undo the move
                    if min_result > v:
                        v = min_result

        return v

    def min_value(board):
        if is_terminal(board):
            return evaluate(board)

        v = float('inf')
        best_move = None

        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = 'O'  # Simulate making a move
                    max_result = max_value(board)
                    board[i][j] = None  # Undo the move

                    if max_result < v:
                        v = max_result

        return v

    def evaluate(board):
        # Evaluation function (you can customize this based on your game logic)
        if winner(board) == 'X':
            return 1
        elif winner(board) == 'O':
            return -1
        else:
            return 0

    # Find the best move for the AI ('O') in the initial state
    best_move = None
    best_score = float('-inf')

    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = 'O'  # Simulate making a move
                score = max_value(board)
                board[i][j] = None  # Undo the move

                if score > best_score:
                    best_score = score
                    best_move = (i, j)

    return best_move