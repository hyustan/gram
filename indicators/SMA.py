# Adding parent directory to the PYTHONPATH
import sys
import pandas as pd
sys.path.insert(0,'..')
from Indicator import Indicator
from utils.GlobalVariables import *

class SMA(Indicator):
	# Simple moving average indicator
	
	def __init__(self, period = 14, on = CLOSE):
		super(SMA, self).__init__()
		self.period = period
		self.on = on

	def calculate_(self):
		'''
		returns the values of the simple moving average
		:param: period: the period of the SMA indicator
		:param: of: close, open, HLC
		:return: the SMA values as a panda series
		'''
		pass

if __name__ == "__main__":
	df = pd.read_csv("..\data\Forex\GBPUSD\GBPUSD_1D.csv", index_col = 0)
	print (df)
	input()
	my_SMA = SMA(20, CLOSE)
	my_SMA.calculate()