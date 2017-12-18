import numpy as np
import random
from collections import defaultdict

def reader():
    file = open('templates.txt', 'rb')

    res = []
    temp = np.array([], dtype=np.int64).reshape(0,5)
    for line in file:
        read = list(line.decode("utf-8").strip('\r\n'))
        if len(read) == 0:
            res.append(temp)
            temp = np.array([]).reshape(0,5)
            continue

        temp = np.vstack([temp, np.array(read)])

    return np.array(res)

def getRandomTemplate(templateList):
    return templateList[random.randint(0, len(templateList)-1)]

def constructEmptyMap(dimensions):
    newMap = np.empty(dimensions*3, dtype=str)
    return newMap

def fitTemplate3by3(template):
    return template[1:4][...,1:4]

def checkTemplate(template, side):
    if side == "bot":
        idx = np.where(template[-1] == " ")[0]
        res = []
        for i in idx:
            if i == 0:
                continue
                #res.append("topleft")
            if i == 4:
                continue
                #res.append("topright")
            else:
                res.append((2,i-1))
    elif side == "right":
        idx = np.where(template[:,-1] == " ")[0]
        res = []
        for i in idx:
            if i == 0:
                continue
                #res.append("topleft")
            elif i == 4:
                continue
            else:
                res.append((i-1,2))
    else:
        return "CHOSE A VALID SIDE"
    return res

def getLegal(openFields):
    res = []
    for i in openFields:
        res += availableDict[i]
    
    concat = [tuple(x) for x in res]
    dupes = [x for n, x in enumerate(concat) if x in concat[:n]]
    if len(dupes) == 0:
        return 0
    else:
        idx = random.randint(0,len(dupes)-1)
        return dupes[idx]

availableDict = defaultdict(list)

'''
Creates dictionary for all open (i,j) coordinates
given a rotation
'''

def constructNewMap(dimx,dimy):
    templates = reader()

    for templateIdx in range(len(templates)):
        fitted = fitTemplate3by3(templates[templateIdx])
        
        for rot in range(4):
            temp = np.rot90(fitted, rot)
            for i in range(3):
                for j in range(3):
                    if (i == 1) and (j == 1):
                        continue

                    if temp[i][j] == " ":
                        availableDict[(i,j)].append([templateIdx,rot])

    newMap = constructEmptyMap(np.array([dimx,dimy]))
    dim = np.shape(newMap)

    x = int(dim[0]/3)
    y = int(dim[1]/3)

    templateSave = {}
    for i in range(x):
        for j in range(y):
            templateSave[(i,j)] = 0

    for i in range(x):
        for j in range(y):
            if (i == 0) and (j == 0):
                template = getRandomTemplate(templates)
                fittedTemplate = fitTemplate3by3(template)
                newMap[i*3:i*3+3][...,j*3:j*3+3] = fittedTemplate
                templateSave[(i,j)] = template
            elif (i == 0):
                requirements = checkTemplate(templateSave[(i,j-1)], "right")
                if len(requirements) == 0:
                    template = getRandomTemplate(templates)
                    fittedTemplate = fitTemplate3by3(template)
                    newMap[i*3:i*3+3][...,j*3:j*3+3] = fittedTemplate
                    templateSave[(i,j)] = template
                else:
                    fittedMaps = getLegal(requirements)
                    if fittedMaps == 0:
                        return 0
                    template = np.rot90(templates[fittedMaps[0]], fittedMaps[1])
                    fittedTemplate = fitTemplate3by3(template)
                    newMap[i*3:i*3+3][...,j*3:j*3+3] = fittedTemplate
                    templateSave[(i,j)] = template

            elif (j == 0):
                requirements = checkTemplate(templateSave[(i-1,j)], "bot")
                if len(requirements) == 0:
                    template = getRandomTemplate(templates)
                    fittedTemplate = fitTemplate3by3(template)
                    newMap[i*3:i*3+3][...,j*3:j*3+3] = fittedTemplate
                    templateSave[(i,j)] = template
                else:
                    fittedMaps = getLegal(requirements)
                    if fittedMaps == 0:
                        return 0
                    leftTemplate = np.rot90(templates[fittedMaps[0]], fittedMaps[1])
                    fittedTemplate = fitTemplate3by3(leftTemplate)
                    newMap[i*3:i*3+3][...,j*3:j*3+3] = fittedTemplate
                    templateSave[(i,j)] = template
            elif (i != 0) and (j != 0):

                requirements1 = checkTemplate(templateSave[(i-1,j)], "bot")
                requirements2 = checkTemplate(templateSave[(i,j-1)], "right")
                reqs = requirements1 + requirements2
                if len(requirements) == 0:
                    template = getRandomTemplate(templates)
                    fittedTemplate = fitTemplate3by3(template)
                    newMap[i*3:i*3+3][...,j*3:j*3+3] = fittedTemplate
                    templateSave[(i,j)] = template
                else:
                    fittedMaps = getLegal(requirements)
                    if fittedMaps == 0:
                        return 0
                    leftTemplate = np.rot90(templates[fittedMaps[0]], fittedMaps[1])
                    fittedTemplate = fitTemplate3by3(leftTemplate)
                    newMap[i*3:i*3+3][...,j*3:j*3+3] = fittedTemplate
                    templateSave[(i,j)] = template
                    
    return newMap

x = 2
y = 3
generatedMap = []
for i in range(1000):
    res = constructNewMap(x,y)
    if  res != 0:
        res = np.vstack((res,["#"]*y*3))
        res = np.vstack((["#"]*y*3, res))
        res = np.hstack((res,np.array(["#"]*((x*3)+2)).reshape(-1,1)))
        res = np.hstack((np.array(["#"]*((x*3)+2)).reshape(-1,1), res))
        generatedMap.append(res)
