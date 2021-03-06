'''
Created on Sep 10, 2015

@author: expert
'''

import os.path
from operator import mul
from itertools import product

pathToPrimesFile = os.path.join(os.path.dirname(__file__), "primes.txt")  # contains first 1.000.000 primes
assert os.path.isfile(pathToPrimesFile), pathToPrimesFile + " does not exist!"
linesOfPrimes = open(pathToPrimesFile).readlines()[2:-1:2]
    
def getFactorization(x):
    """ Returns a list which represents factorization of x:
        The "tuples" in the list have the form [prime, powerOfPrime].
        For Example getFactorization(50) returns [[2, 1], [3, 0], [5, 2]] = 2^1*3^0*5^2 = 50
    """
    
    result = []
    for i in range(len(linesOfPrimes)):
        for p in [int(p) for p in linesOfPrimes[i].split()]:
            power = 0
            while x % p == 0:
                power += 1
                x = x / p
            result.append([p, power])
            
            if x == 1: return result
            
    raise Exception("not enough primes in " + pathToPrimesFile + " for factorization of " + str(x))

def countDivisors(x):
    return reduce(mul, [factor[1] + 1 for factor in getFactorization(x)], 1)

def getDivisors(x):
    result = [1]
    for factor in getFactorization(x):
        divisorsOfFactor = [factor[0] ** i for i in range(1, factor[1] + 1)]
        result += [a * b for a, b in list(product(result, divisorsOfFactor))]
    
    return result    

def getDivisors2(x):
    result = [1]
    for factor in getFactorization(x):
        noDoubleBorder = len(result)
        borderMovement = 0
        while factor[1] > 0:
            result += [i * factor[0] for i in result[noDoubleBorder * borderMovement: ]]
            borderMovement += 1
            factor[1] -= 1
    
    return result
