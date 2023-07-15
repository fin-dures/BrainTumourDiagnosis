from file_handler import *
from math import log, e

class hypothesis_test():

    def __init__(self, network, significance, tail):

        self.network = network
        self.significance = significance
        self.tail = tail

    def _test(self, probability):

        if self.tail == 0:
            return float(self.significance)<float(probability)

        if self.tail == 1:
            return float(probability)>(1-float(self.significance))



def factorial(n):

    def log_factorial(n):
        
        if n==1:
            return 0
        
        return log(n, 2) + log_factorial(n-1)

    return round(2**log_factorial(n))

def choose(a, b):
    if a==b or b==0:
        return 1
    
    return factorial(a) / (factorial(b)*factorial(a-b))

 
class binomial_test(hypothesis_test):

    def __init__(self, network, significance, tests, probability):

        super().__init__(network, significance, 1)
        self.tests = tests
        self.prob = probability

    def _test(self, probability):

        super()._test(probability)

    def __bcd(self, x):
        
        if x==-1:
            return 0

        
        current = choose(self.tests,x)*self.prob**x*(1-self.prob)**(self.tests-x)

        return current+self.__bcd(x-1)
        

    def __find_probability(self, successes):

        return self.__bcd(successes-1)

    def test(self, successes):

        prob = self.__find_probability(successes)

        return super()._test(prob), (1-prob)
        

        

    

    
