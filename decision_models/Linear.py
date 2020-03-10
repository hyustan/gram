# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *
from decision_models.BaseDecisionModel import BaseDecisionModel

import numpy as np
import pandas as pd

class Linear(BaseDecisionModel):
	# Base class for indicators
	def __init__(self, D, address, name, warm_up = False, n_trained = 0):
		super(Linear, self).__init__()
		self.D = D
		self.address = address
		self.name = name
		# The model has three vectors, each vector corresponds to a decision namely SHORT, WAIT, LONG
		if warm_up:
			self.load(address, name)
		else:
			self.model = np.random.randn(3, 40)

	def learn(self, X, Y, action, lr = 0.0002):
		# Gradient descent algorithm
		# action is -1, 0, 1 for decisions, then we only apply gradient decent on the correspongfing model
		# by reaching that model in self.model
		# action+1 is for indexing
		self.model[action+1] += lr * (Y - X.dot(self.model[action+1])/X.shape[0]).dot(X)

	def get_weights(self):
		return self.model

	def predict_value(self, X):
		return X.dot(np.transpose(self.model))

	def decide(self, X):
		# The "-1" at the end is for indexing
		# ... to convert the index to decision
		return np.argmax(self.predict_value(X), axis = 1) - 1

	def save(self, address, name):
		df = pd.DataFrame(np.transpose(self.model), columns = ['SHORT', 'WAIT', 'LONG'])
		dir = address + name + '.csv'
		df.to_csv(dir)

	def load(self, address, name):
		dir = address + name + '.csv'
		self.model = np.transpose(np.array(pd.read_csv(dir, index_col = 0)))

if __name__ == '__main__':
	# Testing the matrix form
	myModel = Linear(40, "", 'Test', warm_up = False)
	X = np.random.randn(100, 40)
	Y = np.random.randn(100)

	LONG, WAIT, SHORT = 1, 0, -1
	myModel.learn(X, Y, LONG)
	# print (myModel.get_weights())

	X = np.random.randn(100, 40)
	print (myModel.predict_value(X))
	print (myModel.decide(X))
	myModel.save("", 'Test')
	myModel =Linear(40, "", 'Test', warm_up=True)
	print (myModel.predict_value(X))
	print (myModel.decide(X))

