# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *

class CoinToss(object):
	# Base class for indicators
	def __init__(self, n = 5):
		super(CoinToss, self).__init__()
		self.n = n

	def learn(self):
		pass

	def get_weights(self):
		pass

	def predict(self, inp):
		return np.random.randint(3, size=len(inp)) - 2

	def save(self):
		pass

