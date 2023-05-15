import random

class MutationPhase:
    def __init__(self, mutationProbability: float):
        self.mutationProbability = mutationProbability


    @staticmethod
    def __mutateIndividual(individual: str, mutationPoints: list[int]) -> str:
        # converting the encoded chromosome to an integer list representation
        mutatedIndividual = [int(gene) for gene in individual]

        for mutationPoint in mutationPoints:
            # each mutated gene is negated
            mutatedIndividual[mutationPoint] = int(not mutatedIndividual[mutationPoint])

        return ''.join([str(gene) for gene in mutatedIndividual])


    def performMutations(self, population: list[str], verbose: bool = False) -> list[str]:
        mutatedIndividuals = []

        for i, individual in enumerate(population):
            # generating probabilities of mutation for each gene of every chromosome
            generatedSample = [random.random() for _ in range(len(individual))]
            mutatedGeneIndexes = [i for i, sample in enumerate(generatedSample) if sample < self.mutationProbability]

            if not mutatedGeneIndexes:
                continue

            # in order to report them, a list of mutated individuals must be kept
            mutatedIndividuals.append(i)
            population[i] = self.__mutateIndividual(individual, mutatedGeneIndexes)

        if verbose:
            print(f'[*] With a {self.mutationProbability} mutation probability, the following chromosomes mutated:')
            print(*mutatedIndividuals, '\n')

        return population
