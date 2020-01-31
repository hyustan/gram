# Adding parent directory to the PYTHONPATH
import sys
sys.path.insert(0,'..')
from Indicator import Indicator
from utils.GlobalVariables import *

class SMA(Indicator):
	# Simple moving average indicator
	
	def __init__(self, period = 14, of = CLOSE):
		super(SMA, self).__init__()
		self.period = period
		self.of = of

	def calculate_(self):
		'''
		returns the values of the simple moving average
		:param: period: the period of the SMA indicator
		:param: of: close, open, HLC
		:return: the SMA values as a panda series
		'''
		pass

if __name__ == "__main__":
	my_SMA = SMA(20, CLOSE)
	my_SMA.calculate()