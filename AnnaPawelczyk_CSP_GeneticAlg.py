import copy
import random
import collections



class Problem:

    alphabet = ['a','c','g','t']

    items = [
        "aaactgcatatatataccattggtaaattgggggcgaaaatcatttttactgaggggtca",
        "cattttcatatatataccattggtaaattggtcgttaaaatcatttttactagctagtca",
        "cattttcatatatataccattggtaaattggtcgttaaaatcaaaattactagctagtca",
        "catctgcatatatataccattggtaaattgggggcgaaaatcatttcacctgaggggtca",
        "catctttttatatataccattgacgagctgggggcgaaaatcatttcacctgaggggtca",
        "catcattttatatataccattggtgttggaagggcgaaaatcatttcacctgaggggtca",
        "caaaagcttatatataccattggtgtattaaaagcgaaaatcatttcacctgaggggtca",
        "aaactgatcgggtataccattggggccctgggggcgaaaatcatttctttacaggggtca",
        "cattttcatggatataccaggagtaaattggtcgttaaaatcatttttactagctagtca",
        "cattttcatatatatagtaggggtaaatcggtcgttaactttcatcttactagctagtca",
        "catctgcatatatataccattgagcctcctcgggcgaaaatcatttcacctgaggggtca",
        "catctttttatatataccattgacgagctggccctttctcttatttcacctgtccggtca",
        "catcattttatatataccattggtgttggaagggcgaaaatcttttctcctgaggggtca",
        "caaaagcttatatataccattggtgtaaatcctcatccaatcatttcacctgaggactaa",
        "aaactgcatatatataccattggtaaattgggggcgaaaatcataagaagtgaggggtca",
        "cattttcatatatataccattggtaaattggtcgttaaaatcatttgggatagctagtca",
        "cattttcatatataaataatgggtaaattggtcgttaaaatcaaaattactagctagtca",
        "gaactgcatatatataccattggtaaattgggggcgaaaatcatttcaccaaaggggtca",
        "cttgggtagagagaatttattgacgagctgggggcgaacccgggatcacctgaggggtca",
        "catcattttatatataccttccatgttggaagggcgaaaatcatttcacctgaggggtca",
        "caaaagcttatatataccattggtgtattaaaagcgccctatggttcacctgaggggtca",
        "aaacttttcagagccaccattggggccctgggggcgaaaatcatttctttacaggggtca",
        "cattttcatggatataccgcccctaaattggtcgttaaaatcatttttactagctagtca",
        "cattttcatatatatagtaggggtaaatcggtcgttattttacatcttactagctagtca",
        "catctgcatatatataccattgagcctcctcgggcgaaaatcattatccctgaggggtca",
        "catctttttatatataccattgacgagctggccctttctcttatatctcctgtccggtca",
        "catcattttatatataccattggtgttcataatgcgaaaatcttttctcctgaggggtca",
        "caaaatcatcaatataccattggtgtaaatcctcatccaatcatttcacctgaggactaa",
        "catcattttatatattcatcaggtgttggaagggcgaaaatcttttctcctgaggggtca",
        "caaaagcttatatataccattggttcataccctcatccaatcatttccttttaggactaa",
    ]


    def generateInitialPopulation(self, populationSize, schema):
        initialPopulation = []
        for i in range(populationSize):
            spice = ""
            for j in range(len(self.items[0])):
                position = random.randint(0, self.alphabet.__len__() - 1)
                spice += self.alphabet[position]
            spice = schema.applySchema(spice)
            initialPopulation.append(spice)
        return initialPopulation


    def fitnessFun1(self, spice):
        maxFitness = 0
        for itemIndex in range(self.items.__len__()):
            fitness = 0
            for position in range(len(spice)):
                if self.items[itemIndex][position] != spice[position]:
                    fitness += 1
            if fitness > maxFitness:
                maxFitness = fitness
        return maxFitness



class Schema:
    def __init__(self, isUseSchema):
        self.schemaFound = False

        if isUseSchema == False:
            return

        self.schema = [None] * len(Problem.items[0])
        self.minSchemaStatistic = 0.75
        self.schemaCleanCopy = {}
        for letter in Problem.alphabet:
            self.schemaCleanCopy[letter] = 0
        self.findSchema()
        print("This is schema: ")
        print(self.schema)


    def applySchema(self, item):
        if self.schemaFound == False:
            return item

        for position, letter in enumerate(self.schema):
            if letter != None:
                item = substituteLetterInString(item, position, letter)
        return item


    def findSchema(self):
        itemSize = len(Problem.items[0])
        for i in range(itemSize):
            statistics = copy.deepcopy(self.schemaCleanCopy)
            for item in Problem.items:
                letter = item[i]
                statistics[letter] += 1
            for letter, statistic in statistics.items():
                if statistic / Problem.items.__len__() > self.minSchemaStatistic:
                    self.schemaFound = True
                    self.schema[i] = letter


