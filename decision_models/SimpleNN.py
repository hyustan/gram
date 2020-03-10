# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *
from decision_models.BaseDecisionModel import BaseDecisionModel

import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout
from keras.regularizers import l1, l2

LOSS_FUNC = 'MSE'
OPTIMIZER = 'adam'

class SimpleNN(BaseDecisionModel):
	# Base class for indicators
	def __init__(self, D, address, name, warm_up=False, n_trained=0):
		super(SimpleNN, self).__init__()
		self.D = D
		self.address = address
		self.name = name

		if warm_up:
			self.load(address, name)
		else:
			model = Sequential()
			model.add(Dense(D, input_dim = D, activation="tanh"))
			model.add(Dense(200, activation="relu"))
			model.add(Dense(3, activation="linear"))  # First one is for -1, 0, 1
			model.compile( loss=LOSS_FUNC, optimizer=OPTIMIZER)
			self.model = model

	def learn(self, X, Y):
		self.model.fit(np.atleast_2d(X), Y, epochs = 1, verbose = 0)

	def get_weights(self):
		return self.model.get_weights()

	def predict_value(self, X):
		return self.model.predict(np.atleast_2d(X))

	def decide(self, X):
		return np.argmax(self.model.predict(np.atleast_2d(X)), axis =1)-1

	def save(self, address, name):
		dir = address + name + '.h5'
		self.model.save(dir)

	def load(self, address, name):
		dir = address + name + '.h5'
		self.model = load_model(dir)

if __name__ == '__main__':
	# Testing the matrix form
	myModel = SimpleNN(40, "", 'Test', warm_up = False)
	X = np.random.randn(100, 40)
	Y = np.random.randn(100, 3)

	myModel.learn(X, Y)
	# print (myModel.get_weights())

	X = np.random.randn(100, 40)
	print (myModel.predict_value(X))
	print (myModel.decide(X))
	myModel.save("", 'Test')
	myModel =SimpleNN(40, "", 'Test', warm_up=True)

