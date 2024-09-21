import numpy as np

class ReductionController:
    def __init__(self, stressLevelWeight = 0.3, informationLossWeight = 0.7):
        self.__stressLevelWeight = stressLevelWeight
        self.__informationLossWeight = informationLossWeight

        self.__reductionFactor = 0.0
        self.__reductionMemory = []
        self.__reductionMemorySize = 5

    def getReductionFactor(self):
        return self.__reductionFactor
    
    def __calculateInformationLoss(self):
        informationLoss = 0.0
        for t in range(len(self.__reductionMemory)):
            informationLoss += max(self.__reductionMemory[t], 0)

        if(len(self.__reductionMemory) == 0):
            return 0.0

        informationLoss /= len(self.__reductionMemory)
        return informationLoss

    def __calculateError(self, stressLevel, informationLoss):
        return self.__stressLevelWeight * stressLevel + self.__informationLossWeight * informationLoss

    def __updateMemory(self):
        self.__reductionMemory.append(self.getReductionFactor())
        if(len(self.__reductionMemory) >= self.__reductionMemorySize):
            self.__reductionMemory.pop(0)

        self.__reductionFactor = min(1.0, max(0.0, self.__reductionFactor))

    def update(self, stressLevel):
        informationLoss = self.__calculateInformationLoss()
        error = self.__calculateError(stressLevel, informationLoss)

        print(error)

        self.__updateMemory()

