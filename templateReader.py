import numpy as np
import pickle
import platform

line_ending = '\r\n'
cut = 2

if (platform.system() == 'Darwin' or platform.system() == 'Linux'): #Fixes Yuan's problem
    line_ending = '\n'
    cut = 1

def reader():
    file = open('templates.txt', 'rb')
    counter = 0
    start = False
    border_parse = False
    maps = []
    borders = []
    for line in file:
        if start == True:
            if line == bytes(line_ending):#, 'utf-8'):
                start = False
                counter += 1
            else:
                if border_parse:
                    int_line = np.fromstring(line,int,sep=" ")
                    border_parse = False
                    borders.append(int_line)
                    continue
                #line into array
                mapLine = line.decode("utf-8")
                mapLine = mapLine[:-cut]
                mapLine = list(mapLine)
                for i in mapLine:
                    if i == 'X':
                        mapLine[mapLine.index(i)] = '#'
                    if i == '*':
                        mapLine[mapLine.index(i)] = '$'
                    if i == '.':
                        mapLine[mapLine.index(i)] = '.'
                    if i == '@':
                        mapLine[mapLine.index(i)] = '@'
                    if i == ' ':
                        mapLine[mapLine.index(i)] = ' '
                    if i == 'n':
                        mapLine[mapLine.index(i)] = 'n'
                if len(maps) >= (counter + 1):
                    maps[counter].append(mapLine)
                else:
                    maps.append([mapLine])
        else:
            if line == bytes(line_ending):#, 'utf-8'):
                start = True
                border_parse = True
    return maps, borders
