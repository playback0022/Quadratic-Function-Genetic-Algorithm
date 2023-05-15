import math

class EncoderDecoder:
    def __init__(self, a: float, b: float, precision: int):
        self.a = a
        self.b = b
        self.precision = precision

        # number of bits necessary to represent numbers in [a, b] with the given precision
        self.numberOfBits = math.ceil(math.log((b - a) * (10 ** precision), 2))
        # the size of the interval of numbers which will be represented by a single value
        self.stepValue = (b - a) / 2 ** self.numberOfBits


    # the provided number should be a regular float
    def encodeIndividual(self, numberToEncode: float) -> str:
        # the admitted numbers for the given precision take the following form:
        #       a + i * stepValue, where i is between 0 and (numberOfBits - 1)
        # numbers in between (a + i * stepValue) and (a + (i + 1) * stepValue)
        # are represented as 'i';
        # therefore, computing the floor of 'i' gives us the encoded value of
        # the provided number
        indexOfNumber = math.floor((numberToEncode - self.a) / self.stepValue)
        # formatting as binary, without the '0b' prefix and filling with the
        # remaining 0s
        return f'{indexOfNumber:b}'.zfill(self.numberOfBits)


    # the provided number should be in binary
    def decodeIndividual(self, numberToDecode: str) -> float:
        return self.a + int(numberToDecode, 2) * self.stepValue


    def encodePopulation(self, population: list[float]) -> list[str]:
        return [self.encodeIndividual(individual) for individual in population]


    def decodePopulation(self, population: list[str]) -> list[float]:
        return [self.decodeIndividual(individual) for individual in population]
