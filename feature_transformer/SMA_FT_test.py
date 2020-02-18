import sys
sys.path.insert(0,'..')
from utils.GlobalVariables import *
from data.FXDataLoader import Pair
from indicators.SMA import SMA
from  SMA_FT import SMA_FT

def exec():
	
	# Loading the data
	GBPUSD_data = Pair(GBPUSD)

	# Dataframe for test
	df = GBPUSD_data._1D

	# Creating feature
	sma = SMA(20, CLOSE)
	sma_values = sma.calculate(df)

	# Transforming the Features
	sma_transformed = SMA_FT().transform(df, sma_values)

	print (sma_transformed)

if __name__ == "__main__":
	exec()