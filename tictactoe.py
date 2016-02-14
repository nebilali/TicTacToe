from copy import deepcopy

class Board():
	'''
		Board represented by 3x3 arrary. 
		0 = Empty 
		1 =	player 1 space
		2 = player 2 space
	'''
	def __init__(self,board = None):
		# starts Empty, all zero
		if board==None: 
			self.board = [[0,0,0],[0,0,0],[0,0,0]]
		else: 
			#Initalize with given board
			self.board = board 

	def isGameOver(self):
		#check one player at a time
		for player in [1,2]:
		
			#check rows
			for row in range(len(self.board)):
				homogenousTiles = 0
				for column in range(len(self.board[row])):
					if self.board[row][column] == player: 
						homogenousTiles += 1
				if homogenousTiles == 3: 
					return True, player

			#check columns
			numColumns = len(self.board[0])
			for column in range(numColumns):
				homogenousTiles = 0
				for row in range(len(self.board)):
					if self.board[row][column] == player: 
						homogenousTiles += 1
				if homogenousTiles == 3: 
					return True, player

			#check diagnols -- assumes board is square
			homogenousTiles = 0
			for row in range(len(self.board)): 
				if self.board[row][row] == player: 
					homogenousTiles += 1 
			if homogenousTiles == 3: 
					return True, player

			homogenousTiles = 0
			for column, row in enumerate(reversed(range(len(self.board)))): 
				if self.board[row][column] == player: 
					homogenousTiles += 1 
			if homogenousTiles == 3: 
					return True, player

		#No one won yet

		return self._isDraw(), 0

	def _isDraw(self): 
		'''
			Checks if ther are any empty spaces on the board.
			Used with isGameOver() to determine if there is a draw.
				- Not deterministic of Draw without isGameOver()
		'''
		isDraw = True
		for row in range(len(self.board)):
			for column in range(len(self.board[row])):
				if self.board[row][column] == 0: 
					isDraw = False
		return isDraw

	def makeMove(self, player, row, column): 
		'''
			player makes move.
			Returns true is succesful, otherwise false. 
			Arguments:
				row, column : board positions 
				player : player making move
		'''

		if self.board[row][column] != 0: 
			return False

		self.board[row][column] = player
		return True

	def resetBoard(self): 
		self.board = [[0,0,0],[0,0,0],[0,0,0]]

	def printBoard(self): 
		for row in self.board: 
			print row
		print ''

	def _HeuristicHelper(self,player):
		HeuristicValue = 0
		
		scoreDictionary = {3:100, 2:10, 1:1, 0:0}

		#check rows
		for row in range(len(self.board)):
			homogenousTiles = 0
			for column in range(len(self.board[row])):
				if self.board[row][column] == player: 
					homogenousTiles += 1
			HeuristicValue += scoreDictionary[homogenousTiles]
		
		#check columns
		numColumns = len(self.board[0])
		for column in range(numColumns):
			homogenousTiles = 0
			for row in range(len(self.board)):
				if self.board[row][column] == player: 
					homogenousTiles += 1
			HeuristicValue += scoreDictionary[homogenousTiles]

		#check diagnols -- assumes board is square
		homogenousTiles = 0
		for row in range(len(self.board)): 
			if self.board[row][row] == player: 
				homogenousTiles += 1 
		HeuristicValue += scoreDictionary[homogenousTiles]

		homogenousTiles = 0
		for column, row in enumerate(reversed(range(len(self.board)))): 
			if self.board[row][column] == player: 
				homogenousTiles += 1 
		HeuristicValue += scoreDictionary[homogenousTiles]

		return HeuristicValue

	def getHeuristicValue(self,player): 
		if player == 1: 
			otherPlayer = 2
		else:  
			otherPlayer = 1
		
		return self._HeuristicHelper(player) - self._HeuristicHelper(otherPlayer)

	def getChildren(self,player):
		'''
			One Layer BFS
			Returns all possible givin player's turn 
			Arguments: 
				player - either 1 or 2, determines player turn 
		'''
		childBoards = []
		for row in range(len(self.board)):
			for column in range(len(self.board[row])):
				if self.board[row][column] == 0: 
					childBoard = deepcopy(self)
					childBoard.makeMove(player,row,column)
					childBoards.append((childBoard,row,column))
		return childBoards



