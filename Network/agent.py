import numpy as np
import random
import pickle
import os
from collections import deque
from Network.nn import NeuralNetwork

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = NeuralNetwork(state_size, 24, action_size)
        


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))
        
    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        
        state = np.reshape(state, [1, self.state_size])
        
        act_values = self.model.forward(state)
        return np.argmax(act_values[0])
    


    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        
        minibatch = random.sample(self.memory, batch_size)
        
        for state, action, reward, next_state, done in minibatch:
            target = reward
            
            state = np.reshape(state, [1, self.state_size])
            
            if not done:
                next_state = np.reshape(next_state, [1, self.state_size])
                target = reward + self.gamma * np.amax(self.model.forward(next_state)[0])
            
            target_f = self.model.forward(state)
            target_f[0][action] = target
            
            self.model.backward(state, target_f, self.model.forward(state), self.learning_rate)
        
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


    def save(self, name):
        with open(name, 'wb') as f:
            pickle.dump({
                'weights1': self.model.weights1,
                'weights2': self.model.weights2,
                'epsilon': self.epsilon
            }, f)
            
            
    def load(self, name):
        if os.path.exists(name):
            with open(name, 'rb') as f:
                data = pickle.load(f)
                self.model.weights1 = data['weights1']
                self.model.weights2 = data['weights2']
                self.epsilon = data['epsilon']