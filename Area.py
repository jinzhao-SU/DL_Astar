import numpy as np
import random
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

launchingArea = [
    [
        [15, 0],
        [15, 2],
        [16, 0],
        [16, 2],
    ],
    [
        [7, 10],
        [7, 11],
        [8, 10],
        [8, 11],
    ],
    [
        [23, 29],
        [23, 30],
        [24, 29],
        [24, 30],
    ]
]

destinationArea = [
    [
        [30, 9],
        [30, 10],
        [31, 9],
        [31, 10],
    ],
    [
        [7, 22],
        [7, 25],
        [9, 22],
        [9, 25],
    ],
    [
        [30, 9],
        [30, 10],
        [31, 9],
        [31, 10],
    ]
]

blockArea = [
    [15, 3],
    [16, 4],
    [8, 8],
    [8, 12],
    [25, 26],
    [23, 27],
    [15, 15],
    [13, 15],
    [5, 26],
    [18, 6],
]

class Areas:
    def __init__(self):
        self.la = np.concatenate(launchingArea, axis=0)
        self.da = np.concatenate(destinationArea, axis=0)
        self.ba = blockArea

    def getLaunchPoint(self, n, low=0, high=1):
        np.random.shuffle(self.la)
        if n < 0:
            n = len(self.la)
        result = []
        for n in range(n):
            point = random.choice(self.la)
            point = np.append(point, np.random.uniform(low, high))
            result.append(np.round(point, decimals=2))
        return np.array(result)
    
    def getDestination(self, n):
        np.random.shuffle(self.da)
        if n < 0:
            return self.da
        result = []
        for n in range(n):
            point = random.choice(self.da)
            result.append(point)
        return np.array(result)
    
    def getBlockPoint(self, n):
        np.random.shuffle(self.ba)
        if n < 0:
            return self.ba
        result = []
        for n in range(n):
            point = random.choice(self.ba)
            result.append(point)
        return np.array(result)
    
    def image(self):
        plt.plot(self.la)
        plt.savefig("result.png")

a = Areas()
lp = a.getLaunchPoint(-1)
dp = a.getDestination(-1)
bp = a.getBlockPoint(-1)



