# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *

class SMA_FT(object):
	# Base class for all of the feature transformers
	def __init__(self):
		super(SMA_FT, self).__init__()

	def transform(self, df, features):
		# it construct a set of feature to be used in the GA, RL, or even static strategies
		# We might need to modify this in the future
		df['SMA'] = features
		df['ft'] = df[df['']]



		raise NotImplementedError ("'transform' feature is not ")