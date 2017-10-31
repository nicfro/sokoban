import numpy as np
import pickle

def reader():
	file = open('maps.txt', 'rb')
	counter = 0
	start = False
	maps = []
	for line in file:
	    if start == True:
	        if line == bytes('\r\n', 'utf-8'):
	            start = False
	            counter += 1
	        else:
	            #line into array
	            mapLine = line.decode("utf-8")
	            mapLine = mapLine[:-2]
	            mapLine = list(mapLine)
	            for i in mapLine:
	                if i == 'X':
	                    mapLine[mapLine.index(i)] = 'w'
	                if i == '*':
	                    mapLine[mapLine.index(i)] = 'b'
	                if i == '.':
	                    mapLine[mapLine.index(i)] = 'g'
	                if i == '@':
	                    mapLine[mapLine.index(i)] = 'p'
	                if i == ' ':
	                    mapLine[mapLine.index(i)] = 'e'
	            if len(maps) >= (counter + 1):
	                maps[counter].append(mapLine)
	            else:
	                maps.append([mapLine])
	    else:
	        if line == bytes('\r\n', 'utf-8'):
	            start = True

	return maps