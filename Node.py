import queue as Q
class Node:
    def __init__(self,t = 0,y = 0, x = 0):
        self.x = x
        self.y = y
        self.t = t
        self.hCost = 0
        self.gCost = 0
        self.tCost = 0
        self.parentNode = None
        # self.closed = False
        # self.opened = False
        self.walkable = True

    def __lt__(self, other):
        if self.fCost == other.fCost:
            if self.gCost == other.gCost:
                return self.hCost < other.hCost
            if self.hCost == other.hCost:
                return self.tCost < other.tCost
            return self.hCost + self.tCost < other.hCost+ other.tCost
        return self.fCost < other.fCost

    @property
    def hCost(self):
        #print("return hCost")
        return self._hCost
    @hCost.setter
    def hCost(self,value):
        #print("set hCost")
        self._hCost = value

    @property
    def gCost(self):
        #print("return hCost")
        return self._gCost
    @gCost.setter
    def gCost(self, value):
        #print("set gCost")
        self._gCost = value

    @property
    def tCost(self):
        #print("return hCost")
        return self._tCost
    @tCost.setter
    def tCost(self, value):
        #print("set Cost")
        self._tCost = value

    @property
    def fCost(self):
        #print("return fCost")
        return self._gCost + self._hCost + self._tCost



if __name__ == '__main__':
    node_1 = Node(1,5,9)
    print(node_1.hCost)
    node_1.hCost = 2
    node_1.gCost = 4
    print(node_1.hCost)
    print(node_1.fCost)
    node_2 = Node(2,2,2)
    print(node_2.hCost)
    print(node_2.fCost)
    node_3 = Node(3,5,6)
    node_3.hCost = 1
    node_3.gCost = 5
    q = Q.PriorityQueue()
    q.put(node_1)
    q.put(node_2)
    q.put(node_3)
    while not q.empty():
        print(q.get().x)




