from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from flask import Flask, url_for, render_template, request, redirect, jsonify
import cgi
from board import *
from os.path import join

tileMap = {0:(0,0), 1:(0,1), 2:(0,2), 3:(1,0), 4:(1,1), 5:(1,2), 6:(2,0), 7:(2,1), 8:(2,2)}

buttonMap = {(0,0):0, (0,1):1, (0,2):2, (1,0):3, (1,1):4, (1,2):5, (2,0):6, (2,1):7, (2,2):8}


def add(a, b): 
	return a+b

app = Flask(__name__,static_folder='assets')

ticTacToe = Game()
@app.route('/')
def index():
	ticTacToe.startNewGame()
	return render_template('index.html')#, instances = instances)


@app.route('/_getmove')
def getmove():
	move = request.args.get('a')
	print move
	row, column = tileMap[int(move)]
	isValid= ticTacToe.makeMove(row,column)
	print isValid

	buttonId = -1
	GameOver = 'False'

	if isValid: 
		# row, column = ticTacToe.compMove()
		score, row, column = MiniMax(10,ticTacToe.board,2,True)
		ticTacToe.makeMove(row,column)
		buttonId = buttonMap[(row,column)]

	gameOver, player = ticTacToe.isGameOver()
	print gameOver,player

	# 3=not Over,2=player2 win,1=player1 win, 0=draw
	isWin = 3
	if gameOver: 
		#Draw State, player== 0
		if player == 0:
			#'Nobody won. It is a DRAW! :'
			isWin = 0
		#Either Player 1 or Player 2 is the Winner!
		else:
			#'player {} is the winner!'.format(player)
			isWin = player

	ticTacToe.printBoard()
	return jsonify(isValid=isValid, compButton=str(buttonId), playerButton=str(move), isWin=isWin)
	
	
if __name__ == '__main__': 
	app.run(host = '0.0.0.0', port = 5000)