def substituteLetterInString(str, pos, letter):
    listStr = (list(str))
    listStr[pos] = letter
    return "".join(listStr)


class SolutionFinder:
    class FitnesItem:
        def __init__(self, spice, fitness):
            self.spice = spice
            self.fitness = fitness
            self.relativeFitness = 0.0


    def __init__(self, fitnessFun, generationsSize, alphabet, crossoverProbability, mutationProbability, schema):
        self.fitnessFun = fitnessFun
        self.generationsSize = generationsSize
        self.alphabet = alphabet
        self.crossoverProbability = crossoverProbability
        self.mutationProbability = mutationProbability
        self.schema = schema


    def find(self, population):
        # values for the initial population
        fitnessMatrix = self.countFitnessMatrix(population)
        elythe = self.chooseNewElythe(fitnessMatrix[0], fitnessMatrix)

        #values for next generations
        for i in range(self.generationsSize):
            matingPool = self.rouletteChoice(fitnessMatrix)
            newPopulation = self.randomlyMate(matingPool)
            fitnessMatrix = self.countFitnessMatrix(newPopulation)
            elythe = self.chooseNewElythe(elythe, fitnessMatrix)

        # print(elythe.spice, elythe.fitness)
        if elythe.fitness in result:
            result[elythe.fitness] += 1
        else:
            result[elythe.fitness] = 1

        return elythe.spice


    def countFitnessMatrix(self, population):
        fitnessMatrix = []
        fitnessSum = 0
        for spice in population:
            fitness = self.fitnessFun(spice)
            fitnessMatrix.append(SolutionFinder.FitnesItem(spice, fitness))

        for fitnessMatrixItem in fitnessMatrix:
            fitnessMatrixItem.relativeFitness = 1. / fitnessMatrixItem.fitness
        for fitnessMatrixItem in fitnessMatrix:
            fitnessSum += fitnessMatrixItem.relativeFitness
        for fitnessMatrixItem in fitnessMatrix:
            fitnessMatrixItem.relativeFitness = fitnessMatrixItem.relativeFitness / fitnessSum

        return fitnessMatrix


    def chooseNewElythe(self, elythe, fitnessMatrix):
        for fitnessItem in fitnessMatrix:
            if elythe.relativeFitness <= fitnessItem.relativeFitness:
                elythe = fitnessItem
        return elythe

    def rouletteChoice(self, fitnessMatrix):
        matingPool = []
        for i in range(fitnessMatrix.__len__()):
            spice = self.pickSpiceByRoulette(fitnessMatrix)
            matingPool.append(spice)
        return matingPool

    def pickSpiceByRoulette(self, fitnessMatrix):
        rouletteVal = random.random()
        currentVal = 0
        for fitnessItem in fitnessMatrix:
            currentVal += fitnessItem.relativeFitness
            if currentVal >= rouletteVal:
                return fitnessItem.spice
        return fitnessMatrix[fitnessMatrix.__len__() - 1].spice

    def randomlyMate(self, matingPool):
        newPopulation = []
        for i in range(matingPool.__len__()):
            spiceA = self.getRandomSpice(matingPool)
            if self.decision(self.crossoverProbability):
                spiceB = self.getRandomSpice(matingPool)
                crossingIdex = random.randint(1, matingPool.__len__() - 2)
                newSpice = spiceA[0 : crossingIdex] + spiceB[crossingIdex : len(spiceB)]
            else:
                newSpice = spiceA
            if self.decision(self.mutationProbability):
                mutationPosition = random.randint(0, len(spiceA) - 1)
                mutationValue = random.randint(0, self.alphabet.__len__() - 1)
                substituteLetterInString(newSpice, mutationPosition, self.alphabet[mutationValue])

            newPopulation.append(newSpice)


        return newPopulation

    def getRandomSpice(self, matingPool):
        rand = random.randint(0, matingPool.__len__() - 1)
        return matingPool[rand]

    def decision(self, probability):
        return random.random() < probability

if __name__ == "__main__":

    print("HELLO! It's Ania Pawelczyk here!")
    print("You are running a Genetic Algorithm that seeks for the Common Substring")
    print("for a set of nucleotide strings. Have Fun!")
    print("-----")

    result = {}

    repetitions = 50
    populationSize = 10
    generationsSize = 10
    crossoverProbability = 0.75
    mutationProbability = 0.05
    isUseSchema = True

    schema = Schema(isUseSchema)

    problemInstance = Problem()
    fitnessFun = problemInstance.fitnessFun1

    solutionFinder = SolutionFinder(fitnessFun, generationsSize, problemInstance.alphabet, crossoverProbability, mutationProbability, schema)

    for repetition in range(repetitions):
        initialPopulation = problemInstance.generateInitialPopulation(populationSize, schema)
        solutionFinder.find(initialPopulation)

    print(collections.OrderedDict(sorted(result.items())))


