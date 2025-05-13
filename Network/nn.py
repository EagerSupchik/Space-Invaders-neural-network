import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        
        self.weights1 = np.random.randn(self.input_size, self.hidden_size) / np.sqrt(self.input_size)
        self.weights2 = np.random.randn(self.hidden_size, self.output_size) / np.sqrt(self.hidden_size)
        
    def forward(self, X):
        self.z1 = np.dot(X, self.weights1)
        self.a1 = self.sigmoid(self.z1)
        self.z2 = np.dot(self.a1, self.weights2)
        self.a2 = self.sigmoid(self.z2)
        return self.a2
    
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)
    
    def backward(self, X, y, output, learning_rate):
        self.output_error = y - output
        self.output_delta = self.output_error * self.sigmoid_derivative(output)
        
        self.z1_error = self.output_delta.dot(self.weights2.T)
        self.z1_delta = self.z1_error * self.sigmoid_derivative(self.a1)
        
        self.weights1 += X.T.dot(self.z1_delta) * learning_rate
        self.weights2 += self.a1.T.dot(self.output_delta) * learning_rate