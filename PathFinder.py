import queue as Q
from Node import Node
class PathFinder:
    def __init__(self,gridInstance,start_x,start_y,start_t,end_x,end_y):
        self.gridInstance = gridInstance
        self.gridMap = gridInstance.grid
        self.startNode = self.gridMap[start_t][start_y][start_x]
        self.endNode = Node(y = end_y, x = end_x, t = 0)
        self.end_x = end_x
        self.end_y = end_y
        print('destination y x: ',self.end_y, self.end_x)


    def astar(self):
        openSet = Q.PriorityQueue()
        generated_path = []

        openSet.put(self.startNode)
        self.startNode.opened = True
        flag = 0
        while not openSet.empty():
            currNode = openSet.get()
            #print("show currNode t,y,x", currNode.t, currNode.y, currNode.x)
            self.gridInstance.setClosed(currNode, False)
            # if reached the end position, construct the path and return it
            if currNode.x == self.end_x and currNode.y == self.end_y:
                print("we got it")
                generated_path = self.buildPath(currNode)
                self.gridInstance.reNew()
                return generated_path

            # get neigbours of the current node
            neighbors = self.gridInstance.getNeighbors(currNode)
            for neighbor in neighbors:
                if self.gridInstance.isClosed(neighbor) :
                    continue

                if currNode.x != self.startNode.x and currNode.y != self.startNode.y:
                    if neighbor.x != currNode.parentNode.x and neighbor.y != currNode.parentNode.y:
                        flag = 5
                    else :
                        flag = 0
                    neighbor.tCost = currNode.tCost
                next_gCost = currNode.gCost + self.gridInstance.getDistance(currNode, neighbor) + flag

                if (not self.gridInstance.isOpened(neighbor)) or (next_gCost < neighbor.gCost):
                    neighbor.gCost = next_gCost
                    neighbor.hCost = neighbor.hCost or self.gridInstance.getDistance(neighbor,self.endNode)
                    #print("show hcost", neighbor.hCost)
                    neighbor.parentNode = currNode

                if not self.gridInstance.isOpened(neighbor):
                    openSet.put(neighbor)
                    self.gridInstance.setOpened(neighbor, True)
        print("we have a problem")
        self.gridInstance.reNew()
        return generated_path

    def buildPath(self, node):
        path = []
        while  node != self.startNode:
            #print("!")
            path.append(node)
            node.walkable = False
            node = node.parentNode
        path.append(self.startNode)
        returnPath = []
        returnPath = path.reverse()
        #print(len(path))
        return path

    def mht(self):
        if self.end_y >= self.startNode.y:
            step = 1
            for y in range(self.startNode.y, self.end_y+1):
                self.gridMap[self.startNode.t+step][y][self.startNode.x] += 1
                step += 1
        else:
            step = 1
            for y in range(self.startNode.y, self.end_y-1, -1):
                self.gridMap[self.startNode.t+step][y][self.startNode.x] += 1
                step += 1
        if self.end_x <= self.startNode.x:
            step = 1
            for x in range(self.startNode.x, self.end_x+1):
                self.gridMap[self.startNode.t+step][self.end_y][x] += 1
                step += 1
        else:
            step = 1
            for x in range(self.startNode.x, self.end_x-1, -1):
                self.gridMap[self.startNode.t+step][self.end_y][x] += 1
                step += 1


    def showOnFly(self,timeStamp):
        result = []
        for y in range(len(self.gridMap[timeStamp])):
            for x in range(len(self.gridMap[timeStamp][y])):
                if self.gridMap[timeStamp][y][x] == 1:
                    result.append(Node(timeStamp, y, x))
        return result
