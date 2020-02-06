# Adding parent directory to the PYTHONPATH
import sys
import pandas as pd
sys.path.insert(0,'..')
from Indicator import Indicator
from utils.GlobalVariables import *

class EMA(Indicator):
	# Simple moving average indicator
	
	def __init__(self, period = 14, on = CLOSE):
		super(EMA, self).__init__()
		self.period = period
		self.on = on

	def calculate(self, df):
		'''
		returns the values of the simple moving average
		:param: period: the period of the SMA indicator
		:param: on: close, open, HLC/3
		:return: the SMA values as a panda series
		'''
		df[HLC_3] = (df[HIGH] + df[LOW] + df[CLOSE])/3
		out_series = df[self.on].ewm(span = self.period).mean()
		
		# For testing
		df['EMA(14)'] = out_series
		df.to_csv("../test_reports/EMA_test/EMA14.csv")
		
		return out_series

if __name__ == "__main__":
	df = pd.read_csv("..\data\Forex\GBPUSD\GBPUSD_1D.csv", index_col = 0)
	my_ind = EMA(14, CLOSE)
	my_ind.calculate(df)