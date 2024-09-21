import numpy as np

class ReductionController:
    def __init__(self, stressLevelWeight = 0.3, informationLossWeight = 0.7):
        self.__stressLevelWeight = stressLevelWeight
        self.__informationLossWeight = informationLossWeight

        self.__reductionFactor = 0.0
        self.__reductionMemory = []

    def getReductionFactor(self):
        return self.__reductionFactor
    
    def __calculateInformationLoss(self):
            return 0

    def __calculateError(self, stressLevel, informationLoss):
        return self.__stressLevelWeight * stressLevel + self.__informationLossWeight * informationLoss

    def update(self, stressLevel):
        informationLoss = self.__calculateInformationLoss()
        error = self.__getError(stressLevel, informationLoss)

        self.__reductionMemory.append(self.getReductionFactor())