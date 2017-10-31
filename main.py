import numpy as np
import pygame
import math
import copy
import pickle

BLACK = (0,     0,   0)
WHITE = (255, 255, 255)
GREEN = (0,   255,   0)
RED   = (255,   0,   0)
BLUE =  (0  ,   0, 255)

sprite_folder ="sprites/poke/"

image_empty       = pygame.image.load(sprite_folder + "empty.png")
image_wall        = pygame.image.load(sprite_folder + "wall.png")
image_player      = pygame.image.load(sprite_folder + "player.png")
image_player_goal = pygame.image.load(sprite_folder + "playerGoal.png")
image_goal        = pygame.image.load(sprite_folder + "goal.png")
image_box         = pygame.image.load(sprite_folder + "box.png")
image_box2        = pygame.image.load(sprite_folder + "box2.png")#Outcomment if not poke
image_box_goal    = pygame.image.load(sprite_folder + "boxGoal.png")

sprite_width = 50
sprite_height = 50


game = np.array([["w","w","w","w","w","w","w","w"],
				 ["w","w","w","e","e","e","w","w"],
				 ["w","g","p","b","e","e","w","w"],
				 ["w","w","w","e","b","g","w","w"],
				 ["w","g","w","w","b","e","w","w"],
				 ["w","e","w","e","g","e","w","w"],
				 ["w","b","e","@","b","b","g","w"],
				 ["w","e","e","e","g","e","e","w"],
				 ["w","w","w","w","w","w","w","w"]])

maps = pickle.load( open( "maps.p", "rb" ))

def getLevel(level):
	return(np.asarray(maps[level]))

level = 0
game = getLevel(level)
size = np.shape(game)

pygame.init()

screen_width = size[1]*50
screen_height = size[0]*50

# Set the width and height of the screen [width, height]
screen = pygame.display.set_mode([screen_width,screen_height])



# Used to manage how fast the screen updates


R = (0,1)
L = (0,-1)
U = (-1,0)
D = (1,0)
NO = (0,0)

clock = pygame.time.Clock()
pygame.key.set_repeat(100,100)
pygame.display.set_caption("Sokoban")

'''
w = wall
e = empty
g = goal
b = box
@ = box on goal
p = player
# = player on goal
'''

def findGoals(game):
	goals1 = np.shape(np.where(game=="g"))[1]
	goals2 = np.shape(np.where(game=="@"))[1]
	return goals1+goals2

def findPlayer(game):
	find_player = np.where(game=="p")
	player_pos = np.array((find_player[0][0],find_player[1][0]))
	return player_pos

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
			if current == "#":
				board[tuple(position)] = "g"
			else:
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
		return copy.copy(board), new_position
	else:
		return copy.copy(board), position

def isDone(board, goals):
	if np.shape(np.where(board=="@"))[1] == goals:
		return 1
	else:
		return 0

new_board, new_position = move(findPlayer(game), game, NO)
moves = 0
# -------- Main Program Loop -----------
anim_count = 1

number_of_goals = findGoals(new_board)

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
            if current_elem == "w":
                image = image_wall
            elif current_elem == "p":
                image = image_player
            elif current_elem == "g":
                image = image_goal
            elif current_elem == "b":
                if anim_count == 1:
                    image = image_box
                elif anim_count == -1:
                    image = image_box2
            elif current_elem == "e":
                image = image_empty
            elif current_elem == "#":
                image = image_player
            elif current_elem == "@":
                image = image_box_goal
            screen.blit(image,(sprite_width*column, sprite_height*row))
    anim_count *= -1

    pygame.display.flip()
    if isDone(new_board, number_of_goals):
    	print("hello")
    	level += 1
    	new_board = getLevel(level)
    	new_position = findPlayer(new_board)
	



    # --- Limit to 60 frames per second
    clock.tick(30)


# Close the window and quit.
pygame.quit()
