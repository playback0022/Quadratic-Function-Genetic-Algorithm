import random

class CrossoverPhase:
    def __init__(self, numberOfBits: int, crossoverProbability: float):
        self.numberOfBits = numberOfBits
        self.crossoverProbability = crossoverProbability


    @staticmethod
    def __performCrossover(firstIndividual: str, secondIndividual: str, breakPoint: int) -> tuple[str, str]:
        segmentOfFirstIndividual = firstIndividual[breakPoint:]
        firstIndividual = firstIndividual[:breakPoint] + secondIndividual[breakPoint:]
        secondIndividual = secondIndividual[:breakPoint] + segmentOfFirstIndividual

        return firstIndividual, secondIndividual


    def performPopulationCrossover(self, population: list[str], verbose: bool = False) -> list[str]:
        # probabilities of each chromosome participating the crossover
        generatedValues = [random.random() for _ in range(len(population))]

        if verbose:
            print('[*] Crossover probabilities')

            for i, generatedValue in enumerate(generatedValues):
                print(f'{i + 1:4d}. {population[i]} - u ={generatedValue:10f}', end='')

                if generatedValue < self.crossoverProbability:
                    print(f' < {self.crossoverProbability} -> participates in crossover')
                else:
                    print()

        participatingIndividuals = [i for i, generatedValue in enumerate(generatedValues) if generatedValue < self.crossoverProbability]

        # there must be at least two participating
        # individuals for the crossover to take place
        if len(participatingIndividuals) < 2:
            if verbose:
                print()

            return population

        # dealing with an odd number of participating individuals
        if len(participatingIndividuals) % 2:
            # the last three will be dealt with separately
            mainCrossoverSet = participatingIndividuals[:-3]
        else:
            mainCrossoverSet = participatingIndividuals

        if verbose:
            print()

        # two by two, all participating individuals will go through the crossover
        for i in range(0, len(mainCrossoverSet), 2):
            breakPoint = random.randint(0, self.numberOfBits)
            firstIndividual, secondIndividual = self.__performCrossover(population[mainCrossoverSet[i]], population[mainCrossoverSet[i + 1]], breakPoint)

            if verbose:
                print(f'[*] Crossover between chromosome {mainCrossoverSet[i] + 1} and chromosome {mainCrossoverSet[i + 1] + 1}:')
                print(f'         {population[mainCrossoverSet[i]]}  {population[mainCrossoverSet[i + 1]]}  ->  point {breakPoint}')
                print(f'Result:  {firstIndividual}  {secondIndividual}')

            population[mainCrossoverSet[i]] = firstIndividual
            population[mainCrossoverSet[i + 1]] = secondIndividual

        # treating the odd number case
        if len(participatingIndividuals) % 2:
            breakPoint = random.randint(0, self.numberOfBits)
            # first two of the last three chromosomes crossover
            firstIndividual, secondIndividual = self.__performCrossover(population[participatingIndividuals[-3]],
                                                                        population[participatingIndividuals[-2]],
                                                                        breakPoint)
            # the already crossed over second to last chromosome participates in yet another crossover with the last selected chromosome
            secondIndividual, thirdIndividual = self.__performCrossover(secondIndividual,
                                                                        population[participatingIndividuals[-1]],
                                                                        breakPoint)

            if verbose:
                print(
                    f'[*] Crossover between chromosome {participatingIndividuals[-3] + 1}, chromosome {participatingIndividuals[-2] + 1} and chromosome {participatingIndividuals[-1] + 1}:')
                print(
                    f'         {population[participatingIndividuals[-3]]}  {population[participatingIndividuals[-2]]}  {population[participatingIndividuals[-1]]}  -> point {breakPoint}')
                print(f'Result:  {firstIndividual}  {secondIndividual}  {thirdIndividual}')

            population[participatingIndividuals[-3]] = firstIndividual
            population[participatingIndividuals[-2]] = secondIndividual
            population[participatingIndividuals[-1]] = thirdIndividual

        if verbose:
            print()

        return population
