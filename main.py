# Defines a simple artificially intelligent player agent, alpha-beta pruning search algorithm and score function

from random import *
from decimal import *
from copy import *
from MancalaBoard import *

# a constant
INFINITY = 1.0e400

class Player:
    """ A basic AI (or human) player """
    HUMAN = 0
    RANDOM = 1
    MINIMAX = 2
    ABPRUNE = 3
    CUSTOM = 4
    
    def __init__(self, playerNum, playerType, ply=0):
        """Initialize a Player with a playerNum (1 or 2), playerType (one of
        the constants such as HUMAN), and a ply (default is 0)."""
        self.num = playerNum
        self.opp = 2 - playerNum + 1
        self.type = playerType
        self.ply = ply

    def __repr__(self):
        """Returns a string representation of the Player."""
        return str(self.num)
        
    def minimaxMove(self, board, ply):
        """ Choose the best minimax move.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValue(nb, ply-1, turn)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValue(nextBoard, ply-1, turn)
            if s > score:
                score = s
        return score
    
    def minValue(self, board, ply, turn):
        """ Find the minimax value for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValue(nextBoard, ply-1, turn)
            if s < score:
                score = s
        return score


    # The default player defines a very simple score function
    def score(self, board):
        """ Returns the score for this player given the state of the board """
        if board.hasWon(self.num):
           return 100.0
        elif board.hasWon(self.opp):
           return 0.0
        else:
           return 50.0
    
    def alphaBetaMove(self, board, ply):
        """ Choose a move with alpha beta pruning.  Returns (score, move) """
        move = -1
        score = -INFINITY
        turn = self
        alpha = -INFINITY #variable for highest possible score that MAX can choose
        beta = INFINITY #variable for lowest possible score that MIN can choose
        for m in board.legalMoves(self):
            #for each legal move
            if ply == 0:
                #if we're at ply 0, we need to call our eval function & return
                return (self.score(board), m)
            if board.gameOver():
                return (-1, -1)  # Can't make a move, the game is over
            nb = deepcopy(board)
            #make a new board
            nb.makeMove(self, m)
            #try the move
            opp = Player(self.opp, self.type, self.ply)
            s = opp.minValueAB(nb, ply-1, turn, alpha, beta)
            #and see what the opponent would do next
            if s > score:
                #if the result is better than our best score so far, save that move,score
                move = m
                score = s
        #return the best score and move so far
        return score, move

    def maxValueAB(self, board, ply, turn, alpha, beta):
        """ Find the minimax value with alpha beta pruning for the next move for this player
        at a given board configuation. Returns score."""
        if board.gameOver(): #at the end of the tree so return the score 
            return turn.score(board)
        score = -INFINITY
        for m in board.legalMoves(self):
            if ply == 0: #at the specified depth level, start working back up tree
                print "turn.score(board) in max value is: " + str(turn.score(board))
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.minValueAB(nextBoard, ply-1, turn, alpha, beta)
            if s > alpha:
                alpha = s
            if alpha >= beta: #prune
                return alpha
        return alpha
    
    def minValueAB(self, board, ply, turn, alpha, beta):
        """ Find the minimax value with alpha beta pruning for the next move for this player
            at a given board configuation. Returns score."""
        if board.gameOver():
            return turn.score(board)
        score = INFINITY
        for m in board.legalMoves(self):
            if ply == 0:
                return turn.score(board)
            # make a new player to play the other side
            opponent = Player(self.opp, self.type, self.ply)
            # Copy the board so that we don't ruin it
            nextBoard = deepcopy(board)
            nextBoard.makeMove(self, m)
            s = opponent.maxValueAB(nextBoard, ply-1, turn,alpha,beta)
            if s < beta:
                beta = s
            if beta <= alpha: #prune 
                return beta
        return beta
    
                
    def chooseMove(self, board):
        """ Returns the next move that this player wants to make """
        if self.type == self.HUMAN:
            move = input("Please enter your move:")
            while not board.legalMove(self, move):
                print move, "is not valid"
                move = input( "Please enter your move" )
            return move
        elif self.type == self.RANDOM:
            move = choice(board.legalMoves(self))
            print "chose move", move
            return move
        elif self.type == self.MINIMAX:
            val, move = self.minimaxMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.ABPRUNE:
            val, move = self.alphaBetaMove(board, self.ply)
            print "chose move", move, " with value", val
            return move
        elif self.type == self.CUSTOM:
            val, move = self.alphaBetaMove(board, 9) #ply 9 so that it runs in less than 10 seconds
            print "chose move", move, " with value", val
            return move
        else:
            print "Unknown player type"
            return -1

class smartPlayer(Player):
    """ Defines a player that knows how to evaluate a Mancala gameboard
        intelligently """


    def score(self, board):
        """ Evaluate the Mancala board for this player """
        if board.hasWon(self.num): #current player wins
            return 100.0
        elif board.hasWon(self.opp): #opponent wins
            return -100.0
        else:
            countP1 = board.scoreCups[0]
            countP2 = board.scoreCups[1]
            totalOppBeads = 0
            cupsEmpty = 0
            if self.num == 1: #player 1
                for cup in range(0, len(board.P2Cups)):
                    totalOppBeads = board.P2Cups[cup] + totalOppBeads #count opponent's beads
                for cup in range(0, len(board.P1Cups)):
                    if board.P1Cups[cup] == 0:
                        cupsEmpty+= 1 #counts number of empty cups on player's side
                if board.makeMoveHelp == True:
                    goAgain = 10 #adds value to score if move lets player go again
                else:
                    goAgain = 0
                utility = countP1 - countP2 - totalOppBeads + goAgain + cupsEmpty 
            else: #player 2
                for cup in range(0, len(board.P1Cups)):
                    totalOppBeads = board.P1Cups[cup] + totalOppBeads #count opponent's beads
                for cup in range(0, len(board.P2Cups)):
                     if board.P2Cups[cup] == 0:
                        cupsEmpty+= 1 #counts number of empty cups on player's side
                if board.makeMoveHelp == True:
                    goAgain = 10 #adds value to score if move lets player go again
                else:
                    goAgain = 0
                utility = countP2 - countP1 - totalOppBeads + goAgain + cupsEmpty
            return utility


        print "Calling score in MancalaPlayer"
        return Player.score(self, board)
        




