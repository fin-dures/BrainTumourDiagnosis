from random import randint
from itertools import pairwise
from tools import *

class neural_network():
    
    def __init__(self, input_size, output_size, weights0 = None, weights1 = None):
        
        network = []
        self.input_size=input_size
        self.output_size = output_size
        self.hidden_size = round((2/3)*input_size)+output_size
        self.weights1=weights1
        self.weights0=weights0

        
        
        if weights1==None or weights0 == None:
            
            #weights0 is the list of weights that maps each input node to each hidden node
            self.weights0=[None]*self.input_size
            #weights1 maps each hidden node to each output node
            self.weights1=[None]*self.hidden_size

            #each input node has a vector that represents how it is mapped to each hidden node
            for i in range(self.input_size):
                self.weights0[i] = [0.5]*self.hidden_size
            #each hidden node has a vector that represents how it is mapped to each output node
            for i in range(self.hidden_size):
                self.weights1[i] = [0.5]*self.output_size

        else:

            self.hidden_size = len(weights1)

            if len(self.weights0) != self.input_size or len(self.weights0[0])!= self.hidden_size or len(self.weights1[0])!=self.output_size:

                raise Exception("Ensure weights are correct sizes")



        
    def feed_forward(self, input_vector, *, show_hidden = False):

        hidden_nodes = [None]*self.hidden_size

        for hidden_index in range(len(hidden_nodes)):
            subtotal=0
            for input_index, inp in enumerate(input_vector):

                weight = self.weights0[input_index][hidden_index]
                value = weight*inp
                subtotal+=value
            subtotal/=self.input_size
            subtotal= sigmoid(subtotal)
            hidden_nodes[hidden_index]=subtotal
                
        output_nodes = [None] *self.output_size

        for output_index in range(len(output_nodes)):
            subtotal=0
            for hidden_index, hidden_node in enumerate(hidden_nodes):

                weight = self.weights1[hidden_index][output_index]
                value = weight*hidden_node
                subtotal+=value
            subtotal/=self.hidden_size
            subtotal = sigmoid(subtotal)
            output_nodes[output_index] = subtotal

        if show_hidden:
            return (output_nodes, hidden_nodes)
                
        return output_nodes


    def find_single_cost(self, input_vector, expected_output_vector):

        output = self.feed_forward(input_vector)
        total=0
        for index, output_node in enumerate(output):
            total+=0.5*(output_node-expected_output_vector[index])**2
        total/=self.output_size
        return total

    def find_total_cost(self, input_matrix, expected_output_matrix):

        outputs = []
        total=0
        for inp, exp in zip(input_matrix, expected_output_matrix):
            total+=self.find_single_cost(inp, exp)
        total/=len(input_matrix)

        return total
            

    def grad(self, input_vector, expected_output_vector):
                
                    
        output_vector, hidden_nodes = self.feed_forward(input_vector, show_hidden=True)
        output_derivatives=[]
        
        for output, expected_output in zip(output_vector, expected_output_vector):
                derivative = output_derivative(expected_output, output)
                output_derivatives.append(derivative)
                
        weight1_gradients = []


        #by starting by differentating weights1, we can use these derivatives later to find weights0
        for index1, node in enumerate(hidden_nodes):
                weight1_gradients.append([])
                for index2, deriv in enumerate(output_derivatives):
                        weight1_deriv = weight1_derivative(deriv, node)
                        weight1_gradients[index1].append(weight1_deriv)

        



        #by averaging the hidden derivatives then working out the weight0 derivatives we can reduce the time complexity from n^3 to n^2
        hidden_derivatives = []
        for hidden_node, weight_vector in zip(hidden_nodes, self.weights1):
                hidden_deriv = 0
                
                for index, weight1 in enumerate(weight_vector):
                        hidden_deriv += hidden_derivative(output_derivatives[index], weight1, hidden_node)
                        
                        
                hidden_deriv/=self.output_size
                hidden_derivatives.append(hidden_deriv)
        

        weight0_gradients = []
        for index1, inp in enumerate(input_vector):
            weight0_derivatives = []
            for index2, hidden_deriv in enumerate(hidden_derivatives):
                weight0_deriv = weight0_derivative(inp, hidden_deriv)
                weight0_derivatives.append(weight0_deriv)
            weight0_gradients.append(weight0_derivatives)
                
        
        return weight0_gradients, weight1_gradients
        


    def adjust_weights(self, input_vector, expected_output_vector, learning_rate):

        weight0_gradients, weight1_gradients = self.grad(input_vector, expected_output_vector)
        
        
        for i, vector in enumerate(weight0_gradients):
            for j, grad in enumerate(vector):
                self.weights0[i][j] += grad*learning_rate
                
                
        for i, vector in enumerate(weight1_gradients):
            for j, grad in enumerate(vector):
                self.weights1[i][j] += grad*learning_rate



    def backpropogate(self, input_matrix, expected_output_matrix, learning_rate):

        for input_vector, expected_output_vector in zip(input_matrix, expected_output_matrix):
            self.adjust_weights(input_vector, expected_output_vector, learning_rate)
        
        
    def train_network(self, input_matrix, expected_output_matrix, learning_rate, training_sessions, update_frequency):

        print("Starting cost={cost}".format(cost=self.find_total_cost(input_matrix, expected_output_matrix)))
        for i in range(training_sessions):
            self.backpropogate(input_matrix, expected_output_matrix, learning_rate)
            print("Iteration number: {i} out of {training_sessions}".format(i=i+1, training_sessions=training_sessions), end=". ")

            if (i+1)%update_frequency==0:
                cost=self.find_total_cost(input_matrix, expected_output_matrix)
                print("Cost={cost}".format(cost=cost), end="")
            print("\n")

        print("Ending cost={cost}".format(cost=self.find_total_cost(input_matrix, expected_output_matrix)))

        total=0
        for vector in input_matrix:

            output = self.feed_forward(vector)
            total+= sum(output)/len(output)

        average = total/len(input_matrix)

        return average

        
#function that tests the neural network using a fake, randomly produced dataset 
def test(variables = False):
    if variables:
        inputs, outputs, items, learning_rate, update_frequency, training_sessions= variables
        learning_rate*=-1

    else:
        inputs=int(input("Enter the number of inputs: "))
        outputs=int(input("Enter the number of outputs: "))
        items=int(input("Enter the number of items: "))
        learning_rate = float(input("Enter the learning rate as a positive float: ")) * (-1)
        update_frequency = int("Enter update frequency")
        training_sessions = int("Enter training sessions")

    a=neural_network(inputs,outputs)
    print(a.weights0)
    inp = random_matrix(items, inputs,0,100,100)
    exp = random_matrix(items, outputs,0.2,0.8,10)
    
    
    a.train_network(inp, exp,learning_rate, training_sessions, update_frequency)
    print(a.weights0)


def main():
    test([100,2,2,0.5,1,100])
    
if __name__ == "__main__":
    main()
    
