from genetic_algorithm_modules import population_logging, encoder_decoder, selection, crossover, mutation
import matplotlib.pyplot as plt
import argparse
import random

# defining the CLI parser
parser = argparse.ArgumentParser(
    description='Runs a genetic algorithm to determine the maximum value of the given quadratic function.'
)

parser.add_argument('-s', '--population-size', required=True, type=int, dest='populationSize', help='number of individuals in population', metavar='POPULATION-SIZE')
parser.add_argument('-i', '--interval', required=True, type=float, nargs=2, help='bounds of interval; lowest first', metavar='INTERVAL-BOUNDARY')
parser.add_argument('-f', '--function-parameters', required=True, type=float, nargs=3, dest='parameters', help='a, b and c in f(x) = a * x ^ 2 + b * x + c', metavar='PARAMETER')
parser.add_argument('-p', '--precision', required=True, type=int, help='floating point precision of values in the given interval')
parser.add_argument('-c', '--crossover-probability', required=True, type=float, dest='crossoverProbability', metavar='CROSSOVER-PROBABILITY')
parser.add_argument('-m', '--mutation-probability', required=True, type=float, dest='mutationProbability', metavar='MUTATION-PROBABILITY')
parser.add_argument('-g', '--number-of-generations', required=True, type=int, dest='numberOfGenerations', metavar='NUMBER-OF-GENERATIONS')

arguments = parser.parse_args()

# instantiating the utility objects of each step's class
logger = population_logging.Logger()
encoderDecoder = encoder_decoder.EncoderDecoder(arguments.interval[0], arguments.interval[1], arguments.precision)
selectionPhase = selection.SelectionPhase(arguments.parameters[0], arguments.parameters[1], arguments.parameters[2], arguments.populationSize - 1)
crossoverPhase = crossover.CrossoverPhase(encoderDecoder.numberOfBits, arguments.crossoverProbability)
mutationPhase = mutation.MutationPhase(arguments.mutationProbability)

# lists used to keep track of performance metrics across generations
maximumFitnessOverGenerations = []
meanFitnessOverGenerations = []


# First generation - verbose output;
# encoding a randomly generated population within the provided interval
encodedPopulation = encoderDecoder.encodePopulation([random.uniform(arguments.interval[0], arguments.interval[1]) for _ in range(arguments.populationSize)])
decodedPopulation = encoderDecoder.decodePopulation(encodedPopulation)
fitness = selectionPhase.getFitnessOfPopulation(decodedPopulation)
# saving max fitness
fitOfFittestIndividual = max(fitness)
# and the corresponding individual
fittestIndividual = decodedPopulation[fitness.index(fitOfFittestIndividual)]
logger.logCurrentPopulation(encodedPopulation, decodedPopulation, fitness, 'Initial population')

# selection of first generation;
# only 19 individuals are returned after the selection, to accommodate the fittest one
decodedPopulation = selectionPhase.performSelection(decodedPopulation, verbose=True)
encodedPopulation = encoderDecoder.encodePopulation(decodedPopulation)
fitness = selectionPhase.getFitnessOfPopulation(decodedPopulation)
# the fittest individual must also be logged
logger.logCurrentPopulation(encodedPopulation + [encoderDecoder.encodeIndividual(fittestIndividual)], decodedPopulation + [fittestIndividual], fitness + [fitOfFittestIndividual], 'Population after selection')

# crossover of first generation;
encodedPopulation = crossoverPhase.performPopulationCrossover(encodedPopulation, verbose=True)
decodedPopulation = encoderDecoder.decodePopulation(encodedPopulation)
fitness = selectionPhase.getFitnessOfPopulation(decodedPopulation)
logger.logCurrentPopulation(encodedPopulation + [encoderDecoder.encodeIndividual(fittestIndividual)], decodedPopulation + [fittestIndividual], fitness + [fitOfFittestIndividual], 'Population after crossover')

# mutation of first generation;
# after the mutation phase, the generation in its final form is generated, so the fittest individual can be safely appended
encodedPopulation = mutationPhase.performMutations(encodedPopulation, verbose=True) + [encoderDecoder.encodeIndividual(fittestIndividual)]
decodedPopulation = encoderDecoder.decodePopulation(encodedPopulation)
fitness = selectionPhase.getFitnessOfPopulation(decodedPopulation)
logger.logCurrentPopulation(encodedPopulation, decodedPopulation, fitness, 'Population after mutations')

# the rest of the generations
for i in range(1, arguments.numberOfGenerations):
    # selection phase;
    # the fitness of the fittest individual is no longer required (no logging needed)
    fittestIndividual = max(decodedPopulation, key=lambda x: arguments.parameters[0] * x ** 2 + arguments.parameters[1] * x + arguments.parameters[2])
    decodedPopulation = selectionPhase.performSelection(decodedPopulation)
    encodedPopulation = encoderDecoder.encodePopulation(decodedPopulation)

    # crossover phase;
    # the mutation phase only uses the encoded version of each individual
    encodedPopulation = crossoverPhase.performPopulationCrossover(encodedPopulation)

    # mutation phase;
    # fittest individual must also be appended
    encodedPopulation = mutationPhase.performMutations(encodedPopulation) + [encoderDecoder.encodeIndividual(fittestIndividual)]
    decodedPopulation = encoderDecoder.decodePopulation(encodedPopulation)

    fitness = selectionPhase.getFitnessOfPopulation(decodedPopulation)
    currentMetrics = logger.logCurrentFunctionMetrics(i, fitness)
    maximumFitnessOverGenerations.append(currentMetrics[0])
    meanFitnessOverGenerations.append(currentMetrics[1])

print('[*] Generating plot...')

plt.plot(maximumFitnessOverGenerations, label='maximum fitness')
plt.plot(meanFitnessOverGenerations, label='mean fitness')
plt.xlabel('generations')
plt.show()

print('[*] Goodbye!')
