import random

class SelectionPhase:
    def __init__(self, a: float, b: float, c: float, numberOfIndividuals: int):
        self.a = a
        self.b = b
        self.c = c
        self.numberOfIndividuals = numberOfIndividuals


    @staticmethod
    def __binarySearch(array: list[float], number: float) -> int:
        left = 0
        right = len(array) - 1

        while left <= right:
            mid = (left + right) // 2

            if number == array[mid]:
                return mid
            elif number < array[mid]:
                right = mid - 1
            else:
                left = mid + 1

        return right


    def __getIntervalPoints(self, individuals: list[float], verbose: bool) -> list[float]:
        if verbose:
            print('[*] Selection probabilities')

        fitness = self.getFitnessOfPopulation(individuals)
        # computing the sum of the fitness of all the individuals
        totalFitness = 0

        for fitnessOfIndividual in fitness:
            totalFitness += fitnessOfIndividual

        # probabilities based on individual fitness
        probabilities = [individualFitness / totalFitness for individualFitness in fitness]

        # the first element of the leftmost interval is always 0
        intervalPoints = [0]
        # at each step, the current probability is added to the sum calculated previously
        maximumIntervalPointValue = 0
        for i, probability in enumerate(probabilities):
            if verbose:
                print(f'chromosome {i + 1:4d} - probability {probability}')

            # maximumIntervalPointValue is the sum of all the probabilities with indexes up to 'i'
            maximumIntervalPointValue += probability
            intervalPoints.append(maximumIntervalPointValue)

        if verbose:
            print('\n[*] Selection probability intervals')
            print(*intervalPoints)

        return intervalPoints


    def getFitnessOfPopulation(self, population: list[float]) -> list[float]:
        fitness = [self.a * individual ** 2 + self.b * individual + self.c for individual in population]
        return fitness


    def performSelection(self, population: list[float], verbose: bool = False) -> list[float]:
        intervalPoints = self.__getIntervalPoints(population, verbose)
        # generating uniform values between 0 and 1, with which to select individuals;
        # the numberOfIndividuals is always one less than the actual population size,
        # to accommodate the fittest individual of the current generation
        generatedValues = [random.random() for _ in range(self.numberOfIndividuals)]

        if verbose:
            print('\n[*] Chromosome selection')

        selectedIndividuals = []
        for generatedValue in generatedValues:
            indexOfSelectedIndividual = self.__binarySearch(intervalPoints, generatedValue)
            selectedIndividuals.append(population[indexOfSelectedIndividual])

            if verbose:
                print(f'u={generatedValue:10f} -> selecting chromosome {indexOfSelectedIndividual + 1:4d}')

        if verbose:
            print()

        return selectedIndividuals
