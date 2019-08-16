import numpy as np
import logging
import random
from PathFinder import PathFinder
from Grid import Grid
from Node import Node
from Area import Area
import time
import os

class Simulator:
    def __init__(self,startPointsNum,endPointsNum ,iteration=1, gridTime = 150,simTime = 90, row=0, column=0,):
        self.iteration = iteration
        self.row = row
        self.column = column
        self.gridTime = gridTime
        self.simTime = simTime
        self.area = Area()
        self.startPointsNum = startPointsNum
        self.endPointsNum = endPointsNum
        self.blocks = self.area.getBlockPoint('all')
        # In channel, 0th is status that uav is launching at this second
        # 1st is launching rate of this point
        # 2nd and 3rd is (x, y) postion of destination point
        self.trainingSets = np.zeros(shape=(self.iteration, self.simTime, self.row, self.column, 4), dtype=np.float32)
        self.groundTruths = np.zeros(shape=(self.iteration, self.gridTime, self.row, self.column), dtype=np.float32)
        logging.info('finish init\n')


    def generate(self,):
        startTimeTotal = time.time()
        for index in range(self.iteration):
            logging.info('At {0} iteration'.format(index))
            grid = Grid(time=self.gridTime, row=self.row, col=self.column, blocks=self.blocks)
            grid.generateBlock()

            # startPoints = self.choosePoints(self.startPointsNum)
            # startPositions = list(map(lambda x: (x // self.column, x % self.column), startPoints))
            # endPoints = self.choosePoints(self.endPointsNum)
            # endPositions = list(map(lambda x: (x // self.column, x % self.column), endPoints))
            startPositions = self.area.getLaunchPoint(self.startPointsNum)

            for startRow, startCol, launchingRate in startPositions:
                #logging.info('   At start Point ({0}, {1})'.format(startRow, startCol))
                # set traning sets
                startRow = int(startRow)
                startCol = int(startCol)
                self.trainingSets[index, :, startRow, startCol, 1] = launchingRate

                for currentTime in range(self.simTime):
                    # generate ground truth
                    succ = np.random.uniform(0, 1) <= self.trainingSets[index, currentTime, startRow, startCol, 1]
                    if succ:
                        endRow, endCol = self.area.getDestination(self.endPointsNum)

                        # add info into channel
                        self.trainingSets[index, currentTime, startRow, startCol, 0] = 1  # launching one uav
                        self.trainingSets[index, currentTime, startRow, startCol, 2] = endRow  # destination row value
                        self.trainingSets[index, currentTime, startRow, startCol, 3] = endCol  # destination col value
                        for item in self.blocks:
                            self.trainingSets[index, currentTime, self.blocks[0], self.blocks[1], 0] = 1

                        logging.info( '      At time {0}, ({1}, {2}) --> ({3}, {4})'.format(currentTime, startRow, startCol, endRow, endCol))
                        print('      At time {0}, ({1}, {2}) --> ({3}, {4})'.format(currentTime, startRow, startCol,endRow, endCol))
                        pf = PathFinder(grid, start_x= startCol, start_y= startRow, end_x= endCol, end_y= endRow, start_t=currentTime)
                        trajectory = []
                        trajectory = pf.astar()
                        print("show tra", len(trajectory))
                        for item in trajectory:
                            # logging.info('  show path:  time, height, width ({0}, {1}, {2})'.format(item.t, item.y, item.x))
                            # print('  show path:  time, height, width ({0}, {1}, {2})'.format(item.t, item.y, item.x))
                            self.groundTruths[index, item.t, item.y, item.x] = 1

        logging.info('finish generate, cost {0}'.format(time.time() - startTimeTotal))


    def choosePoints(self, pointsNum):
        return np.random.choice(self.row * self.column, pointsNum, replace=False)

if __name__ == '__main__':
    logger = logging.getLogger()
    logger.disabled = False
    if os.path.exists("log.txt"):
        os.remove("log.txt")
    logging.basicConfig(filename='log.txt', format='%(levelname)s:%(message)s', level=logging.INFO)

    logging.info('Started')
    print("start")
    startTimeIter = time.time()
    # s = Simulator(iteration=2, row=4, column=4, time=5, startPointsNum=3, endPointsNum=3)
    # s = Simulator(iteration=10000, row=16, column=16, time=60, startPointsNum=15, endPointsNum=15)
    s = Simulator(startPointsNum=12, endPointsNum=12,iteration=3, row=32, column=32)
    s.generate()

    # logging.info('Finished')
    np.save('data/training/trainingSets_raw.npy', s.trainingSets)
    np.save('data/training/groundTruths_raw.npy', s.groundTruths)
    print('total time: ', time.time() - startTimeIter)
    # logging.info('trainingSets: \n{0}'.format(s.trainingSets))
    # logging.info('groundTruths: \n{0}'.format(s.groundTruths))
