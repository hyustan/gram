# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *

class BaseDecisionModel(object):
	# Base class for indicators
	def __init__(self):
		super(BaseDecisionModel, self).__init__()

	def init_model(self):
		raise NotImplementedError('init_model method has not been implemented')

	def learn(self):
		raise NotImplementedError('Learn method has not been implemented')

	def get_weights(self):
		raise NotImplementedError('get_weights method has not been implemented')

	def predict(self):
		raise NotImplementedError('predict method has not been implemented')

	def save(self):
		raise NotImplementedError('save method has not been implemented')

