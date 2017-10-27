import numpy as np
import pygame
import numpy as np
import math
 
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
pygame.init()
 
# Set the width and height of the screen [width, height]
size = [100, 100]
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Sokoban")
 
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

R = (0,1)
L = (0,-1)
U = (-1,0)
D = (1,0)

#savedImage = pygame.image.load("sprite.png").convert()
#b.image = pygame.image.load("sprite.png").convert()

pygame.key.set_repeat(50,50)


'''
w = wall
e = empty
g = goal
b = box
@ = box on goal
p = player
# = player on goal
'''
game = np.array([["w","w","w","w","w","w","w"],
				  ["w","e","e","e","e","e","w"],
				  ["w","e","e","e","e","e","w"],
				  ["w","p","g","b","e","e","w"],
				  ["w","e","e","e","e","e","w"],
				  ["w","e","e","e","e","e","w"],
				  ["w","w","w","w","w","w","w"]])

game = np.array([["e","e","w","w","w","w","w","e"],
				 ["w","w","w","e","e","e","w","e"],
				 ["w","g","p","b","e","e","w","e"],
				 ["w","w","w","e","b","g","w","e"],
				 ["w","g","w","w","b","e","w","e"],
				 ["w","e","w","e","g","e","w","w"],
				 ["w","b","e","b","b","b","g","w"],
				 ["w","e","e","e","g","e","e","w"],
				 ["w","w","w","w","w","w","w","w"]])

find_player = np.where(game=="p")
player_pos = np.array((find_player[0][0],find_player[1][0]))
goals = np.shape(np.where(game=="g"))[1]

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
	if legalMove(position, board, direction):
		move = board[tuple(position + direction)]
		current = board[tuple(position)]
		
		if move == "e":
			board[tuple(position + direction)] = "p"
			if current == "#":
				board[tuple(position)] = "g"
			else:
				board[tuple(position)] = "e"

		if move == "g":
			board[tuple(position + direction)] = "#"
			board[tuple(position)] = "e"

		if move == "b":
			next_to_box = board[tuple(position + direction + direction)]
			if next_to_box == "e":
				board[tuple(position + direction + direction)] = "b"
				board[tuple(position + direction)] = "p"
				if current == "#":
					board[tuple(position)] = "g"
				else:
					board[tuple(position)] = "e"
			if next_to_box == "g":
				board[tuple(position + direction + direction)] = "@"
				board[tuple(position + direction)] = "p"
				if current == "#":
					board[tuple(position)] = "g"
				else:
					board[tuple(position)] = "e"

		if move == "@":
			next_to_box = board[tuple(position + direction + direction)]
			if next_to_box == "e":
				board[tuple(position + direction + direction)] = "b"
				board[tuple(position + direction)] = "#"
				if current == "#":
					board[tuple(position)] = "g"
				else:
					board[tuple(position)] = "e"

			if next_to_box == "g":
				board[tuple(position + direction + direction)] = "@"
				board[tuple(position + direction)] = "#"
				if current == "#":
					board[tuple(position)] = "g"
				else:
					board[tuple(position)] = "e"

		new_position = position + direction
		return board, new_position
	else:
		return board, position

def isDone(board, goals):
	if np.shape(np.where(board=="@"))[1] == goals:
		return 1
	else:
		return 0

new_board, new_position = move(player_pos, game, L)




#print(board[tuple(player_pos+R+R)])
print(new_board)
#print(tuple(player_pos-(0,1)))

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = U
                new_board, new_position = move(new_position, new_board, direction)
                print(new_board)
            if event.key == pygame.K_DOWN:
                direction = D
                new_board, new_position = move(new_position, new_board, direction)
                print(new_board)
            if event.key == pygame.K_LEFT:
            	direction = L 
            	new_board, new_position = move(new_position, new_board, direction)
            	print(new_board)
            if event.key == pygame.K_RIGHT:
                direction = R
                new_board, new_position = move(new_position, new_board, direction)
                print(new_board)
                

    #screen.fill(BLACK)

    #pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
# Close the window and quit.
pygame.quit()