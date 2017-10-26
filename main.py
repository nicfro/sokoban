import numpy as np


'''
w = wall
e = empty
g = goal
b = box
@ = box on goal
p = player
# = player on goal


'''
board = np.array([["w","w","w","w","w","w"],
				  ["w","e","e","e","e","w"],
				  ["w","e","e","e","e","w"],
				  ["w","p","b","e","g","w"],
				  ["w","e","e","e","e","w"],
				  ["w","e","e","e","e","w"],
				  ["w","w","w","w","w","w"]])

find_player = np.where(board=="p")
player_pos = np.array((find_player[0][0],find_player[1][0]))

def legalMove(position,board,direction):
	move = board[tuple(position + direction)]

	if move == "e":
		return 1
	if move == "g":
		return 1
	if move == "w":
		return 0
	if move == "b" or "@":
		next_to_box = board[tuple(position + direction + direction)]
		if (next_to_box == "e") or (next_to_box == "g"):
			return 1
		else:
			return 0

def move(position, board, direction):
	move = board[tuple(position + direction)]

	if move != "b":
		board[tuple(position + direction)] = "p"
		board[tuple(position)] = "e"

	if move == "g":
		board[tuple(position + direction)] = "#"
		board[tuple(position)] = "e"

	if move == "b" or "@":
		board[tuple(position)] = "e"
		next_to_box = board[tuple(position + direction + direction)]
		if next_to_box == "g":
			board[tuple(position + direction + direction)] = "@"
		else: 
			board[tuple(position + direction + direction)] = "b"
		if move == "g":
			board[tuple(position + direction)] = "#"
		else:
			board[tuple(position + direction)] = "p"
	positon = position + direction
	return board, position



R = (0,1)
L = (0,-1)
U = (-1,0)
D = (1,0)


if legalMove(player_pos, board, U):
	new_board, new_position = move(player_pos, board, U)

if legalMove(player_pos, new_board, R):
	new_board, new_position = move(new_position, new_board, R)
#print(board[tuple(player_pos+R+R)])
print(board)
#print(tuple(player_pos-(0,1)))