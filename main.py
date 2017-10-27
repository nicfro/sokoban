import numpy as np
import pygame
import math
import copy

BLACK = (0,     0,   0)
WHITE = (255, 255, 255)
GREEN = (0,   255,   0)
RED   = (255,   0,   0)
BLUE =  (0  ,   0, 255)

image_empty = pygame.image.load("sprites/empty.png")
image_wall = pygame.image.load("sprites/wall.png")
image_player = pygame.image.load("sprites/player.png")
image_player_goal = pygame.image.load("sprites/playerGoal.png")
image_goal = pygame.image.load("sprites/goal.png")
image_box = pygame.image.load("sprites/box.png")
image_box_goal = pygame.image.load("sprites/boxGoal.png")

game = np.array([["e","e","w","w","w","w","w","e"],
				 ["w","w","w","e","e","e","w","e"],
				 ["w","g","p","b","e","e","w","e"],
				 ["w","w","w","e","b","g","w","e"],
				 ["w","g","w","w","b","e","w","e"],
				 ["w","e","w","e","g","e","w","w"],
				 ["w","b","e","@","b","b","g","w"],
				 ["w","e","e","e","g","e","e","w"],
				 ["w","w","w","w","w","w","w","w"]])

size = np.shape(game)
print(size)
pygame.init()

screen_width = size[1]*50
screen_height = size[0]*50


# Set the width and height of the screen [width, height]
screen = pygame.display.set_mode([screen_width,screen_height])

pygame.display.set_caption("Sokoban")

done = False
sprite_width = 50
sprite_height = 50

screen = pygame.display.set_mode([screen_width, screen_height])

all_sprites_list = pygame.sprite.Group()


# Used to manage how fast the screen updates
clock = pygame.time.Clock()

R = (0,1)
L = (0,-1)
U = (-1,0)
D = (1,0)
NO = (0,0)

#savedImage = pygame.image.load("sprite.png").convert()
#b.image = pygame.image.load("sprite.png").convert()

pygame.key.set_repeat(200,200)


'''
w = wall
e = empty
g = goal
b = box
@ = box on goal
p = player
# = player on goal
'''

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
		return copy.copy(board), new_position
	else:
		return copy.copy(board), position

def isDone(board, goals):
	if np.shape(np.where(board=="@"))[1] == goals:
		return 1
	else:
		return 0

new_board, new_position = move(player_pos, game, NO)
moves = 0
# -------- Main Program Loop -----------
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
            moves += 1
            new_board, new_position = move(new_position, new_board, direction)

            if event.key == pygame.K_r:
                new_board = copy.copy(game)
                find_player = np.where(game=="p")
                new_position = np.array((find_player[0][0],find_player[1][0]))

    for row in range(len(new_board)):
        for column in range(len(new_board[0])):
            current_elem = new_board[row][column]
            if current_elem == "w":
                screen.blit(image_wall,(sprite_width*column, sprite_height*row))
            elif current_elem == "p":
                screen.blit(image_player,(sprite_width*column, sprite_height*row))
            elif current_elem == "g":
                screen.blit(image_goal,(sprite_width*column, sprite_height*row))
            elif current_elem == "b":
                screen.blit(image_box,(sprite_width*column, sprite_height*row))
            elif current_elem == "e":
                screen.blit(image_empty,(sprite_width*column, sprite_height*row))
            elif current_elem == "#":
                screen.blit(image_player_goal,(sprite_width*column, sprite_height*row))
            elif current_elem == "@":
                screen.blit(image_box_goal,(sprite_width*column, sprite_height*row))


    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)
# Close the window and quit.
pygame.quit()
