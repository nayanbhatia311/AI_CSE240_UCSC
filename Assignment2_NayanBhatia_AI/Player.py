
import numpy as np
from operator import itemgetter

wins = 0        
class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)


    def validMoves(self, board):
        mov = []
        column=7
        rows=5
        for col in range(column):
            for row in range(rows,-1,-1):
                if board[row][col] == 0:
                    mov.append([row, col])
                    break
        return mov

    def count_values(self, board, num, player_num):
        no_wins = 0 
        win_string = '{0}' * num 
        win_string = win_string.format(player_num)
        stringConversion = lambda a: ''.join(a.astype(str))

        def check_rows(b):
            count = 0
            for row in b:
                if win_string in stringConversion(row):
                    count += stringConversion(row).count(win_string) 
            return count

        def check_columns(b):
            return check_rows(b.T)

        def check_cross(b):
            count = 0 
            for op in [None, np.fliplr]:
                op_board = op(b) if op else b
                main_diag = np.diagonal(op_board, offset=0).astype(np.int)
                if win_string in stringConversion(main_diag):
                    count += stringConversion(main_diag).count(win_string) 

                for i in range(1, b.shape[1]-3):
                    for offset in [i, -i]:
                        diag = np.diagonal(op_board, offset=offset)
                        diag = stringConversion(diag.astype(np.int))
                        if win_string in diag:
                            count += diag.count(win_string) 
            return count 
        no_wins = check_rows(board) + check_columns(board) + check_cross(board) 
        return no_wins

    def evaluation_function(self, board):
        outcome = 0
        player = self.player_number
        if (player == 1): 
            player_2 = 2
        else: 
            player_2 = 1
        outcome = self.count_values( board, 4, player) * 1000
        outcome += self.count_values( board, 3, player) * 100
        outcome += self.count_values( board, 2, player) * 10

        outcome -= self.count_values( board, 4, player_2) * 950 
        outcome -= self.count_values( board, 3, player_2) * 100 
        outcome -= self.count_values( board, 2, player_2) * 10

        return outcome

    def get_alpha_beta_move(self, board):
        values = []
    
        def alphabeta( board, depth, alpha, beta, player, player_2):
            for row, col in self.validMoves(board):
                board[row][col] = player
                alpha = max(alpha, min_value(board,alpha, beta,depth + 1 , player, player_2))
                values.append((alpha,col))
                board[row][col] = 0
            maxvalue = (max(values,key=itemgetter(1))[0]) 
            for item in values:
                if maxvalue in item:
                    maxindex = item[1]
                    break

            return (maxindex)

        def min_value(board,alpha,beta,depth,player, player_2):
            valid_moves = self.validMoves(board)
            if(depth == 4 or not valid_moves):
                return (self.evaluation_function(board))
            for row,col in valid_moves:
                board[row][col] = player_2 
                result = max_value(board, alpha, beta, depth+1, player, player_2)
                beta = min (beta, result)
                board[row][col] = 0
                if beta<= alpha:
                    return beta 
            return beta
        def max_value(board,alpha, beta, depth, player, player_2):
            valid_moves = self.validMoves(board)
            if(depth == 4 or not valid_moves):
                return (self.evaluation_function(board))
            for row, col in valid_moves:
                board[row][col] = player 
                result = min_value(board,alpha,beta,depth+1, player, player_2)
                alpha = max(alpha, result)
                board[row][col] = 0
                if alpha >= beta:
                    return alpha
            return alpha

        player = self.player_number
        if (player == 1): 
            player_2 = 2
        else: 
            player_2 = 1
        return (alphabeta(board, 0, -100000,+100000, player, player_2)) 
        raise NotImplementedError('Whoops I don\'t know what to do')


   
    def get_expectimax_move(self, board):
        values = []
        def expectimax(board, depth, player, player_2):
            alpha = - 1000000
            for row, col in self.validMoves(board):
                board[row][col] = player
                alpha = max(alpha, exp_val(board,depth - 1 , player, player_2))
                values.append((alpha,col))
                board[row][col] = 0

            maxvalue = (max(values,key=itemgetter(1))[0]) 
            for item in values:
                if maxvalue in item:
                    maxindex = item[1]
                    break

            return (maxindex)
        def max_val(board, depth, player,player_2):
            valid_moves = self.validMoves(board)
            if (depth == 0 or not valid_moves): 
                return (self.evaluation_function(board))
            bestValue = -100000
            for row,col in valid_moves:
                board[row][col] = player 
                val = exp_val(board, depth - 1, player, player_2)
                bestValue = max(bestValue, val);
            return bestValue
        def exp_val(board, depth, player, player_2): 
            valid_moves = self.validMoves(board)
            lengthmoves = len(valid_moves)
            print (lengthmoves)
            if (depth == 0 or not valid_moves): 
                return (self.evaluation_function(board))
            expectedValue = 0
            for row,col in valid_moves:
                board[row][col] = player_2 
                val = max_val(board , depth-1, player, player_2)
                expectedValue += val


            return (expectedValue/lengthmoves)

        player = self.player_number
        if (player == 1): 
            player_2 = 2
        else: 
            player_2 = 1
        return (expectimax(board, 8 , player, player_2))

        raise NotImplementedError('Whoops I don\'t know what to do')


class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):

        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))
        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move