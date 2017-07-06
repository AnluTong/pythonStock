from numpy import *

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))


def randCent(dataSet, k):
    # get data set column count
    n = shape(dataSet)[1]
    # init centroid
    centroids = mat(zeros((k, n)))
    for i in range(n):
        minI = min(dataSet[:, i])
        rangeI = float(max(dataSet[:, i]) - minI)
        # generate array (line k column 1), value between min and max
        centroids[:, i] = minI + rangeI * random.random(size=(k, 1))
    return centroids


"""
    kmean 
    return an tuple
    first element is centroid array
    second element is assignment array which is an array too
    size of assignment equals to data set
    assignment element one is index of centroid the point belong to
    assignment element two is dist*dist from point to centroid
"""
def kMeans(dataSet, k, distMeas=distEclud, createRandCent=randCent):
    # get data set line count
    N = shape(dataSet)[0]
    # init data assignment array
    # column 0 represent the index of centroid the point belong to
    # column 1 represent the dist*dist from point to centroid
    clusterAssment = mat(zeros((N, 2)))
    # generate centroid point
    centroids = createRandCent(dataSet, k)
    # stop flag
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        # update the assignment array of every point
        for line in range(N):
            minDist = inf
            minIndex = -1
            # find the nearest centroid point the line belong to
            for i in range(k):
                # get measure distance from one centroid to one point
                distIJ = distMeas(centroids[i, :], dataSet[line, :])
                if distIJ < minDist:
                    minDist = distIJ
                    minIndex = i
            if clusterAssment[line, 0] != minIndex:
                clusterChanged = True
            clusterAssment[line, :] = minIndex, minDist ** 2
        # update the centroid value upon assignment
        for cen in range(k):
            # nonzero(clusterAssment[:, 0].A == centroid)[0]
            # return array(column is 1) which cen point belong to
            # ptsInClust get all of upon data in data set
            ptsInClust = dataSet[nonzero(clusterAssment[:, 0].A == cen)[0]]
            if len(ptsInClust) != 0:
                centroids[cen, :] = mean(ptsInClust, axis=0)
    return centroids, clusterAssment


### bisecting K-means  
def biKmeans(dataSet, k, distMeas=distEclud):
    N = shape(dataSet)[0]
    clusterAssment = mat(zeros((N, 2)))
    centroid0 = mean(dataSet, axis=0).tolist()[0]
    centList = [centroid0]
    for ii in range(N):
        clusterAssment[ii, 1] = distMeas(mat(centroid0), dataSet[ii, :]) ** 2
    while (len(centList) < k):
        lowestSSE = inf
        for ii in range(len(centList)):
            ptsInCurrCluster = dataSet[nonzero(clusterAssment[:, 0].A == ii)[0], :]
            centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeas)
            sseSplit = sum(splitClustAss[:, 1])
            sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:, 0].A != ii)[0], 1])
            if (sseSplit + sseNotSplit) < lowestSSE:
                bestCentToSplit = ii
                bestNewCents = centroidMat
                bestClustAss = splitClustAss.copy()
                lowestSSE = sseSplit + sseNotSplit
        bestClustAss[nonzero(bestClustAss[:, 0].A == 1)[0], 0] = len(centList)
        bestClustAss[nonzero(bestClustAss[:, 0].A == 0)[0], 0] = bestCentToSplit
        centList[bestCentToSplit] = bestNewCents[0, :]
        centList.append(bestNewCents[1, :])
        clusterAssment[nonzero(clusterAssment[:, 0].A == bestCentToSplit)[0], :] = bestClustAss
    return mat(centList), clusterAssment  