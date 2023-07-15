from math import log, e
from random import randint
#Main neural network script was getting too full so I made a seperate script for the differentiation tools
#Note: all differentation functions find the derivative of the COST function 


#activation function with horizontal asymptotes at f(x)=0 and f(x)=1. Gradient of 1 at 0.5
def sigmoid(x):
    return 1/(1+e**(-x))


#since the derivative of sigmoid(x) is sigmoid(x)*(1-sigmoid(x)) we can simply sub in the preprocessed output to avoid having to find the sigmoid of the output twice

def sigmoid_derivative(x):

    return x*(1-x)
    


def output_derivative(expected, output):
    sd=sigmoid_derivative(output)
    return (sd)*(output-expected)

#does not call output_derivative in order to save space as many weight1 derivatives will use the same output derivative
def weight1_derivative(output_derivative, hidden_activation):

    return hidden_activation*output_derivative


def hidden_derivative(output_derivative, weight1, hidden_node):

    return output_derivative*weight1*sigmoid_derivative(hidden_node)

def weight0_derivative(inp, hidden_derivative):
    
    return inp*hidden_derivative


def random_vector(size, minimum, maximum, detail):
    
        vector = []
        for i in range(size):
            vector.append(randint((detail*minimum),(detail*maximum))/detail)

        return vector


def random_matrix(size1, size2, minimum, maximum, detail):
    
    matrix = []
    for i in range(size1):
        matrix.append(random_vector(size2, minimum, maximum, detail))

    return matrix
