import logging
import sys
import numpy as np
import re
import random


logging.basicConfig(level=logging.DEBUG,
                    filename='../logs/CodeCraft-2019.log',
                    format='[%(asctime)s] %(levelname)s [%(funcName)s: %(filename)s, %(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filemode='a')

def readData(fileName):
    f = open(fileName)
    data = []
    count = 0
    for line in f:
        if count == 0:
            count = 1
            continue
        data.append(re.findall(r"-?\d+",line))
    data = np.array(data,dtype=np.int64)
    return data
def writeData(data,fileName):
    f = open(fileName,'w')
    for line in data:
        f.write('(')
        for i in range(len(line)):
            f.write(str(line[i]))
            if i == len(line)-1:
                continue
            f.write(',')
        f.write(')')
        f.write('\n')


def DFS(crossData,roadData, visitDone,crossId,direction=None,preCrossId=None):
    if visitDone[crossId]== 1:
        return
    visitDone[crossId] = 1
    if preCrossId is not None:
        for i in range(1,5):
            roadId = crossData[crossId][i]
            if roadId!=-1:
                pcId = roadData[roadId][4] if roadData[roadId][4]!=crossId else roadData[roadId][5]
                if pcId == preCrossId:
                    break
        shift=((i+2)%4-direction)%4
        for i in range(shift):
            crossData[crossId][1],crossData[crossId][2],crossData[crossId][3],crossData[crossId][4] = \
                crossData[crossId][2],crossData[crossId][3],crossData[crossId][4],crossData[crossId][1]
    for i in range(1,5):
        roadId = crossData[crossId][i]
        if roadId!=-1:
            nextCrossId = roadData[roadId][4] if roadData[roadId][4]!=crossId else roadData[roadId][5]
            DFS(crossData,roadData, visitDone,nextCrossId,i,crossId)


def DFS1(crossP,crossData,roadData, visitDone,crossId,direction=None,preCrossId=None):
    if visitDone[crossId]== 1:
        return
    visitDone[crossId] = 1
    if preCrossId is not None:
        for i in range(1,5):
            roadId = crossData[crossId][i]
            if roadId!=-1:
                pcId = roadData[roadId][4] if roadData[roadId][4]!=crossId else roadData[roadId][5]
                if pcId == preCrossId:
                    break
    for i in range(1,5):
        roadId = crossData[crossId][i]
        if roadId!=-1:
            nextCrossId = roadData[roadId][4] if roadData[roadId][4]!=crossId else roadData[roadId][5]
            print(crossId,nextCrossId,crossP[crossId])
            if i == 1:
                crossP[nextCrossId][0] = crossP[crossId][0]- 1
                crossP[nextCrossId][1] = crossP[crossId][1]
            elif i == 2:
                crossP[nextCrossId][1] = crossP[crossId][1]+ 1
                crossP[nextCrossId][0] = crossP[crossId][0]
            elif i == 3:
                crossP[nextCrossId][0] = crossP[crossId][0]+ 1
                crossP[nextCrossId][1] = crossP[crossId][1]
            elif i == 4:
                crossP[nextCrossId][1] = crossP[crossId][1]- 1
                crossP[nextCrossId][0] = crossP[crossId][0]
            DFS1(crossP,crossData,roadData, visitDone,nextCrossId,i,crossId)



def createCrossNet(crossData,roadData):
    crossP = np.zeros([crossData.shape[0],2],dtype=np.int64)
    visitDone = np.zeros(crossData.shape[0],dtype=np.int64)
    DFS(crossData,roadData, visitDone,11)


    visitDone = np.zeros(crossData.shape[0],dtype=np.int64)
    DFS1(crossP,crossData,roadData, visitDone,11)
    min_i = np.min(crossP[:,0])
    min_j = np.min(crossP[:,1])
    max_i = np.max(crossP[:,0])
    max_j = np.max(crossP[:,1])
    crossNet = np.zeros([max_i-min_i+1,max_j-min_j+1],dtype=np.int64)
    crossNet -= 1
    for i in range(len(crossP)):
        crossP[i][0] -= min_i
        crossP[i][1] -= min_j
        crossNet[crossP[i][0]][crossP[i][1]] = i
    return crossNet,crossP
def dfs(i,j,endi,endj,crossNet,crossData,roadData,crossFlag,route):
    if i==endi and j ==endj:
        return i,j
    idx = crossNet[i][j]
    if idx == -1:
        return i,j
    crossFlag[idx] = 1
    if i<endi and j<endj:
        d=[2,3,4,1]
    elif i<endi and j>endj:
        d=[4,3,2,1]
    elif i>endi and j>endj:
        d=[4,1,2,3]
    elif i>endi and j<endj:
        d=[2,1,4,3]
    elif i<endi and j==endj:
        d=[3,4,2,1]
    elif i>endi and j==endj:
        d=[1,4,2,3]
    elif i==endi and j>endj:
        d=[4,1,3,2]
    elif i==endi and j<endj:
        d=[2,1,3,4]
    for k in range(4):
        if crossData[idx][d[k]] == -1:
            continue
        if roadData[crossData[idx][d[k]]][6]==0 and roadData[crossData[idx][d[k]]][5]==crossData[idx][0]:
            continue
        if d[k]==1 and crossFlag[crossNet[i-1][j]]==1:
            continue
        elif d[k]==2 and crossFlag[crossNet[i][j+1]]==1:
            continue
        elif d[k]==3 and crossFlag[crossNet[i+1][j]]==1:
            continue
        elif d[k]==4 and crossFlag[crossNet[i][j-1]]==1:
            continue
        route.append(crossData[idx][d[k]])
        if d[k] == 1:
            i -= 1
        elif d[k] ==2:
            j += 1
        elif d[k] ==3:
            i += 1
        elif d[k] ==4:
            j -= 1
        i,j = dfs(i,j,endi,endj,crossNet,crossData,roadData,crossFlag,route)
        if i ==endi and j == endj:
            return i,j
        if d[k] == 1:
            i += 1
        elif d[k] ==2:
            j -= 1
        elif d[k] ==3:
            i -= 1
        elif d[k] ==4:
            j += 1
        route.pop()
    crossFlag[idx] = 0
    return i,j
def dx(cc,cc1,i,j):
    return abs(i-cc)*abs(i-cc)+abs(j-cc1)*abs(j-cc1)
def dfs1(i,j,endi,endj,crossNet,crossData,roadData,crossFlag,route):
    cc  = crossNet.shape[0]/2
    cc1  = crossNet.shape[1]/2
    if i==endi and j ==endj:
        return i,j
    idx = crossNet[i][j]
    if idx == -1:
        return i,j
    crossFlag[idx] = 1
    if i<endi and j<endj:
        d=[3,2,4,1]
        if dx(cc,cc1,i+1,j)<dx(cc,cc1,i,j+1):
            d=[2,3,4,1]
    elif i<endi and j>endj:
        d=[3,4,2,1]
        if dx(cc,cc1,i+1,j)<dx(cc,cc1,i,j-1):
            d=[4,3,2,1]
    elif i>endi and j>endj:
        d=[4,1,2,3]
        if dx(cc,cc1,i-1,j)>dx(cc,cc1,i,j-1):
            d=[1,4,2,3]
    elif i>endi and j<endj:
        d=[2,1,4,3]
        if dx(cc,cc1,i-1,j)>dx(cc,cc1,i,j+1):
            d=[1,2,4,3]
    elif i<endi and j==endj:
        d=[3,4,2,1]
        if dx(cc,cc1,i,j-1)<dx(cc,cc1,i,j+1):
            d=[3,2,4,1]
    elif i>endi and j==endj:
        d=[1,4,2,3]
        # if dx(cc,i,j-1)<dx(cc,i,j+1):
        #     d=[1,4,2,3]
    elif i==endi and j>endj:
        d=[4,1,3,2]
        # if dx(cc,i+1,j)>dx(cc,i-1,j):
        #     d=[4,1,3,2]
    elif i==endi and j<endj:
        d=[2,1,3,4]
        # if dx(cc,i+1,j)>dx(cc,i-1,j):
        #     d=[2,1,3,4]
    for k in range(4):
        if crossData[idx][d[k]] == -1:
            continue
        if roadData[crossData[idx][d[k]]][6]==0 and roadData[crossData[idx][d[k]]][5]==crossData[idx][0]:
            continue
        if d[k]==1 and crossFlag[crossNet[i-1][j]]==1:
            continue
        elif d[k]==2 and crossFlag[crossNet[i][j+1]]==1:
            continue
        elif d[k]==3 and crossFlag[crossNet[i+1][j]]==1:
            continue
        elif d[k]==4 and crossFlag[crossNet[i][j-1]]==1:
            continue
        route.append(crossData[idx][d[k]])
        if d[k] == 1:
            i -= 1
        elif d[k] ==2:
            j += 1
        elif d[k] ==3:
            i += 1
        elif d[k] ==4:
            j -= 1
        i,j = dfs1(i,j,endi,endj,crossNet,crossData,roadData,crossFlag,route)
        if i ==endi and j == endj:
            return i,j
        if d[k] == 1:
            i += 1
        elif d[k] ==2:
            j -= 1
        elif d[k] ==3:
            i -= 1
        elif d[k] ==4:
            j += 1
        route.pop()
    crossFlag[idx] = 0
    return i,j


def dfs2(i,j,endi,endj,crossNet,crossData,roadData,crossFlag,route,roadL):
    if i==endi and j ==endj:
        return i,j
    idx = crossNet[i][j]
    if idx == -1:
        return i,j
    crossFlag[idx] = 1
    if i<endi and j<endj:
        d=[3,2,4,1]
        if roadL[idx][2]<roadL[idx][3]:
            d=[2,3,4,1]
    elif i<endi and j>endj:
        d=[3,4,2,1]
        if roadL[idx][4]<roadL[idx][3]:
            d=[4,3,2,1]
    elif i>endi and j>endj:
        d=[4,1,2,3]
        if roadL[idx][1]<roadL[idx][4]:
            d=[1,4,2,3]
    elif i>endi and j<endj:
        d=[2,1,4,3]
        if roadL[idx][1]<roadL[idx][2]:
            d=[1,2,4,3]
    # elif i<endi and j==endj:
    #     d=[3,4,2,1]
    # elif i>endi and j==endj:
    #     d=[1,4,2,3]
    # elif i==endi and j>endj:
    #     d=[4,1,3,2]
    # elif i==endi and j<endj:
    #     d=[2,1,3,4]
    elif i<endi and j==endj:
        d=[3,4,2,1]
        if roadL[idx][2]<roadL[idx][4]:
            d=[3,2,4,1]
    elif i>endi and j==endj:
        d=[1,4,2,3]
        if roadL[idx][2]<roadL[idx][4]:
            d=[1,2,4,3]
    elif i==endi and j>endj:
        d=[4,1,3,2]
        if roadL[idx][3]<roadL[idx][1]:
            d=[4,3,1,2]
    elif i==endi and j<endj:
        d=[2,1,3,4]
        if roadL[idx][3]<roadL[idx][1]:
            d=[2,3,1,4]
    for k in range(4):
        #print(crossFlag[crossNet[i+1][j]])
        if crossData[idx][d[k]] == -1:
            continue
        if roadData[crossData[idx][d[k]]][6]==0 and roadData[crossData[idx][d[k]]][5]==crossData[idx][0]:
            continue
        if d[k]==1 and crossFlag[crossNet[i-1][j]]==1:
            continue
        elif d[k]==2 and crossFlag[crossNet[i][j+1]]==1:
            continue
        elif d[k]==3 and crossFlag[crossNet[i+1][j]]==1:
            continue
        elif d[k]==4 and crossFlag[crossNet[i][j-1]]==1:
            continue
        route.append(crossData[idx][d[k]])
        if d[k] == 1:
            i -= 1
        elif d[k] ==2:
            j += 1
        elif d[k] ==3:
            i += 1
        elif d[k] ==4:
            j -= 1
        i,j = dfs2(i,j,endi,endj,crossNet,crossData,roadData,crossFlag,route,roadL)
        if i ==endi and j == endj:
            return i,j
        if d[k] == 1:
            i += 1
        elif d[k] ==2:
            j -= 1
        elif d[k] ==3:
            i -= 1
        elif d[k] ==4:
            j += 1
        route.pop()
    crossFlag[idx] = 0
    return i,j
def computeDist(c1,c2,i,j):
    return c1*c1+c2*c2-int(abs(i-c1)*abs(i-c1) +abs(j-c2)*abs(j-c2))
def initRoadWeight(crossNet,crossP,crossData,roadData):
    roadW = np.zeros(crossData.shape,dtype=np.int64)
    center = crossNet.shape[0]/2-0.5
    center1 = crossNet.shape[1]/2-0.5
    for i in range(len(crossData)):
        for j in range(1,5):
            if crossData[i][j] == -1:
                roadW[i][j] = 10000
            else:
                idx = roadData[crossData[i][j]][5] -1
                roadW[i][j] = computeDist(center,center1,crossP[idx][0],crossP[idx][1])
    return roadW
def initRoadLenght(crossData,roadData):
    roadL = np.zeros(crossData.shape,dtype=np.int64)
    for i in range(len(crossData)):
        for j in range(1,5):
            if crossData[i][j] == -1:
                roadL[i][j] = 10000
            else:
                roadL[i][j] = roadData[crossData[i][j]][1]
    return roadL

def getRoute(route,map_r):
    for k,v in map_r.items():
        if route == v:
            return k

def main():
    if len(sys.argv) != 5:
        logging.info('please input args: car_path, road_path, cross_path, answerPath')
        exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

    # to read input file
    carData = readData(car_path)
    crossData = readData(cross_path)
    roadData = readData(road_path)
    map_c = dict()
    map_r = dict()
    for i in range(len(crossData)):
        map_c[crossData[i][0]] = i
    for i in range(len(roadData)):
        map_r[roadData[i][0]] = i
    for car in carData:
        car[1] = map_c[car[1]]
        car[2] = map_c[car[2]]
    for cross in crossData:
        cross[0] = map_c[cross[0]]
        for i in range(1,5):
            if cross[i]!=-1:
                cross[i] = map_r[cross[i]]
    for road in roadData:
        road[0] = map_r[road[0]]
        road[4] = map_c[road[4]]
        road[5] = map_c[road[5]]
    #writeData(crossData,'r.txt')
    # process
    
    crossNet,crossP = createCrossNet(crossData,roadData)
    crossFlag = np.zeros(crossData.shape[0],dtype=np.int64)
    roadL = initRoadLenght(crossData,roadData)
    roadW = initRoadWeight(crossNet,crossP,crossData,roadData)
    print(crossNet)

    answer = []
    route = []
    carCount = 0
    tt = 0
    maxPlanTime = 0
    carData = sorted(carData,key=lambda car: car[3],reverse=True)
    a2 = 0
    for car in carData:
        route.append(car[0])# car id
        route.append(car[4]+tt)# car plan time
        if route[1]>maxPlanTime:
            maxPlanTime = route[1]
        # if car[3] == 2:
        #     if carCount%800==0:
        #         a2 += 2
        # if car[3] == 4:
        #     if carCount%3000==0:
        #         a2 += 2
        # # if car[3] == 6:
        # #     if carCount%2000==0:
        # #         a2 += 1
        # if car[3] == 8:
        #     if carCount%3000==0:
        #         a2 -= 2
        # if carCount%(18+a2+car[3]*3)==0:
        #     tt += 1
        if carCount%(10+a2+car[3]*2)==0:
            tt += 1 
        carCount+=1
        if(carCount%100==0):
            print(carCount,tt,car[1],car[2])
        i,j = crossP[car[1]] #start cross
        endi,endj = crossP[car[2]] #end cross
        if random.randint(1,100)%3==0:
            i,j=dfs2(i,j,endi,endj,crossNet,crossData,roadData,crossFlag,route,roadL)
        else:
            #i,j=dfs2(i,j,endi,endj,crossNet,crossData,roadData,crossFlag,route,roadW)
            i,j=dfs1(i,j,endi,endj,crossNet,crossData,roadData,crossFlag,route)
        for i in range(2,len(route)):
            route[i] = getRoute(route[i],map_r)
        answer.append(route)
        for i in range(crossFlag.shape[0]):
            crossFlag[i]=0
        route=[]
    print("max plan time is",maxPlanTime)
    # to write output file
    writeData(answer,answer_path)







if __name__ == "__main__":
    main()