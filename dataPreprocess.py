import numpy as np


class Preprocess:

    def __init__(self):
        self.gtr = np.load("data/training/groundTruths_raw.npy")
        self.tsr = np.load("data/training/trainingSets_raw.npy")
        print('raw trainingSets', self.tsr.shape)
        print('raw groundTruth: ', self.gtr.shape, '\n')

    def split(self):
        dgtr = self.gtr[:,-1:]
        dgtr = dgtr.reshape((dgtr.shape[0],dgtr.shape[2],dgtr.shape[3]))
        for i in range(dgtr.shape[0]):
            dgtr[i] = (dgtr[i] - np.min(dgtr[i])) / (np.max(dgtr[i]) - np.min(dgtr[i]))
            if np.max(dgtr[i]) != 1 or np.min(dgtr[i]) != 0:
                print('{0} data error'.format(i))
                break
        print(dgtr.shape)
        print(np.sum(self.tsr[:,-1]))
        np.save('data/training/groundTruths_density.npy', dgtr)
        self.gtr = self.gtr[:,:-1]
        self.tsr = self.tsr[:,:-1]
        print('after split')
        print('raw trainingSets', self.tsr.shape)
        print('raw groundTruth: ', self.gtr.shape)
        print('split complete\n')
    
    # only save the first sample after 30 seconds
    def fromTtoEnd(self, startTime, endTime):
        # self.gtr = self.gtr[:1, t:]
        # self.tsr = self.tsr[:1, t:]
        self.gtr = self.gtr[:, startTime:endTime]
        self.tsr = self.tsr[:, startTime:endTime]
        # self.gtr = self.gtr[:, 20:]
        # self.tsr = self.tsr[:, 20:]
        print(self.tsr.shape)
        print(self.gtr.shape)
        print('time from {0} to {1} complete\n'.format(startTime, endTime))

    def countAverageUAV(self):
        totalNum = 0
        for d1 in self.gtr:
            for d2 in d1:
                totalNum += np.sum(d2)
        ave = totalNum / self.gtr.shape[0] / self.gtr.shape[1]
        print('the average number of uav: ', ave)

    # switch all elements to zero or one 
    def oneOrZero(self):
        m = np.median(self.gtr[self.gtr!=0])
        print('median:',m)
        # self.gtr[self.gtr<=m] = 0
        # self.gtr[self.gtr>m] = 1
        self.gtr[self.gtr<m] = 0
        self.gtr[self.gtr>=m] = 1
        print('oneOrZero complete\n')


    # ground truth only save the last second (the 30th second)
    def lastSecond(self):
        gtr1 = self.gtr[:,29:,:,:].reshape((1, 16, 16))
        print('self.gtr[:,29:,:,:]: ', self.gtr[:,29:,:,:].shape)
        print('gtr1: ', gtr1.shape)
        print('self.gtr == gtr1:', np.all(gtr1==self.gtr[:,29]))
        self.gtr = gtr1
        print('lastSecond complete\n')

    # print number of non-zeros and zeros
    def computeWeights(self):
        one = self.gtr[self.gtr>0].size
        zero = self.gtr[self.gtr==0].size
        print('zero:',zero)
        print('one:',one)
        print('weight:',zero/one)
        print('computeWeights complete\n')


    # nomalize groud truth as the last second
    def batchNormalize(self):
        for i in range(len(self.gtr)):
            self.gtr[i] = (self.gtr[i] - np.min(self.gtr[i])) / (np.max(self.gtr[i]) - np.min(self.gtr[i]))
        print('min: ', np.min(self.gtr))
        print('max: ', np.max(self.gtr))
        print('mean: ', np.mean(self.gtr))
        print('median: ', np.median(self.gtr))
        print('batchNormalize complete\n')

    # broadcast one sample to many 
    def broadCast(self):
        self.tsr = np.broadcast_to(self.tsr, (10000, 30, 32, 32, 4))
        self.gtr = np.broadcast_to(self.gtr, (10000, 30, 32, 32))
        print(self.tsr.shape)
        print(self.gtr.shape)
        print('broadCast complete\n')
        
    # (30, 32, 32) --> (32, 32)
    def generateDensity(self):
        self.gtr = np.sum(self.gtr, axis=1)
        print(self.gtr.shape)
        print('generateDensity complete\n')

    def saveData(self):
        np.save('data/training/trainingSets_diff.npy', self.tsr)
        np.save('data/training/groundTruths_diff.npy', self.gtr)
        print('save complete\n')

    def checkGroundTruthIdentical(self):
        p = np.random.randint(0, len(self.gtr), 5)
        for i in range(1,5):
            print(np.all(self.gtr[p[i]] == self.gtr[p[i-1]]))
        print('checked trainingSets', self.tsr.shape)
        print('checked groundTruth: ', self.gtr.shape)
        print('check complete\n')

p = Preprocess()
# p.split()
p.fromTtoEnd(30, 90)
p.countAverageUAV()
# p.oneOrZero()
p.generateDensity()
p.batchNormalize()
p.computeWeights()
# p.broadCast()
p.checkGroundTruthIdentical()
p.saveData()