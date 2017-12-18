import numpy as np
import pygame
import math
import copy
import pickle
from mapReader import reader

BLACK = (0,     0,   0)
WHITE = (255, 255, 255)
GREEN = (0,   255,   0)
RED   = (255,   0,   0)
BLUE =  (0  ,   0, 255)

sprite_folder ="sprites/"

image_empty       = pygame.image.load(sprite_folder + "empty.png")
image_wall        = pygame.image.load(sprite_folder + "wall.png")
image_player      = pygame.image.load(sprite_folder + "player.png")
image_player_goal = pygame.image.load(sprite_folder + "playerGoal.png")
image_goal        = pygame.image.load(sprite_folder + "goal.png")
image_box         = pygame.image.load(sprite_folder + "box.png")
image_box2        = pygame.image.load(sprite_folder + "box.png")#Outcomment if not poke
image_box_goal    = pygame.image.load(sprite_folder + "boxGoal.png")

sprite_width = 50
sprite_height = 50

'''
w = wall
e = empty
g = goal
b = box
@ = box on goal
p = player
# = player on goal
'''

game = np.array([["#","#","#","#","#","#","#","#"],
				 ["#","#","#"," "," "," ","#","#"],
				 ["#",".","@","$"," "," ","#","#"],
				 ["#","#","#"," ","$",".","#","#"],
				 ["#",".","#","#","$"," ","#","#"],
				 ["#"," ","#"," ","."," ","#","#"],
				 ["#","$"," ","*","$","$",".","#"],
				 ["#"," "," "," ","."," "," ","#"],
				 ["#","#","#","#","#","#","#","#"]])

maps = reader()

def getLevel(level):
	return(np.asarray(maps[level]))

level = 36
game = getLevel(level)


pygame.init()

def initializeScreen(game):
	size = np.shape(game)

	screen_width = size[1]*sprite_width
	screen_height = size[0]*sprite_height

	# Set the width and height of the screen [width, height]
	return pygame.display.set_mode([screen_width,screen_height])

screen = initializeScreen(game)

R = (0,1)
L = (0,-1)
U = (-1,0)
D = (1,0)
NO = (0,0)

clock = pygame.time.Clock()
pygame.key.set_repeat(100,100)
pygame.display.set_caption("Sokoban")

def findGoals(game):
	goals1 = np.shape(np.where(game=="."))[1]
	goals2 = np.shape(np.where(game=="*"))[1]
	return goals1+goals2

def findPlayer(game):
	find_player = np.where(game=="@")
	player_pos = np.array((find_player[0][0],find_player[1][0]))
	return player_pos

def legalMove(position,board,direction):
	move = board[tuple(position + direction)]

	if move == " ":
		return 1
	if move == ".":
		return 1
	if move == "#":
		return 0
	if move == "$" or "*":
		next_to_box = board[tuple(position + direction + direction)]
		if (next_to_box == " ") or (next_to_box == "."):
			return 1
		else:
			return 0

def move(position, board, direction):
	if legalMove(position, board, direction):
		move = board[tuple(position + direction)]
		current = board[tuple(position)]

		if move == " ":
			board[tuple(position + direction)] = "@"
			if current == "+":
				board[tuple(position)] = "."
			else:
				board[tuple(position)] = " "

		if move == ".":
			board[tuple(position + direction)] = "+"
			if current == "+":
				board[tuple(position)] = "."
			else:
				board[tuple(position)] = " "

		if move == "$":
			next_to_box = board[tuple(position + direction + direction)]
			if next_to_box == " ":
				board[tuple(position + direction + direction)] = "$"
				board[tuple(position + direction)] = "@"
				if current == "+":
					board[tuple(position)] = "."
				else:
					board[tuple(position)] = " "
				
			if next_to_box == ".":
				board[tuple(position + direction + direction)] = "*"
				board[tuple(position + direction)] = "@"
				if current == "+":
					board[tuple(position)] = "."
				else:
					board[tuple(position)] = " "
				

		if move == "*":
			next_to_box = board[tuple(position + direction + direction)]
			if next_to_box == " ":
				board[tuple(position + direction + direction)] = "$"
				board[tuple(position + direction)] = "+"
				if current == "+":
					board[tuple(position)] = "."
				else:
					board[tuple(position)] = " "
				

			if next_to_box == ".":
				board[tuple(position + direction + direction)] = "*"
				board[tuple(position + direction)] = "+"
				
				if current == "+":
					board[tuple(position)] = "."
				else:
					board[tuple(position)] = " "

		new_position = position + direction
		return copy.copy(board), new_position
	else:
		return copy.copy(board), position

def isDone(board, goals):
	if np.shape(np.where(board=="*"))[1] == goals:
		return 1
	else:
		return 0

#create board, get position and find number of goals
new_board, new_position = move(findPlayer(game), game, NO)
number_of_goals = findGoals(new_board)


# -------- Main Program Loop -----------
anim_count = 1
moves = 0
done = False

while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                direction = U
            if event.key == pygame.K_DOWN:
                direction = D
            if event.key == pygame.K_LEFT:
            	direction = L
            if event.key == pygame.K_RIGHT:
                direction = R
            #TODO: This is why other keys will trigger movement
            moves += 1
            new_board, new_position = move(new_position, new_board, direction)

            if event.key == pygame.K_r:
                new_board = copy.copy(game)
                new_position = findPlayer(game)

    for row in range(len(new_board)):
        for column in range(len(new_board[0])):
            current_elem = new_board[row][column]
            if current_elem == "#":
                image = image_wall
            elif current_elem == "@":
                image = image_player
            elif current_elem == ".":
                image = image_goal
            elif current_elem == "$":
                if anim_count == 1:
                    image = image_box
                elif anim_count == -1:
                    image = image_box2
            elif current_elem == " ":
                image = image_empty
            elif current_elem == "+":
                image = image_player
            elif current_elem == "*":
                image = image_box_goal
            screen.blit(image,(sprite_width*column, sprite_height*row))
    anim_count *= -1

    pygame.display.flip()
    if isDone(new_board, number_of_goals):
    	level += 1
    	print("Completed Level, moving to level: ", level)
    	new_board = getLevel(level)
    	new_position = findPlayer(new_board)
    	screen = initializeScreen(game)
    	number_of_goals = findGoals(new_board)
	
    # --- Limit to 60 frames per second
    clock.tick(30)

# Close the window and quit.
pygame.quit()
