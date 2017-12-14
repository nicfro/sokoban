import random
import numpy as np
import copy
from pprint import pprint
from templateReader import reader
from collections import defaultdict

#Init
size = 5
curr_spot = 0
template_map = []

for i in range(0,size):
    pass#template_map.append()

templates = reader()

availableDict = defaultdict(list)

'''
Initialize dictionary for available connections
'''
templateNumber = 0
for template in templates:
    listToAdd = template[1:-1][...,1:4]
    rot = 0
    for i in range(4):
        temp = np.rot90(listToAdd, i)
        counter = 1
        for j in temp:
            for k in j:
                if k == " ":
                    availableDict[counter].append([templateNumber,i])
                counter += 1
    templateNumber += 1

    


arr = np.array = (["e","e","e","e","e","e","e","e","e","e","e","e","e","e","e"])

for i in range (0,15):
    template_map.append(copy.deepcopy(arr))


#TODO: Fix! Not in use yet!!!!
rot_attempts = range(0,4)
temp_attempts = range(0,len(templates))
rand_template = random.randint(1,17)
rotation = random.randint(0,3)

#else:
#def checkBorder(curr_pos,template_number):

#def rotate(template):

def rotateTemplate(template, rotations):
    return np.rot90(template, rotations)

print(templates[6])
print(rotateTemplate(templates[6], 3))


def insertTemp(template):
    global curr_spot
    global size
    #pos = curr_spot * 3
    x = curr_spot // size*3
    y = curr_spot % size*3

    #For all 9 fields, try to insert them into the map.
    for i in range(x,x+3):
        for j in range(y,y+3):
            if (checkSpot(i,j,i+1,j+1,template)):
                pass
            else:
                return 0 #Failed!

    curr_spot = curr_spot+1
    return 1 # Succes!

def checkSpot(x1,y1,x2,y2,template) :
    if(template_map[x1][y1] == "e"):
        template_map[x1][y1] = template[x1%3+1][y1%3+1]
        return 1
    else:
        return 0

#insertTemp(templates[4])
#print(curr_spot)
#insertTemp(templates[4])
#print(curr_spot)
#insertTemp(templates[4])
#print(curr_spot)
#insertTemp(templates[4])
#print(curr_spot)
#pprint broke. Using this instead :P

#print(template_map[1])

#for i in range(0,15):
#    line = []
#    for j in range (0,15):
#        line.append(template_map[i][j])
#    print(line)
#    print("\n")