class Game(): 
	def __init__(self):
		'''
			variables: 
				turnCounter: determines if players 1's or 2's turn
		'''
		self.board = Board()
		self.turnCounter = 1 

	def getActivePlayer(self):
		'''
			Who's turn is it?!?
		'''
		if self.turnCounter%2:
			player = 1 
		else: 
			player = 2

		return player

	def makeMove(self, row, column): 
		'''
			player makes move.
			Utilizes Board.makeMove()
			Arguments:
				row, column : board positions 

		'''
		player = self.getActivePlayer()
		isGoodMove = self.board.makeMove(player, row, column)
		
		if isGoodMove:
			self.turnCounter += 1
			return True
		else:
			return False

	def isGameOver(self):
		'''
			Utilizes Board.isGameOver()
			Returns: Boolean, int 
				if Boolean == True: 
					int: 
						1 - player1 is the winner
						2 - player2 is the winner
						0 - game ended in a draw
		'''

		return self.board.isGameOver()

	def printBoard(self): 
		self.board.printBoard()

	def startNewGame(self): 
		self.board.resetBoard()
		self.turnCounter = 1

	def compMove(self):
		score, row, column = MiniMax(6,self.board,2,True)	
		print 'here'
		return row, column


def MiniMax(depth, board,player,maxPlayer):
	'''
		AI algorithm 
		Arguments: 
			depth: int - for depth limited search of board states
			board: Board class - starting board state
			player: int (1 or 2) - players turn 
			maxPlayer: boolean - is Maximizing Player
		Returns: 
			bestValue, row, col 

			bestValue: int - board heurisitic value (For Testing)
			row: int - best row position on board
			col: int - best column position on board
	'''
	if player == 1: 
		otherPlayer = 2
	else: 
		otherPlayer = 1

	#Base Case
	if  depth == 0 or board.isGameOver()[0]:
		# board.printBoard()
		# print board.getHeuristicValue(1), board.getHeuristicValue(2), 'Player: {}'.format(player)
		return board.getHeuristicValue(player), None, None
		
	#Maximizing Player	
	if maxPlayer: 
		bestValue = -float('inf')
		for child,r,c in board.getChildren(player):
			v = MiniMax(depth-1, child, otherPlayer, False)[0]
			bestValue = max(bestValue,v)
			if bestValue == v: 
				row = r
				column = c
		return bestValue, row, column
	#Minimizing Player
	else: 
		bestValue = float('inf')
		for child, r, c in board.getChildren(player): 
			v = MiniMax(depth-1, child, otherPlayer, True)[0]
			bestValue = min(bestValue,v)
			if bestValue == v: 
				row = r
				column = c
		return bestValue, row, column

def PlayGame(numPlayers=2):
	ticTacToe = Game()

	while 1: 
		#make move
		while 1: 
			ticTacToe.printBoard()

			player = ticTacToe.getActivePlayer()
			print "it is player {}'s turn".format(player)
			
			#if numplayers is 1, Play with AI on second player turn 
			if numPlayers==1 and not ticTacToe.turnCounter%2:
				score, row, column = MiniMax(10,ticTacToe.board,2,True)
				print 'the Computer placed at row {}, column {}'.format(row,column)
				pass
			else: 
				print 'Enter row: '
				row = input() 
				print 'Enter col: '
				column = input()

			if ticTacToe.makeMove(row, column): 
				break
			print 'move not valid'

		gameOver, player = ticTacToe.isGameOver()
		print gameOver,player
		if gameOver: 
			#Draw State, player== 0
			if player == 0:
				print 'Nobody won. It is a DRAW! :'
			#Either Player 1 or Player 2 is the Winner!
			else:
				ticTacToe.printBoard()
				print 'player {} is the winner!'.format(player)
			
			#Handle End of Game
			print 'would you like to play a new game? y or n: '
			answer = raw_input()
			if answer == 'n': 
				break
			ticTacToe.startNewGame()



PlayGame()

if __name__ == '__main__':

	print 'Enter number of players: 1 or 2'
	numPlayers = input()
	PlayGame(numPlayers)
