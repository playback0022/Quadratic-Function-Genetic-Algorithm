class Logger:
    @staticmethod
    def logCurrentPopulation(encodedPopulation: list[str], decodedPopulation: list[float], fitness: list[float], message: str) -> None:
        print(f'[*] {message}')

        for i in range(len(encodedPopulation)):
            print(f'{i + 1:4d}. {encodedPopulation[i]} -> {decodedPopulation[i]} -> fitness={fitness[i]}')
        print()

    @staticmethod
    def logCurrentFunctionMetrics(generation: int, fitness: list[float]) -> tuple[float, float]:
        # computing mean fitness value
        meanFitness = 0
        for currentFitness in fitness:
            meanFitness += currentFitness

        meanFitness /= len(fitness)
        maxFitness = max(fitness)

        print(f'[*] Generation {generation + 1}')
        print(f'    max={max(fitness):10f}, mean={meanFitness:10f}\n')
        return maxFitness, meanFitness
