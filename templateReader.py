import numpy as np
import pickle
import platform

line_ending = '\r\n'

if (platform.system() == 'Darwin' or platform.system() == 'Linux'): #Fixes Yuan's problem
    line_ending = '\n'

def reader():
    file = open('templates.txt', 'rb')

    res = []
    temp = np.array([], dtype=np.int64).reshape(0,5)

    for line in file:
        read = list(line.decode("utf-8").strip(line_ending))
        if len(read) == 0:
            res.append(temp)
            temp = np.array([]).reshape(0,5)
            continue

        temp = np.vstack([temp, np.array(read)])

    return np.array(res)
