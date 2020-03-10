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
		return 1/3

	def decide(self):
		return np.random.randint(3, size=len(inp)) - 1

	def save(self):
		pass

	def load(self):
		pass

