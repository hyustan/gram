# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *
from decision_models.BaseDecisionModel import BaseDecisionModel

class VP(BaseDecisionModel):
	# Base class for indicators
	def __init__(self, D = 5):
		super(VP, self).__init__()
		self.D = D

	def learn(self):
		pass

	def get_weights(self):
		pass

	def predict_value(self, inp):
		pass

	def decide(self, X, X_1, close_price, ATR, win_previous_trade):
		# Assumptions:
		'''
		X_1 is the previous feature vector
		X0 = baseline
		X1 = first_trend
		X2 = second_trend
		X3 = Volume
		'''

		if X[0]*X_1[0] < 0 and abs(close_price-X[0])<1.5*ATR and 

	def should_close(self, X):
		


	def save(self):
		pass

	def load(self):
		pass

