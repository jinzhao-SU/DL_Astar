import queue as Q
from Node import Node
import logging
from Grid import Grid
from Area import Area
class PathFinder:
    def __init__(self,gridInstance,start_x,start_y,start_t,end_x,end_y):
        self.gridInstance = gridInstance
        self.gridMap = gridInstance.grid
        self.startNode = self.gridMap[start_t][start_y][start_x]
        self.endNode = Node(y = end_y, x = end_x, t = 0)
        self.end_x = end_x
        self.end_y = end_y

    def astar(self):
        openSet = Q.PriorityQueue()
        generated_path = []

        openSet.put(self.startNode)
        self.gridInstance.setOpened(self.startNode, True)
        flag = 0
        temp = []
        while not openSet.empty():
            currNode = openSet.get()
            #print("show currNode t,y,x", currNode.t, currNode.y, currNode.x)
            self.gridInstance.setClosed(currNode, True)
            self.gridInstance.setOpened(currNode, False)

            # logging.info("current node : {0}, {1}".format(currNode.y, currNode.x))
            # if reached the end position, construct the path and return it
            if currNode.x == self.end_x and currNode.y == self.end_y:
                print("we got it")
                logging.info("we got it")
                # for item in temp:
                #     print("current node : {0}, {1}".format(item.y, item.x))
                generated_path = self.buildPath(currNode)
                return generated_path

            # get neigbours of the current node
            neighbors = self.gridInstance.getNeighbors(currNode)
            for neighbor in neighbors:
                temp.append(neighbor)
                if self.gridInstance.isClosed(neighbor) :
                    continue

                if currNode.x != self.startNode.x and currNode.y != self.startNode.y:
                    if neighbor.x != currNode.parentNode.x and neighbor.y != currNode.parentNode.y:
                        flag = 6
                    else :
                        flag = 0
                    neighbor.tCost = currNode.tCost + flag

                next_gCost = currNode.gCost + self.gridInstance.getDistance(currNode, neighbor) + flag

                if (not self.gridInstance.isOpened(neighbor)) or (next_gCost < neighbor.gCost):
                    neighbor.gCost = next_gCost
                    neighbor.hCost = self.gridInstance.getDistance(neighbor,self.endNode)
                    #print("show hcost", neighbor.hCost)
                    neighbor.parentNode = currNode

                    if not self.gridInstance.isOpened(neighbor):
                        self.gridInstance.setOpened(neighbor, True)
                    openSet.put(neighbor)

        print("we have a problem")
        logging.info("we have a problem")
        logging.info(self.gridInstance.grid[0][self.endNode.y][self.endNode.x].walkable)
        for item in temp:
            logging.info("current node :{0}, {1}, {2}".format(item.t, item.y, item.x))
        return generated_path

    def buildPath(self, node):
        path = []
        while  node != self.startNode:
            path.append(node)
            node.walkable = False
            node = node.parentNode
        path.append(self.startNode)
        path.reverse()
        #print(len(path))
        return path

if __name__ == '__main__':


    area = Area()

    grid = Grid(time=150, row=32, col=32, blocks=area.getBlockPoint('all'))
    pf = PathFinder(grid, start_x=11, start_y=8, end_x=9, end_y=30, start_t=0)
    trajectory = pf.astar()
    print("show tra", len(trajectory))