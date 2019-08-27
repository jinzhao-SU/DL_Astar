import numpy as np
from Node import Node
import logging
class Grid:
    def __init__(self,time, row, col, blocks):
        self.time = time
        self.rows = row
        self.cols = col
        self.grid = [[[Node( t,y ,x ) for x in range(self.cols)] for y in range(self.rows)] for t in range(self.time)]
        self.movement_col = (1,-1,0,0,0)
        self.movement_row = (0,0,1,-1,0)
        self.movement_time = (1,1,1,1,1)
        self.blocks = blocks
        self.openSet = [[False for x in range(self.cols)] for y in range(self.rows)]
        self.closeSet = [[False for x in range(self.cols)] for y in range(self.rows)]

    def reNew(self):
        self.openSet = [[False for x in range(self.cols)] for y in range(self.rows)]
        self.closeSet = [[False for x in range(self.cols)] for y in range(self.rows)]

    def isClosed(self, node):
        return self.closeSet[node.y][node.x]

    def setClosed(self, node, state):
        self.closeSet[node.y][node.x] = state

    def isOpened(self, node):
        return self.openSet[node.y][node.x]

    def setOpened(self, node, state):
        self.openSet[node.y][node.x] = state

    def generateBlock(self):
        for item in self.blocks:
            # print(item[0], item[1])
            for i in range(self.time):
                self.grid[i][item[0]][item[1]].walkable = False



    def getDistance(self,node_1,node_2):
        return abs(node_1.x- node_2.x) + abs(node_1.y- node_2.y)

    def isInside(self, x, y):
        return x >= 0 and x < self.cols and y >= 0 and y < self.rows

    def isWalkableAt(self, x, y,t):
        # if t > len(self.grid)-1:
        #     print("route fails, time is not enough")
        #     return -2
        return self.isInside(x,y) and (self.grid[t][y][x].walkable)

    def getNeighbors(self,node):
        neighbors = []
        for i in range(4):
            newX = node.x + self.movement_col[i]
            newY = node.y + self.movement_row[i]
            newT = node.t + self.movement_time[i]
            if self.isWalkableAt(newX,newY,newT):
                neighbors.append(self.grid[newT][newY][newX])
        return neighbors


if __name__ == '__main__':
    rows = 32
    cols =20
    time = 30
    a =[[5,5],[5,3]]
    grid = Grid(time = time, row = rows, col = cols, blocks = a)
    testNode = grid.grid[29][31][19]
    grid.grid[0][0][0].x = 1
    grid.generateBlock()
    print(len(grid.grid))
    print(testNode.x)