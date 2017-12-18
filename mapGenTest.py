from mapGeneration import constructNewMap

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
